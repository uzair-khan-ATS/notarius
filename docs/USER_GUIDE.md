# Notarius user guide

Notarius takes the minutes of your Microsoft Teams meetings on your own Windows laptop. Leave it
running in the tray. When you join a Teams call it records; when you leave, it transcribes the
call locally and writes minutes of meeting with action items. Read them in its dashboard.

**Contents**

1. [Install](#1-install)
2. [First start: PIN and recovery key](#2-first-start-pin-and-recovery-key)
3. [Everyday use](#3-everyday-use)
4. [The dashboard](#4-the-dashboard)
5. [People and speaker names](#5-people-and-speaker-names)
6. [Languages](#6-languages)
7. [Privacy and security](#7-privacy-and-security)
8. [Troubleshooting](#8-troubleshooting)
9. [Uninstall](#9-uninstall)

---

## 1. Install

Requirements:

- Windows 10 or 11, and the **new Teams desktop app**. Teams in a browser can't be detected
  automatically; see [Troubleshooting](#8-troubleshooting).
- **[uv](https://docs.astral.sh/uv/getting-started/installation/)**, a small free tool that
  installs Python and Notarius's libraries for it.
- **[Claude Code](https://claude.com/claude-code)**, installed and logged in. Notarius uses it to
  write the minutes, with the small Haiku model.
- A headset is recommended, and an NVIDIA GPU is recommended for speed.

### Option A: install from the repository (recommended)

```powershell
git clone https://github.com/uzair-khan-ATS/notarius
cd notarius
uv run --script notarius.py install
```

`install` adds **Notarius** to the Start menu, the Desktop and your login items. It works with
**Smart App Control** turned on, because it launches through `uvw.exe`, which is signed.

### Option B: Notarius.exe

Download `Notarius.exe` from the
[releases page](https://github.com/uzair-khan-ATS/notarius/releases) and double-click it. On first
run it creates the same shortcuts. You still need uv and Claude Code; if uv is missing, it opens
the uv download page.

> **Smart App Control.** Windows 11's Smart App Control blocks unsigned programs, and
> `Notarius.exe` isn't code-signed. Where Smart App Control is on, use Option A. Turning Smart App
> Control off is a **one-way switch**: Windows only lets you turn it back on by resetting or
> reinstalling Windows. Check `Windows Security > App & browser control > Smart App Control`.

### The first start

The first start downloads the speech models once, about 3 GB, so the dashboard can take a few
minutes to appear. After that Notarius starts in seconds.

## 2. First start: PIN and recovery key

1. The dashboard opens at **http://127.0.0.1:8765** and asks you to **choose a 4-digit PIN**.
   Each digit moves to the next box automatically. Enter the PIN a second time to confirm it.
2. Notarius shows your **recovery key**, for example `7K2Q-M9XD-4TRP-H8WC-2VNE-QJ6B`. **Write it on
   paper** or save it in a password manager. It is the only way back in if you forget your PIN,
   and it isn't shown again. Tick *I've written down my recovery key*, then **Continue**.
3. A short guided tour starts. Replay it any time with the **?** button.
4. Open **Settings** (gear icon) to set:
   - your name, used instead of "Me" in transcripts and action items;
   - the language people speak in your calls;
   - the language to write minutes in.

## 3. Everyday use

You don't need to do anything. Keep Notarius running; it starts with Windows.

| Tray icon | Meaning |
|---|---|
| Purple | Watching for Teams calls |
| Red | Recording a call |
| Amber | Writing minutes |
| Grey | Paused: not taking notes |

The icon is a speech bubble (the conversation) whose tail is a pen nib writing it down, with a Roman
letter N inside. The pen is the scribe's, the *notarius* the app is named after.

The tray icon is under **^** next to the clock. You can drag it onto the taskbar to keep it
visible.

- **Click** the icon to open the dashboard.
- **Right-click** it for the menu:
  - **Open dashboard**;
  - the current status;
  - **Pause note-taking**, which stops and discards a call that's being recorded;
  - **Quit Notarius**.

**When you join a call**, recording starts within about 10 seconds, whether you're muted or not.
No bot joins the call and Teams shows nothing to the other participants.

**When you leave**, Notarius waits 30 seconds to be sure the call ended, then processes it. You
get a **Minutes ready** notification:

| Call length | Minutes ready after you leave (with an NVIDIA GPU) |
|---|---|
| 2 minutes | about 45 seconds |
| 1 hour | about 2-3 minutes; speaker names follow a few minutes later |

Calls shorter than a minute, such as a mic test, are discarded.

> Let people know you're taking notes, and follow your organization's policy on recording calls.

## 4. The dashboard

Open it from the tray, the Start menu, or the Desktop shortcut. Every reload asks for your PIN.

**Calendar (left).** Days with meetings show a count. Click a day, **drag across days** to pick a
range, or use the quick ranges: Today, Yesterday, This week, Last 7 days, This month, All.

**Overview (right).** For the selected days you see:

- each meeting with its time, length, participants, a **summary** and the topics;
- **Open action items** from all those meetings, with owner and due date. Tick them off as
  they're done, and use **Show completed** to see them again;
- **Notes for the day**, a free-text box, when one day is selected;
- **Word** and **PDF** buttons that export every meeting in the selection into one document.

**Meeting page.** Click a meeting to open it.

- **People in this meeting:** who spoke and for how long. See [section 5](#5-people-and-speaker-names).
- **Minutes:** a summary, the discussion by topic, and decisions marked **Decision:**. Switch
  between **English** and **Roman Urdu** here. The first switch takes a few seconds; switching
  back is instant.
- **Action items:** a checklist.
- **Transcript:** time-stamped, colour-coded by speaker.
- **My notes:** your own notes, saved automatically and included in exports.
- **Copy minutes** to paste into Teams chat, Outlook or Word, or export to **Word** or **PDF**.

**Search** (top bar) finds any word across all minutes, transcripts and your notes.

**Pause** (top bar) does the same as in the tray. **Lock** (padlock) locks the dashboard at once.
The **moon/sun** button switches between light and dark; until you pick one, Notarius follows your
Windows setting. The **gear** opens Settings.

## 5. People and speaker names

Your own microphone is always you. Everyone else on the call is separated by voice into
**Speaker 1, Speaker 2**, and so on.

- When the conversation makes a name obvious, for example "Thanks Sara" followed by Sara
  answering, Notarius **suggests** it; the box is pre-filled and marked *Suggested from the
  conversation*.
- Type or confirm the names and click **Save names and update minutes**. The transcript and the
  minutes are rewritten with the names.
- Notarius **remembers each named voice**. In later meetings the same person is labelled
  automatically, marked *Recognized by voice*. If it guesses wrong, type the right name and
  save; the wrong voice sample is forgotten.

Separation works best with a headset and when people take turns. Heavy cross-talk can merge two
people or split one person into two.

## 6. Languages

- **Spoken language.** The default, *Detect automatically*, works for any language and for
  **mixed calls**. Each stretch of speech is transcribed in the language it's spoken in, so a call
  that moves between English and Urdu or Hindi is written down as spoken, not translated. Urdu
  and Hindi use one script per meeting, whichever Notarius heard more of. If detection gets your
  calls wrong, set a fixed language in **Settings**.
- **Minutes language.** The default is **English** or **Roman Urdu**, set in Settings, and you can
  switch any meeting on its page. Names, product names and technical terms stay in English.

## 7. Privacy and security

**What stays on your laptop:**

- the audio, which is deleted once the meeting is processed;
- the transcription and speaker separation, which run locally;
- the transcripts and minutes;
- the voice fingerprints;
- the dashboard, which is only reachable from this laptop.

**What leaves it:** the transcript text is sent to **Claude (Haiku)** through your own Claude Code
login to write the minutes. Claude Code is run so that it keeps no copy of the conversation.

**Encryption.** With a PIN set, every transcript, set of minutes, speaker list and personal note is
**encrypted on disk**. Opening the files shows unreadable data. Meetings are stored in
`%LOCALAPPDATA%\Notarius\Meetings`, not in Documents.

The encryption key is protected by your PIN *and* by your Windows account, so the files are
useless on another computer or account. New meetings are encrypted as they're saved, even while
the dashboard is locked.

**Locking.** The dashboard asks for the PIN:

- on every reload or new tab;
- after you've been away from the tab for more than 1 minute;
- after 5 minutes without activity;
- whenever Windows is locked (Win+L, sleep, switching users).

Recording is never affected.

**Limits to be aware of:**

- A 4-digit PIN stops casual access. Someone already signed in to *your* unlocked Windows account
  could, with effort, guess it offline. Lock Windows (Win+L) when you step away.
- During a call, and until it's processed, the raw audio is on disk unencrypted. It's deleted
  afterwards.
- Exported Word and PDF files are ordinary, unencrypted files.

**Forgot your PIN?** On the lock screen click **Forgot your PIN?**, enter your recovery key, and
choose a new PIN. You can create a new recovery key in **Settings**; the old one then stops
working. Without the PIN or the recovery key, the notes can't be recovered.

## 8. Troubleshooting

| Problem | What to do |
|---|---|
| A call wasn't recorded | Only the **Teams desktop app** is detected. For Teams in a browser or other apps, run `uv run --script notarius.py record` and press Ctrl+C when done. Also check that Notarius isn't **paused**. |
| Everyone else shows as "Others" | Speaker separation failed or was skipped. The minutes are still written. Check the log (below). |
| "Minutes failed" | Usually Claude Code isn't logged in. Run `claude` once in a terminal to log in, then click **Try again** on the meeting. |
| Transcription is slow | Notarius falls back to the CPU when the GPU isn't usable. Check the log for `on cpu`. |
| The dashboard doesn't open | Make sure Notarius is running (tray icon). Start it from the Start menu, then open http://127.0.0.1:8765. |
| "Too many attempts" | After 5 wrong PINs the lock screen pauses, starting at 15 seconds and doubling each time. |
| Windows blocked Notarius.exe | That's Smart App Control; use install option A. |
| Other people's words under my name | Your mic also hears the call through your speakers or headset. Notarius removes words on your mic that match the call audio at the same moment, so this should be rare. A headset with little leakage helps. |
| Something I said while muted is in the notes | Teams mute doesn't switch off your microphone, and Notarius can't read Teams' mute state yet. For a private side conversation, use **Pause** in the tray or dashboard. |
| The same person appears as two speakers | Give both the same name in the **People** tab; they're merged, and the voice is remembered. |

The log is at `%LOCALAPPDATA%\Notarius\notetaker.log`. It records events and timings, never what
was said.

## 9. Uninstall

Right-click the tray icon and choose **Quit Notarius**, then run:

```powershell
uv run --script notarius.py uninstall
```

This removes the shortcuts and the login item. Your meetings stay in
`%LOCALAPPDATA%\Notarius\Meetings`. Delete that folder to remove them. The models are in
`%LOCALAPPDATA%\Notarius\models`.
