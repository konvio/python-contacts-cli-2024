# Contacts24

Contacts24 is a command-line interface for managing your contacts.

## Requirements

- Python 3.11
- Poetry

## Installation

You can install Contacts24 directly from PyPI:

```bash
pip install contacts24 --upgrade
python -m contacts24
```

## Installation from Source Code

If you want to run Contacts24 from the source code, you can clone the repository and set up a Poetry environment:

### Clone the repository

```bash
git clone https://github.com/konvio/python-contacts-cli-2024
cd python-contacts-cli-2024
```

### Configure Poetry

```bash
poetry config virtualenvs.in-project true --local
poetry env use 3.11
```

### Install dependencies and run the program

```bash
poetry install
poetry run python main.py
```
