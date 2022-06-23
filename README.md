# scripts_and_dotfiles
This repository contains scripts and dotfiles that I use in my MacOS setup.

## Scripts
* `safari` and `chrome`: interact with web browsers. See https://github.com/antoniolanza1996/openSafariFromTerminal for other details.
* `remind`: create a new reminder in Apple Reminders.
* `search`: search text on all files of a directory (or a single file).
* `italian_covid_stats.py`: show daily Italian Covid-19 data.

## Dotfiles
Dotfiles are handled with [Dotbot](https://github.com/anishathalye/dotbot). So, new additions can be done as follows:
```bash
cd dotfiles
nano install.conf.yaml # and add new links
./install
```