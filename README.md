<p align="center"><img src="assets/logo.svg" width="96" alt="Notarius logo: a white speech bubble on a purple tile, holding a Roman capital N whose right leg is a pen nib"></p>

<h1 align="center">Notarius</h1>

<p align="center"><b>Minutes of your Microsoft Teams meetings, taken on your own laptop.</b><br>
Named after the <i>notarii</i>, the scribes of ancient Rome who wrote down every word said in a meeting.</p>

Notarius runs in the Windows tray. When you join a Teams call it starts recording; when you leave,
it transcribes the call on your laptop and writes **minutes of meeting with action items**. No bot
joins the call, and nobody has to send you the transcript.

- **Starts on its own.** It detects the Teams call audio, so it works whether you're muted or not.
- **Fast, local transcription.** faster-whisper runs on your NVIDIA GPU, transcribing an hour of
  audio in about a minute. It falls back to the CPU if there's no GPU.
- **Any language, including mixed calls.** It detects the language of each stretch of speech, so
  a call that moves between English and Urdu or Hindi is written down as spoken. Minutes can be in
  **English or Roman Urdu**.
- **Knows who said what.** Voices on the call are told apart (Speaker 1, Speaker 2, and so on).
  Claude suggests names from the conversation, and once you name a voice it's recognized in later
  meetings.
- **Minutes and action items.** Each meeting gets a summary, discussion by topic with decisions,
  and an action-items table with owner and due date. A one-hour meeting is ready a few minutes
  after you leave.
- **Calendar dashboard** at http://127.0.0.1:8765:
  - pick a day or drag across a range to see its meetings and open action items;
  - tick action items off as they're done;
  - keep notes per meeting and per day;
  - search everything;
  - export to **Word** or **PDF**;
  - take a guided tour with the **?** button.
- **Private by default.** A **4-digit PIN** locks the dashboard. Notes and transcripts are
  **encrypted on disk** and stored in the app's private folder, not in Documents. A **recovery key**
  resets a forgotten PIN.

The only thing that leaves your laptop is the transcript text, which goes to your own Claude Code
(Haiku model) to write the minutes.

## Install

You need:

- Windows 10 or 11, and the new Teams desktop app.
- [uv](https://docs.astral.sh/uv/getting-started/installation/).
- [Claude Code](https://claude.com/claude-code), logged in.
- An NVIDIA GPU is optional but recommended.

```powershell
git clone https://github.com/uzair-khan-ATS/notarius
cd notarius
uv run --script notarius.py install
```

This adds **Notarius** to the Start menu and the Desktop and starts it at every login. Open it
once: the first start downloads the speech models (about 3 GB, one time) and opens the dashboard,
where you choose your PIN and save your recovery key. After that it works by itself.

**Quit** by right-clicking the tray icon (under **^** next to the clock) and choosing **Quit
Notarius**. The tray icon is purple while watching, red while recording, amber while writing
minutes, and grey when paused.

More documentation:

- **[User guide](docs/USER_GUIDE.md)**: install options, PIN and recovery key, the dashboard,
  languages, privacy, troubleshooting.
- **[How it works](docs/ARCHITECTURE.md)**: pipeline, encryption, API, configuration, building
  the `.exe`.
- **[Roadmap](docs/ROADMAP.md)**: Google Meet, screen-share screenshots, and what comes next.

## License

MIT
