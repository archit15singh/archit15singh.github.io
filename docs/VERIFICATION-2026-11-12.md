# Production verification — 12 November 2026

Native Brave computer use against https://archit15singh.github.io/.

## Confirmed and fixed

- Contact and Projects rendered unstyled. Console showed 404 for a deleted fingerprinted CSS asset referenced by cached HTML. PR #29 restores recent CSS/JS versions and retains immutable assets across deployments. Production Contact was retested by clicking “Discuss this work” from an article and rendered correctly.
- Homepage repeated the name in the navigation and introduction. PR #27 changes the homepage navigation label to Home; fresh production mobile view confirms it.
- At 400px, Contact and Search were hidden beyond a horizontally scrolling navigation row. Follow-up wraps the navigation instead.

## Interaction coverage

- Header navigation: Research, Projects, Writing/archive, Speaking, About, Contact, Search. Pages scrolled and inspected in production.
- Search: typed memory with real keyboard input, observed results, opened the architecture article.
- Article: Listen entered Reading state; Stop returned it to idle. Audio state verified; full narration accuracy not audited.
- Table of contents: clicked Decision 2, observed matching URL fragment and heading scroll.
- Article footer: inspected related reading, previous/next controls and footer. Clicked Discuss this work to Contact.
- Speaking: photos and sketch-note rendered. Embedded YouTube played with visible captions, then was paused. No invitation sent.
- Archive: opened all 17 listed posts, scrolled an interior section and toward the footer, then returned using browser Back. This is layout/navigation coverage, not a line-by-line factual review or a click on every external citation.
- Homepage: observed project diagrams, questions and introduction at desktop and 400px. Theme toggle rendered both light and dark modes. Responsive navigation fix requires post-deployment retest.

## Remaining coverage

Homepage project and question links, pagination, primary external links, RSS, narrow navigation after its fix, and keyboard skip/focus. Hundreds of external article citations and third-party account flows are outside the completed UI coverage; do not report them as tested. No email, social post or sharing action was sent.
