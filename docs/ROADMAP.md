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

1. **Teams in Notarius.** A team is a shared space inside Notarius, like a workspace. You create
   one, add your colleagues by email, and the meetings you put in the team appear in their
   Notarius, read-only. There are no share links: only signed-in team members see anything.
   - **Create a team and add members:** in Notarius, *Teams > New team* (for example "ATS
     Engineering"), then *Add member* with their work email. They appear as *Invited* until
     they sign in.
   - **Members sign in with their email:** Notarius sends a 6-digit code to that email, and the
     invitation is waiting when they sign in. There are no passwords. Microsoft or Google
     sign-in can come later.
   - **Roles:** *Owner* (you: add and remove members, choose what's in the team) and *Member*
     (reads the team's meetings). Removing someone takes the team out of their Notarius at once.
     Later, members could tick off their own action items.
   - **Putting meetings in a team:** a *Team* picker on each meeting, or a rule such as "all my
     meetings" or "meetings with these people". By default the minutes and action items go in;
     the transcript and your own notes are opt-in, and the audio never leaves your laptop. When
     you rename speakers or tick off action items, the team sees the change.
   - **What members see:** the team in Notarius's sidebar (*Personal* and each team they're in),
     with the same meeting feed, meeting pages, action items (with *Mine*) and search. Members
     don't record anything, so they can use the Notarius app or sign in at the Notarius website
     on any computer or phone. Your laptop doesn't need to be on.
   - **How it's built:** a small hosted Notarius service for accounts, teams, membership and the
     team's meetings, which the laptop syncs to over HTTPS. Data is encrypted in transit and at
     rest and kept per team, with a log of who opened what. Later, end-to-end encryption, with
     the team key held only on members' devices so the service can't read the notes. The same
     service is the base for selling Notarius as a product.
   - **Not this:** opening your laptop's dashboard to the internet (port forwarding or tunnels).
     It only works while the laptop is on, and it exposes the PIN screen and your whole archive.
2. **Google Meet** (Chrome and Edge). Detect a Meet call from the browser's microphone and audio
   streams plus the Meet tab title; a small browser extension is the most reliable option.
3. **Teams on the web and Zoom**, detected the same way.
4. **Screen-share screenshots.** While someone shares their screen, save a frame whenever the
   content changes, such as a new slide. Show the frames next to the transcript, encrypted like
   the notes, and optionally let the minutes describe what was shown. Off by default.
5. **Meeting titles and attendees** from the Outlook calendar.
6. **Encrypted cloud backup.** Today the notes exist only on this laptop. Back them up
   automatically to cloud storage (for example OneDrive or an S3 bucket), still encrypted with
   your key, so a lost or reinstalled laptop doesn't lose your meetings. Restore with the
   recovery key.

## Later

- One-click follow-up messages with each person's action items.
- Live notes during the call.
- Better speaker separation for cross-talk.
- Custom vocabulary for project names and acronyms.
- Signed installer with auto-update, so it installs with Smart App Control on.
- An option to write the minutes with a local model, so nothing leaves the laptop.
