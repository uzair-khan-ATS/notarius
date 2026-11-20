# Roadmap

## Done

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

1. **Encrypted cloud backup.** Today the notes exist only on this laptop. Back them up
   automatically to cloud storage (for example OneDrive or an S3 bucket), still encrypted with
   your key, so a lost or reinstalled laptop doesn't lose your meetings. Restore with the
   recovery key.
2. **Its own app window instead of a browser tab.** Opening Notarius shows the dashboard in a
   window with the Notarius icon and its own taskbar entry, like any Windows app. Options: a native
   window with the built-in Edge WebView2 (for example pywebview), or Edge's app mode
   (`msedge --app=...`) as a quick first step.
3. **Google Meet** (Chrome and Edge). Detect a Meet call from the browser's microphone and audio
   streams plus the Meet tab title; a small browser extension is the most reliable option.
4. **Teams on the web and Zoom**, detected the same way.
5. **Screen-share screenshots.** While someone shares their screen, save a frame whenever the
   content changes, such as a new slide. Show the frames next to the transcript, encrypted like
   the notes, and optionally let the minutes describe what was shown. Off by default.
6. **Meeting titles and attendees** from the Outlook calendar.

## Later

- One-click follow-up messages with each person's action items.
- Live notes during the call.
- Better speaker separation for cross-talk.
- Custom vocabulary for project names and acronyms.
- Signed installer with auto-update, so it installs with Smart App Control on.
- Opt-in sharing of minutes to a Teams channel or OneNote.
- An option to write the minutes with a local model, so nothing leaves the laptop.
