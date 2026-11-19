# notetaker

Local note-taker for Microsoft Teams meetings. No bot joins the call and nothing leaves the
machine except the transcript text, which goes to your own Claude Code (Haiku) for the summary.

1. Watches for a Teams call: Teams opens its call-audio stream when you join and keeps it until
   you leave, whether you're muted, unmuted, or have no mic.
2. Records two tracks: your mic (**Me**) and the call audio from the headset/speaker Teams is
   using (**Others**).
3. When you leave, transcribes locally with faster-whisper on the GPU (falls back to CPU) and
   runs `claude -p --model haiku` to write `notes.md`. Raw audio is deleted afterwards.

Output: `~/Documents/MeetingNotes/<date_time>/notes.md` and `transcript.md`.

## Requirements

- Windows 10/11 and the new Teams desktop app
- [uv](https://docs.astral.sh/uv/). It installs Python and all dependencies on first run.
- [Claude Code](https://claude.com/claude-code) CLI, logged in (`claude` on PATH)
- An NVIDIA GPU is optional. Without one, transcription runs on the CPU, which is slower.

## Run

```powershell
git clone https://github.com/uzair-khan-ATS/teams-notetaker; cd teams-notetaker
uv run --script notetaker.py watch     # or double-click start-notetaker.cmd; leave it running
uv run --script notetaker.py status    # during a call: confirms Teams is detected
uv run --script notetaker.py record    # manual start/stop (Teams in a browser, other apps)
uv run --script notetaker.py process "<meeting folder>"   # redo transcript + notes
```

The first run downloads the GPU libraries (~1.2 GB) and the Whisper model (~1.6 GB) once.

To start automatically at login (minimized), run this from the repo folder:

```powershell
$s = (New-Object -ComObject WScript.Shell).CreateShortcut("$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup\notetaker.lnk")
$s.TargetPath = "$PWD\start-notetaker.cmd"; $s.WorkingDirectory = "$PWD"; $s.WindowStyle = 7; $s.Save()
```

## Settings (env vars)

| var | default | |
|---|---|---|
| `NOTETAKER_CLAUDE_MODEL` | `haiku` | model for the notes |
| `NOTETAKER_MODEL` | `large-v3-turbo` | Whisper model; `small` is faster/lighter, less accurate |
| `NOTETAKER_LANG` | auto | force a language, e.g. `en` |
| `NOTETAKER_DIR` | `~/Documents/MeetingNotes` | output folder |
| `NOTETAKER_KEEP_AUDIO` | off | `1` keeps the WAVs |

## Limits

- Individual remote speakers aren't separated. Everyone else is "Others", and Claude names
  people only where the conversation makes it clear.
- Use a headset. On laptop speakers the mic also picks up the others, which produces duplicate text.
- Switching audio devices mid-call isn't followed. The recording stays on the device the call started on.
- Let people know you're taking notes, and check your company's policy on recording.
