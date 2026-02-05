# Repository Guidelines

## Project Structure & Module Organization
- `index_ros1.html` and `index_ros2.html` are the primary slide decks (Reveal.js-based).
- `interactive_app/` contains embedded interactive comparison apps referenced by slides.
- `media/` stores images and SVG diagrams used in slides.
- `code/ros1/` and `code/ros2/` hold ROS launch/xacro snippets that are presented in the slides.
- `CLAUDE.md` documents slide intent and layout rules; treat it as the source of truth for slide design constraints.

## Build, Test, and Development Commands
This is a static HTML repository; there is no build step or package manager.
- `python3 -m http.server 8000` (from repo root) serves the slides locally.
- Open `http://localhost:8000/index_ros1.html` or `http://localhost:8000/index_ros2.html` in a browser.

## Coding Style & Naming Conventions
- HTML/CSS in this repo uses 4-space indentation and inline `<style>` blocks.
- Prefer descriptive, lowercase file names with underscores (e.g., `index_ros2.html`, `ros_control_fake_joint.drawio.svg`).
- Keep slide content in Japanese to match the existing materials.
- Avoid adding animation effects unless explicitly required; the current design favors static layouts (see `CLAUDE.md`).

## Testing Guidelines
- No automated tests are present. Validate changes manually by opening the relevant HTML files in a browser and checking layout, fonts, and embedded assets.

## Commit & Pull Request Guidelines
- Commit history shows short, imperative summaries such as “Update”, “Fix typo”, and “Add …”. Keep messages brief and action-oriented.
- For PRs, include:
  - A concise summary of slide changes and affected files (e.g., `index_ros2.html`, `media/ros_control_fake_joint.drawio.svg`).
  - Screenshots for visual changes to slides or interactive apps.
  - Any external asset/license notes if new media is added.

## Slide Design Constraints
- Backgrounds are expected to be black and layouts consistent (often image/app on the left, text on the right).
- Use Noto Sans JP and highlight.js styles already wired into the slide files.
- Keep embedded apps in `interactive_app/` and reference them via relative paths.
