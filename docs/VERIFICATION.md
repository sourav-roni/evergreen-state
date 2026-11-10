# Evergreen Drive 1.0 — verification

Automated application-logic checks passed:
- 128 unique question IDs; four distinct options per question; valid source pages.
- 191 indexed PDF pages and 12 study routes.
- 20 deterministic, distinct mock forms; 40 unique questions per form.
- Every form covers all 12 routes; the forms collectively cover all 128 questions.
- Correct scoring for 0, 31, 32, and 40 correct, including unanswered questions.
- Passing boundary at 32/40; submission is idempotent.
- Saved-session JSON round-trip and correct resumption of practice bookkeeping.
- No double-counting previously graded practice answers at submission.
- Review scheduling, correct-answer streaks, and malformed-backup rejection.
- Render smoke tests for every primary view.

Browser interaction checks passed in the Codex in-app browser on localhost:
- Dashboard and study route rendering.
- Read-lesson progression and persistence after reload.
- Practice incorrect-answer feedback with the correct answer and source link.
- Protection against accidentally replacing an unfinished session.
- Mock answer selection, flagging, persistence on reload, unanswered submission
  warning, scoring, full answer review, and missed-only filtering.
- Flashcard reveal, explanation, source, rating, and next-card progression.
- Offline text search (school bus) returned source-page matches.
- Original PDF sign atlas images render legibly.
- Progress export created a JSON file in Downloads; importing that file displayed
  a confirmation and restored progress. The browser automation download event
  timed out, but the actual downloaded file was verified and successfully imported.
- Sound toggle activated without JavaScript errors (audible output not assessed).
- Desktop (1280-wide) and narrow (390-wide) layouts visually reviewed. At 390,
  document width and scroll width were both 390: no page-level horizontal overflow.
- No JavaScript error logs during the tested flows.

Limits:
- Browser automation disallows file:// navigation, so visual testing used an
  approved localhost preview. Direct double-click execution was not browser-tested.
  Static audit confirms ordinary deferred scripts, relative assets, and no fetch,
  module imports, CDN fonts, service worker, or server API dependency.
- Cross-browser behavior in installed Chrome, Firefox, Safari, and Edge was not
  separately tested. Browser storage persistence on file URLs is browser-dependent;
  backups and a visible storage-failure message are provided.
- Practice content reflects the supplied guide edition; no claim of access to
  actual DOL questions, official topic weighting, or guaranteed test readiness.
