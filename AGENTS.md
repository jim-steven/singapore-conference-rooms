# Singapore Conference Rooms - Agent Instructions

## Deployment

**Always push changes to GitHub after every modification.** This site is deployed via GitHub Pages at:
- https://jim-steven.github.io/singapore-conference-rooms/

After making any file changes, run:
```bash
git add -A && git commit -m "Description of changes" && git push origin main
```

## Project Structure

- `index.html` - Main landing page with hero, agenda, accommodation CTA, FAQs
- `accommodation.html` - Full accommodation details, POC contacts, room assignments
- `team-details.html` - Team phone numbers and booking references
- `travel.html` - Travel information and arrival times
- `itinerary.html` - Full schedule/itinerary
- `packages.html` - Conference room venues browser
- `login.html` - Password-protected entry page

## Design System

- **Fonts**: DM Serif Display (headings), Work Sans (body)
- **Colors**:
  - Primary accent: #e07b5a (coral)
  - Dark section bg: #0d1117 (FAQ section)
  - Text dark: #1a1a2e
  - Text muted: #6c757d
- **Navigation**: All "Home" links should use `index.html#top` to scroll to top

## Authentication

Pages use sessionStorage-based authentication. Check for `authenticated === 'true'` at page load.
