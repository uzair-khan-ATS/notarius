# Roadmap

## Done

- **Its own app window.** Notarius opens in a window with its icon and taskbar button (Edge
  WebView2), like any Windows app, and installs like one: Settings > Apps entry, uninstaller,
  version details on the .exe. Word and PDF exports carry the Notarius logo and branding.
- **Teams mute and speaker names.** While recording, Notarius reads the Teams meeting window: the
  mic button (anything your mic hears while you're muted is left out) and the live captions (who
  is speaking). Captions are turned on automatically.
- Records Teams desktop calls automatically and transcribes them locally on the GPU, in any
  language, including mixed English/Urdu/Hindi calls.
- Speaker separation, with names remembered by voice.
- Minutes, action items, and English or Roman Urdu minutes.
- Calendar dashboard, search, and Word/PDF export.
- PIN lock, recovery key, encryption at rest, and a tray app.

## Next (in priority order)

1. **Google Meet** (Chrome and Edge). Detect a Meet call from the browser's microphone and audio
   streams plus the Meet tab title; a small browser extension is the most reliable option.
2. **Teams on the web and Zoom**, detected the same way.
3. **Screen-share screenshots.** While someone shares their screen, save a frame whenever the
   content changes, such as a new slide. Show the frames next to the transcript, encrypted like
   the notes, and optionally let the minutes describe what was shown. Off by default.
4. **Meeting titles and attendees** from the Outlook calendar.
5. **Encrypted cloud backup.** Today the notes exist only on this laptop. Back them up
   automatically to cloud storage (for example OneDrive or an S3 bucket), still encrypted with
   your key, so a lost or reinstalled laptop doesn't lose your meetings. Restore with the
   recovery key.

## Later

- One-click follow-up messages with each person's action items.
- Live notes during the call.
- Better speaker separation for cross-talk.
- Custom vocabulary for project names and acronyms.
- Signed installer with auto-update, so it installs with Smart App Control on.
- Opt-in sharing of minutes to a Teams channel or OneNote.
- An option to write the minutes with a local model, so nothing leaves the laptop.
