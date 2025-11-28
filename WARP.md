# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project overview

This is a small Python application intended to display a weather forecast panel using data from a remote weather API.

Current state:
- Single entry-point module: `main.py` at the repo root
- `main()` is a stub that only prints a placeholder message
- README describes planned separation between API client code and the presentation layer

As the project evolves, expect additional modules to appear to implement:
- HTTP client logic for talking to the remote weather API
- A presentation layer (terminal or GUI) for rendering current conditions and forecast data

## Runtime and common commands

### Runtime

- Expected language/runtime: Python 3.x

### Run the application

From the repository root:

```bash
python main.py
```

This runs the stubbed `main()` function. As more functionality is added, this should launch the panel that fetches remote weather data and renders it.

### Linting

- At this stage, there is no linter configuration or dependency file in the repo.
- If/when a linter (e.g. `ruff`, `flake8`) is added, prefer the commands documented in `README.md`, `pyproject.toml`, or other config in this repository rather than assuming defaults.

### Tests

- There is currently no test suite or test configuration in the repository.
- Once a test runner (commonly `pytest`) is introduced, typical patterns will be:
  - Run all tests:
    ```bash
    pytest
    ```
  - Run a single test function in one file:
    ```bash
    pytest path/to/test_file.py::TestClass::test_case
    ```
- Always check this repository's documentation or configuration files for the authoritative test command, as it may differ from these examples.

## Architecture and design notes

### High-level structure

- `main.py` is the entry point for the application. It should remain a thin orchestration layer that:
  - Parses any configuration or input (if added later)
  - Invokes the weather API client to fetch current conditions and forecast
  - Passes that data to a presentation layer responsible for rendering a panel (terminal or GUI)

### Intended separation of concerns

Based on the README, the project should maintain a clear separation between:
- **API client layer**: modules responsible for making HTTP requests to the remote weather API, handling authentication (if needed), error handling, and translating raw API responses into Python data structures.
- **Presentation layer**: modules responsible for displaying key information (temperature, conditions, forecast) in a terminal or GUI panel.

Future code should be organized so that:
- The API client layer does not depend on any UI libraries; it should be reusable from different frontends.
- The presentation layer consumes already-processed weather data structures and focuses only on layout and rendering.
- `main.py` wires these pieces together rather than containing substantial business logic itself.
