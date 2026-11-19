# Meeting Notes (teams-notetaker)

A local note-taker for Microsoft Teams on Windows. It starts recording when you join a Teams
call and writes minutes of meeting with action items when you leave. No bot joins the call.
Audio, transcripts and voice data stay on your laptop. The only thing sent out is the
transcript text, which goes to your own Claude Code (Haiku) to write the minutes.

- **Starts on join.** It detects the Teams call audio, so it works whether you're muted or not.
- **Transcribes locally** with faster-whisper on your GPU, at about 15x real time. Without a
  GPU it falls back to the CPU.
- **Labels people.** Voices on the call are separated into Speaker 1, Speaker 2, and so on.
  Claude suggests names from the conversation. Name a voice once in the dashboard and it's
  recognized by voice in later meetings.
- **Writes minutes:** topics, decisions, and an action-items table with owner and due date.
- **Dashboard** at http://127.0.0.1:8765. A calendar where you pick a day or drag across a
  range to see every meeting and its open action items. Tick off actions, keep notes per
  meeting and per day, search everything, copy the minutes, and export to **Word** or **PDF**.
- **Tray app,** like Docker Desktop. The icon is purple while watching, red while recording,
  and amber while writing minutes. Right-click it for Open dashboard, the current status, and Quit.

## Install

Requirements:

- Windows 10/11 and the new Teams desktop app
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- [Claude Code](https://claude.com/claude-code), logged in
- An NVIDIA GPU is optional but makes transcription much faster.

```powershell
git clone https://github.com/uzair-khan-ATS/teams-notetaker
cd teams-notetaker
uv run --script notetaker.py install
```

This adds **Meeting Notes** to the Start menu and Desktop and starts it at every login. Open
it once now: the first start downloads the speech models (~3 GB, one time) and opens the
dashboard. After that it runs in the tray and takes notes on its own.

To quit, right-click the tray icon (under the **^** next to the clock) and choose **Quit
Meeting Notes**. To uninstall, run `uv run --script notetaker.py uninstall`. Your notes stay
in `Documents\MeetingNotes`.

<details><summary>Other commands</summary>

```powershell
uv run --script notetaker.py open        # start the tray app (if needed) and open the dashboard
uv run --script notetaker.py watch       # same, in a console window with live logs
uv run --script notetaker.py record      # record now, Ctrl+C to stop (Teams in a browser, etc.)
uv run --script notetaker.py status      # during a call: is Teams detected?
uv run --script notetaker.py process "<meeting folder>"   # rewrite the minutes
```

The log is at `%LOCALAPPDATA%\teams-notetaker\notetaker.log`.
</details>

## Settings (environment variables)

| var | default | |
|---|---|---|
| `NOTETAKER_CLAUDE_MODEL` | `haiku` | model that writes the minutes |
| `NOTETAKER_MODEL` | `large-v3-turbo` | Whisper model; `small` is lighter but less accurate |
| `NOTETAKER_LANG` | auto | force the spoken language, e.g. `en`, `ur`, `hi` |
| `NOTETAKER_DIR` | `~/Documents/MeetingNotes` | where meetings are saved |
| `NOTETAKER_PORT` | `8765` | dashboard port (bound to 127.0.0.1 only) |
| `NOTETAKER_KEEP_AUDIO` | off | `1` keeps the WAV recordings |
| `NOTETAKER_CLUSTER_THRESHOLD` | `0.5` | speaker separation; higher means fewer speakers |
| `NOTETAKER_VOICE_MATCH` | `0.5` | how similar a voice must be to be recognized |

## What's in a meeting folder

`Documents\MeetingNotes\<date_time>\`:

| file | contents |
|---|---|
| `notes.md` | minutes and action items |
| `transcript.md` | the transcript |
| `my_notes.md` | your own notes |
| `segments.json` | timed transcript lines |
| `speakers.json` | detected voices |
| `meta.json` | date and duration |

Recognized voices are stored in `_voices.json`, and day notes in `_days\`.

## Limits

- Use a headset. On laptop speakers the mic also picks up everyone else.
- Speaker separation works best when people take turns. Heavy cross-talk can merge or split voices.
- Switching audio devices mid-call isn't followed. The recording stays on the device the call started on.
- Let people know you're taking notes, and follow your company's policy on recording.
