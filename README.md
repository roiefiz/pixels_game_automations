# pixels_game_automations

`pixels_game_automations` is a browser and desktop automation project for the game Pixels. It combines Selenium browser control, PyAutoGUI screen automation, image/color-based interactions, and account-loop orchestration.

This is not a packaged application. It is a personal automation codebase with hardcoded coordinates, local file assumptions, and machine-specific behavior.

## What Is In This Repo

- `main.py`: the main automation implementation, including the `PixelsUser` class and most gameplay helpers
- `run.py`: a loop runner that pulls account names from a remote endpoint and executes farming/buying/selling flows across accounts

There is no `requirements.txt`, `pyproject.toml`, or `README.md` in the original project state.

## Current State

The project is script-based and strongly tied to one operator’s machine and UI layout.

- coordinates are hardcoded for a specific screen/layout
- automation relies on desktop control, browser control, and pixel/color detection
- several local text files are expected but are not present in the repo
- there is no config layer for accounts, screen geometry, or secrets

## Main Module

### `main.py`

This file contains the actual automation logic.

Key pieces include:

- `generate_random_username()`
- `keyboard_move_figure(...)`
- `PixelsUser`

The `PixelsUser` class includes methods for:

- account creation
- logging into existing accounts
- reading game state from the UI
- detecting energy and berry balances
- going to farms
- buying and selling goods
- interacting with inventory
- recording errors
- performing farming loops

The file mixes:

- Selenium page automation
- PyAutoGUI mouse/keyboard automation
- image/color heuristics
- Gmail-style email notification helpers

### `run.py`

This is the closest thing to the main runner.

It currently:

- fetches account names from `https://roiefiz.pythonanywhere.com/accounts`
- loops over returned accounts
- creates a Chrome driver per account
- logs in through `PixelsUser.start_game_with_existing_account()`
- decides what seeds to buy based on farming level
- sells produced goods
- runs farming actions on a target farm
- writes progress lines to `running_accounts.text`

## Local Files Expected By The Code

The scripts refer to several files that are not checked into this repo:

- `accounts.text`
- `new_accounts.txt`
- `running_accounts.text`

The code will create or append to some of them during execution.

## Dependencies

There is no dependency manifest, but from imports the project currently needs at least:

- `selenium`
- `pyautogui`
- `Pillow`
- `httpx`

Standard-library modules used include `datetime`, `random`, `string`, `ssl`, `smtplib`, and the email MIME helpers.

You will also need:

- Chrome installed
- a matching ChromeDriver or compatible Selenium setup
- desktop permissions that allow screen capture and mouse/keyboard automation

## Platform Assumptions

This code is not generic cross-platform automation. It contains specific assumptions about:

- screen resolution
- UI scaling
- browser placement
- OS-specific keybindings
- macOS versus Windows coordinate/color handling

`main.py` includes a large `my_own_macbook_locations` mapping and branches on `operation_system`, which makes it clear that calibration matters.

## Running It Locally

There is no safe one-command setup, but the current intended flow appears to be:

1. ensure Selenium/Chrome/PyAutoGUI/Pillow/httpx are installed
2. make sure the machine resolution and game layout match the expected coordinates
3. provide the local text files the scripts expect
4. run `run.py`

In practice, anyone trying to use this should first calibrate the coordinate map and inspect the methods in `PixelsUser`.

## Risks And Limitations

This project is fragile by design because it automates a live game UI.

Known risks:

- UI updates can break selectors or coordinate assumptions
- screen scaling changes can break clicks
- color heuristics can fail with graphics changes
- unattended desktop automation can misclick outside the game window
- account looping depends on a remote account source endpoint

## Suggested Cleanup

If you plan to continue developing this repo, the most useful improvements would be:

1. add `requirements.txt`
2. move coordinates and OS settings into a config file
3. isolate Selenium, PyAutoGUI, and notification concerns into separate modules
4. document the required screen resolution and browser setup
5. add dry-run/debug modes for coordinate calibration
6. replace wildcard imports in `run.py`

## Summary

This repository is a game automation workspace centered on the `PixelsUser` class in `main.py` and the multi-account farming loop in `run.py`. It is comprehensive in terms of automation logic, but it is highly environment-specific and should be treated as a personal automation project rather than a portable application.
