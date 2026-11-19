# notetaker

Local note-taker for Microsoft Teams meetings. No bot joins the call. Audio, transcripts and
notes stay on your machine. The only thing sent out is the transcript text, which goes to your
own Claude Code (Haiku) to write the minutes.

1. **Detects the call.** Teams opens its call-audio stream when you join and holds it until you
   leave, whether you're muted, unmuted, or have no mic.
2. **Records two tracks.** Your mic (**Me**) and the call audio from the headset or speaker
   Teams is using (**Others**).
3. **Transcribes.** When you leave, faster-whisper transcribes locally on the GPU, falling back
   to the CPU. Raw audio is deleted afterwards.
4. **Writes the minutes.** `claude -p --model haiku` writes **Minutes of Meeting** (topics,
   decisions) and an **Action Items** table (action, owner, due date).
5. **Dashboard.** A local calendar at <http://127.0.0.1:8765> lists your meetings by day.
   Pick a day or a range of days to see the meetings, read the minutes and transcript, and keep
   your own notes per meeting and per day.

Each meeting lands in `~/Documents/MeetingNotes/<date_time>/`: `notes.md`, `transcript.md`,
`my_notes.md`, and `meta.json`. Day notes are in `_days/<date>.md`.

## Requirements

- Windows 10/11 and the new Teams desktop app
- [uv](https://docs.astral.sh/uv/). It installs Python and all dependencies on first run.
- [Claude Code](https://claude.com/claude-code) CLI, logged in (`claude` on PATH)
- An NVIDIA GPU is optional. Without one, transcription runs on the CPU, which is slower.

## Run

```powershell
git clone https://github.com/uzair-khan-ATS/teams-notetaker; cd teams-notetaker
uv run --script notetaker.py watch       # or double-click start-notetaker.cmd; leave it running
uv run --script notetaker.py dashboard   # open the dashboard (watch already serves it)
uv run --script notetaker.py status      # during a call: confirms Teams is detected
uv run --script notetaker.py record      # manual start/stop (Teams in a browser, other apps)
uv run --script notetaker.py process "<meeting folder>"   # redo transcript + minutes
```

The first run downloads the GPU libraries (~1.2 GB) and the Whisper model (~1.6 GB) once.

Timing on an RTX 4050 laptop: transcription runs at about 15x real time. A one-hour meeting is
ready about 4-6 minutes after you leave; Haiku takes about 20 seconds of that. CPU-only takes
roughly 15-30 minutes.

To start automatically at login (minimized), run this from the repo folder:

```powershell
$s = (New-Object -ComObject WScript.Shell).CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\notetaker.lnk")
$s.TargetPath = "$PWD\start-notetaker.cmd"; $s.WorkingDirectory = "$PWD"; $s.WindowStyle = 7; $s.Save()
```

## Settings (env vars)

| var | default | |
|---|---|---|
| `NOTETAKER_CLAUDE_MODEL` | `haiku` | model for the minutes |
| `NOTETAKER_MODEL` | `large-v3-turbo` | Whisper model; `small` is faster and lighter but less accurate |
| `NOTETAKER_LANG` | auto | force a language, e.g. `en` |
| `NOTETAKER_DIR` | `~/Documents/MeetingNotes` | output folder |
| `NOTETAKER_PORT` | `8765` | dashboard port (bound to 127.0.0.1 only) |
| `NOTETAKER_KEEP_AUDIO` | off | `1` keeps the WAVs |

## Limits

- Individual remote speakers aren't separated. Everyone else is "Others", and Claude names
  people only where the conversation makes it clear.
- Use a headset. On laptop speakers the mic also picks up the others, which produces duplicate text.
- Switching audio devices mid-call isn't followed. The recording stays on the device the call started on.
- Let people know you're taking notes, and check your company's policy on recording.
