# Repository Guidelines

## Project Structure & Module Organization
- `index_ros1.html` and `index_ros2.html` are the main slide decks for ROS1/ROS2.
- `interactive_app/` contains standalone HTML demos used inside slides.
- `code/ros1/` and `code/ros2/` hold example scripts (Python/C++) and ROS config (`.yaml`, `.xacro`).
- `media/` stores images and GIFs embedded in slides.
- `CLAUDE.md` is a detailed content outline and reference for the deck.

## Build, Test, and Development Commands
There is no build system in this repo. Common local workflows:
- Preview slides: open `index_ros1.html` or `index_ros2.html` in a browser.
- Local static server (optional, for relative asset loading):
  ```bash
  python3 -m http.server
  ```
  Then browse to the slide HTML file.
- ROS demos: scripts under `code/ros1/` and `code/ros2/` are educational examples. Run them inside a configured ROS1/ROS2 workspace as appropriate.

## Coding Style & Naming Conventions
- Python uses 4-space indentation and UTF-8 source headers. Keep the existing style and inline Japanese comments where present.
- C++ follows ROS2 conventions with `snake_case` for local variables and `UpperCamelCase` for types.
- Filenames are lower_snake_case (e.g., `jtc_demo.py`). Match existing naming patterns when adding new assets or demos.

## Testing Guidelines
- No automated tests are included.
- Manual checks:
  - Open the slide decks and verify image/iframe embeds render correctly.
  - If you modify a ROS demo, run it in a simulator or hardware environment to confirm behavior.

## Commit & Pull Request Guidelines
- Git history shows short, imperative subjects like `Fix typo` or `Update`. Keep commit titles brief and action-oriented.
- PRs should include:
  - A short summary of the content changed (slide numbers or section names).
  - Screenshots or GIFs when visuals or layout change.
  - Any ROS version assumptions if you touched demo code.

## Security & Configuration Tips
- Do not add secrets or credentials. This repo is static content plus sample code.
- When referencing external resources in slides, prefer stable, official documentation links.
