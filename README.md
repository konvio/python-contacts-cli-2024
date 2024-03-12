# Notes & Contacts CLI Application

This is a command-line interface (CLI) application written in Python.

## Prerequisites

- Python 3.11+
- Poetry

## Installation

```bash
pip install contacts24
python -m contacts24

### From source code

```bash
git clone https://github.com/konvio/python-contacts-cli-2024
cd python-contacts-cli-2024
poetry config virtualenvs.in-project true --local
poetry env use 3.11
poetry install
poetry run python main.py
