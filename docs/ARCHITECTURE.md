# How Notarius works

Notarius is one Python script, `notarius.py`, plus one page, `dashboard.html`. `uv` runs the
script using the dependencies declared at its top (PEP 723), so there is no separate install step.

## Processes

```
Notarius tray app (python, hidden console)       started by the Start-menu / login shortcut (uvw)
├─ tray icon (pystray)                           status colour, menu, "Minutes ready" toast
├─ watcher thread                                polls Teams audio every 2 s, records calls
├─ dashboard server (127.0.0.1:8765)             serves dashboard.html + a JSON API
├─ window child process (`window`)               the app window: dashboard.html in Edge
│                                                WebView2 (pywebview); closing it ends it
└─ per meeting, when the call ends:
   └─ _transcribe child process                  transcription + minutes, isolated so a GPU
      ├─ _diarize child process                  library crash can't take down the tray app
      └─ claude -p (Claude Code CLI, Haiku)      writes the minutes from the transcript
```

Only one tray app runs per Windows session (a named mutex), so a call is never recorded twice.

**The app window** is a separate process, so closing it frees its memory and its session (the PIN
is asked again), and a fault in the window can't stop a recording. Only one window opens: opening
Notarius again brings it to the front. Processes set the Windows app ID `Notarius.MeetingNotes`,
which the shortcuts carry too, so the window gets its own taskbar button and pins, and
notifications show as Notarius. The window remembers its size (`window.json`); its browser
profile (`webview\`) holds only the theme and tour state. The right-click menu is cut down to
editing commands, and Word/PDF downloads open a Save As dialog. Without WebView2 the window falls
back to an Edge app window, then to the default browser.

## 1. Detecting a call

`teams_audio_devices()` enumerates the Windows audio sessions on every active output and input
device (pycaw/WASAPI). A call is in progress when a process belonging to Teams (`ms-teams.exe`,
`teams.exe` or a child such as its WebView2) has an **active output stream**. Teams opens it on
join and holds it until you leave, muted or not.

- Recording starts after 8 seconds of an active stream, which skips chat pings.
- Recording stops 30 seconds after the stream closes, which survives holds and device switches.
- Calls under 60 seconds are discarded.

## 2. Recording

`Recording` opens two WASAPI streams with pyaudiowpatch:

- `mic.wav`: the microphone Teams is using. Everything on this track is "Me".
- `others.wav`: a loopback of the speaker or headset Teams is playing to, which carries everyone
  else.

Loopback delivers nothing while the output is silent, so gaps are padded with silence against a
shared clock. This keeps the two tracks aligned in time.

## 3. Transcription (`_transcribe` child)

1. **Speaker separation starts at once** in its own process (`_diarize`), on the CPU, in
   parallel with the GPU work below.
2. **Language per stretch of speech.** Voice-activity detection splits each track into sentences.
   - Whisper detects the language of each ~15-second window.
   - Windows that are less than 90% sure, which is where people switch language, are re-checked
     sentence by sentence.
   - Hindi and Urdu are folded into one language, written in one script per meeting.
   - Consecutive sentences in the same language are transcribed together, with that language set
     explicitly. Without this, Whisper translates a second language instead of transcribing it.
3. **Batched GPU transcription.** faster-whisper `large-v3-turbo` runs in fp16 on CUDA through
   `BatchedInferencePipeline`, at about 1 minute per hour of audio on an RTX 4050. It falls back
   to sequential decoding on error, and to int8 on the CPU if CUDA fails.
4. **Echo removal on your mic.** Your microphone also hears the call (speakers, or a headset that
   leaks), and Teams mute doesn't mute the device. There are two independent layers:
   - **Words.** Both tracks are transcribed with word timestamps. A run of two or more words on
     your mic that matches call-audio words within ±1.5 s is dropped. A single matching word is a
     coincidence and is kept.
   - **Sound.** This catches leaked speech that Whisper mishears as other words or another
     language. Notarius measures once per meeting how the call leaks into the mic: the delay, and
     the coupling (how loud the call is on the mic), which your speakers, mic and room keep
     constant. For each mic sentence, loudness above `1.5 × coupling × call` is your own voice. A
     sentence with less than 45% of your own voice is dropped.

   Talking over someone keeps your words, because your voice is the excess. In tests, leaked
   audio scored at most 0.33, talking over someone 0.57, and plain speech 1.00.

   Segments that Whisper itself marks as unlikely are discarded: high no-speech probability with
   low confidence, very low confidence, or repetitive output. A language heard for only a few
   seconds (under 20% of the speech and under 45 s) is treated as a misdetection.

   Your remaining words are regrouped into sentences at pauses, so talk time is measured from
   words, not from Whisper's 30-second batches.
5. **Teams mute and captions.** While recording, a `TeamsObserver` thread reads the Teams meeting
   window once a second through Windows UI Automation:
   - It finds the window by the mic button's automation id (`microphone-button`). The button's
     label ("Unmute mic" while muted) gives a muted/unmuted timeline.
   - The live captions panel, found from `captions-panel-dismiss-button`, yields
     `(speaker, text)` pairs (each entry is a group of two texts). They're merged across polls
     with first-seen and last-changed times.
   - If no captions panel appears within 15 s, the observer invokes `closed-captions-button`
     once.
   - The data is sealed into `teams.json` and handed to the processing child as a temporary plain
     copy.

   Processing then:
   - drops your mic words inside muted stretches;
   - finds which caption name is you (the name whose caption words appear on your mic rather than
     in the call audio);
   - drops mic words that are someone else's captioned speech.

   Each call-audio word takes the speaker of the caption showing at that moment (caption window
   `[t0 - 3 s, t1 + 1 s]`) that contains the word. Words the captions don't decide take the
   majority caption name of their voice cluster, or else stay with the cluster. Caption names
   also enroll voices for meetings without captions.

   In a simulated 4-person call with rough captions (25% of words dropped, 10% misheard), 17 of
   17 lines were attributed correctly, and the line spoken while muted was dropped.
6. **Speaker labels (without captions).** Separation uses sherpa-onnx with pyannote segmentation 3.0 and WeSpeaker
   ResNet34 embeddings, giving "who spoke when". Call-track words are assigned to speakers by
   their timestamps, and one-word flips at turn boundaries are smoothed out.

   A fixed clustering threshold over-splits people whose call audio varies. A clean-up step
   reuses the fingerprints already computed, so it adds no processing time:
   - voices with under 5 s of speech fold into the voice they resemble most;
   - voices whose averaged fingerprints are ≥ 0.86 similar merge (different people measured up
     to 0.83);
   On a synthetic test with varying audio this took 4 people from 6 speakers to 4, and 2 people
   from 3 to 2.

   **Recognizing named voices.** A wrong name is worse than no name, so a voice is named only when
   all of these hold:
   - it has at least 15 s of speech;
   - its fingerprint is at least 0.75 similar to one remembered person;
   - that person beats the next-best by at least 0.08;
   - each remembered person names at most one voice per meeting.

   Recognition never merges voices. Voices are only remembered from speakers with at least 15 s
   of speech. Settings has **Forget remembered voices** to start over.
7. **Minutes first, names later.** If separation isn't done 20 seconds after transcription, the
   minutes are written straight away with the call audio as "Others". They are rewritten with
   speakers when separation finishes. In practice this applies to long meetings, since
   separation runs at about 1/6 of real time.

## 4. Minutes

`write_notes()` runs `claude -p --model haiku --no-session-persistence --strict-mcp-config` with
the transcript on stdin. The prompt in `NOTES_PROMPT` fixes the output format:

- the title line;
- `**Date/Time/Attendees**`;
- `**Summary:**`;
- `## Minutes`, with one `###` section per topic and `**Decision:**` lines;
- the `## Action Items` table (`# | Action | Owner | Due`).

The headings stay in English whatever the minutes language, because the dashboard parses them.
The model also returns the names it inferred for unnamed speakers as JSON in an HTML comment.
These become *suggestions* in the dashboard; nothing is saved as a voice until you confirm it.

The transcript is treated as data, not instructions, and the prompt says so.

Each minutes language is kept as `notes.<language>.md`, so switching back costs nothing. The saved
versions are dropped when speaker names change.

## 5. Storage and encryption

Meetings live in `%LOCALAPPDATA%\Notarius\Meetings\<YYYY-MM-DD_HHMMSS>\`:

| File | Contents | On disk |
|---|---|---|
| `meta.json` | start time, duration, devices, status flags | plain |
| `notes.md`, `notes.<lang>.md` | minutes | encrypted (`.enc`) |
| `transcript.md`, `segments.json` | transcript, timed lines | encrypted |
| `speakers.json` | speakers, fingerprints, names | encrypted |
| `my_notes.md` | your notes | encrypted |
| `actions.json` | which action items are ticked | plain (indexes only) |
| `mic.wav`, `others.wav` | audio, only until processed | plain, then deleted |

Other files in the `Meetings` folder:

- `_days\*.md`: day notes, encrypted;
- `_voices.bin`: named voices, DPAPI-protected;
- `_settings.json`: name and languages;
- `_vault.json`: keys.

**Vault.** An X25519 key pair is created when you set your PIN.

- **Sealing.** Every sensitive file is sealed to the public key with an ephemeral X25519 key
  exchange, HKDF-SHA256 and AES-256-GCM. This means the recorder can save new meetings without
  the PIN.
- **The private key** is stored wrapped twice: by scrypt(PIN) (n = 2^17) with AES-GCM, and then by
  Windows DPAPI, which ties it to your Windows account.
- **The recovery key** is 24 random base32 characters, about 120 bits. It wraps the same private
  key with its own scrypt + AES-GCM, without DPAPI, so it can also restore notes after a Windows
  reinstall.

**Dashboard sessions.**

- **Unlocking.** Unlocking loads the private key into memory and returns a random session token.
  The page keeps the token in memory only (sent as `X-Session`, never a cookie), so a reload, a
  new tab or a newly opened window asks for the PIN again.
- **Expiry and locking.**
  - Sessions expire after 5 minutes idle; the page also locks after 1 minute away from the tab.
  - All sessions end, and the key is dropped from memory, when Windows shows its lock screen
    (`LogonUI.exe`).
  - When the last session ends, the key leaves memory.
- **Wrong PINs.** After 5 wrong PINs, attempts pause for 15 seconds, doubling each time up to
  5 minutes.

**Web hardening.**

- The server binds to `127.0.0.1` only.
- It checks the `Host` header, which stops DNS rebinding.
- State-changing requests need a custom `X-Notetaker` header, so other websites can't send them
  without a CORS preflight that the server never answers.
- Responses carry `X-Frame-Options: DENY`.
- PDF export prints a page with headless Edge, using a one-time token that is valid for 2
  minutes.

**Exports.** Word and PDF files carry the Notarius look: the logo and name at the top, purple
headings, an action table with a purple header row that repeats on each page, and a
"Minutes taken by Notarius · Page X of Y" footer. Their document properties hold the meeting
title, your name as author and the Notarius version. The logo is drawn from the same numbers as
`assets/logo.svg` and served at `/logo.svg`.

## 6. Dashboard API

| Method | Path | |
|---|---|---|
| GET | `/api/auth` | is a PIN set, is this page unlocked, is there a recovery key |
| POST | `/api/auth/setup`, `/login`, `/logout`, `/recover`, `/change`, `/recovery-key` | PIN lifecycle |
| GET | `/api/status` | watching / recording / processing / paused (no PIN needed) |
| GET | `/api/meetings`, `/api/meetings/<id>`, `/api/search?q=` | meetings |
| PUT | `/api/meetings/<id>/my_notes`, `/actions`, `/api/days/<date>`, `/api/settings` | edits |
| POST | `/api/meetings/<id>/speakers`, `/rewrite`, `/retry`, `/api/pause` | actions |
| GET | `/api/export.docx?ids=`, `/api/export.pdf?ids=` | exports |

## 7. Configuration

Environment variables (all optional):

| Variable | Default | Purpose |
|---|---|---|
| `NOTETAKER_CLAUDE_MODEL` | `haiku` | model for the minutes |
| `NOTETAKER_MODEL` | `large-v3-turbo` | Whisper model |
| `NOTETAKER_LANG` | (settings) | force one spoken language, e.g. `ur` |
| `NOTETAKER_DIR` | `%LOCALAPPDATA%\Notarius\Meetings` | meetings folder |
| `NOTETAKER_PORT` | `8765` | dashboard port |
| `NOTETAKER_KEEP_AUDIO` | off | `1` keeps the WAV files |
| `NOTETAKER_CLUSTER_THRESHOLD` | `0.5` | speaker separation; higher means fewer speakers |
| `NOTETAKER_VOICE_MATCH` | `0.5` | similarity needed to recognize a voice |
| `NOTETAKER_DIARIZE_WAIT` | `20` | seconds to wait for speakers before writing the minutes first |
| `CLAUDE_BIN` | (found on PATH) | path to the Claude Code CLI |

## 8. Commands

```powershell
uv run --script notarius.py install              # shortcuts, login item, Settings > Apps entry
uv run --script notarius.py uninstall [--quiet]   # undo install; --quiet asks nothing, keeps data
uv run --script notarius.py open                  # tray app + app window (what the shortcuts run)
uv run --script notarius.py tray                  # tray app only (login item)
uv run --script notarius.py window                # the app window alone (the tray app opens it)
uv run --script notarius.py version               # print the version
uv run --script notarius.py watch                 # watcher + dashboard in a console, live logs
uv run --script notarius.py record                # record now; Ctrl+C stops (any app)
uv run --script notarius.py status                # is a Teams call detected right now?
uv run --script notarius.py process <meeting dir> # redo a meeting (needs its audio or transcript)
```

Logs go to `%LOCALAPPDATA%\Notarius\notetaker.log`. They record events and timings, not content.

## 9. Building Notarius.exe

`build-exe.cmd` (or `uv run --script build-exe.py`) packs `launcher.py`, with `notarius.py` and
`dashboard.html` inside, into `dist\Notarius.exe` with PyInstaller. Set `VERSION` in
`notarius.py` before a release; the build stamps it, the publisher and the copyright into the
.exe's version details (Properties > Details, Task Manager). It is built without UPX, which makes
antivirus scanners flag unsigned files, and writes `Notarius.exe.sha256` next to it.

The launcher installs per user, with no admin rights, the way other Windows apps do:

1. it copies itself, `notarius.py` and `dashboard.html` to `%LOCALAPPDATA%\Programs\Notarius`
   (program files), separate from `%LOCALAPPDATA%\Notarius` (meetings, voices, models), which
   updates never touch;
2. when the version changed, it runs `install`. That points the shortcuts at the installed
   `Notarius.exe`, gives them the app ID, and writes the Settings > Apps entry (version,
   publisher, icon, size, uninstall command);
3. it starts the app through `uvw`, passing `NOTARIUS_LAUNCHER` so the app knows it was installed
   by the .exe.

A newer `Notarius.exe` updates the installed copy; an older one starts the installed newer
version instead of downgrading it. **Uninstall** (from Settings, or `Notarius.exe uninstall`)
asks the running app to quit (a named event; it saves a recording first), removes the shortcuts,
the Settings entry and the program folder, and deletes your data only if you say so.

**Code signing.** The .exe isn't signed yet, so SmartScreen warns about an unknown publisher and
Smart App Control blocks it. With a code-signing certificate, set `NOTARIUS_SIGN_CERT` (a .pfx
path, with `NOTARIUS_SIGN_PASSWORD`, or a certificate thumbprint) and put `signtool.exe` on
PATH: the build then signs and timestamps the .exe. The script install doesn't have this
problem.

## 10. Measured performance

RTX 4050 laptop GPU, i5-14500HX:

| Step | Speed |
|---|---|
| Transcription (batched, GPU) | ~1.1 min per hour of audio |
| Language checks | a few seconds per hour |
| Speaker separation (CPU, parallel) | ~10 min per hour of call audio |
| Minutes (Claude Haiku) | 10-20 s |
| 2-minute call, end to end | ~45 s after leaving |
