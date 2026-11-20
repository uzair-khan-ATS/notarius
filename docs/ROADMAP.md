# Roadmap

## Done (v1)

- Records Teams desktop calls automatically and transcribes them locally on the GPU, in any
  language, including mixed English/Urdu/Hindi calls.
- Speaker separation, with names remembered by voice.
- Minutes, action items, and English or Roman Urdu minutes.
- Calendar dashboard, search, and Word/PDF export.
- PIN lock, recovery key, encryption at rest, and a tray app.

## Next (in priority order)

1. **Respect Teams mute (top priority).** Teams mute doesn't switch off the microphone device, so
   today Notarius still records and transcribes you while you're muted, including private side
   conversations. Planned flow:
   - While recording, follow Teams' mute state. The Teams third-party app API, on a local
     WebSocket that Teams exposes when it's enabled in Teams settings, reports `isMuted` in its
     meeting updates. Notarius pairs with it once and logs a muted/unmuted timeline next to the
     audio.
   - When processing, words on your mic that fall inside a muted stretch are left out of the
     transcript, the minutes and your talk time, the same way echo is removed today. The call
     audio from everyone else is unaffected.
   - If Teams' API isn't available, fall back to today's behaviour, and tell you so on the
     meeting page, so nothing is silently lost.
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
