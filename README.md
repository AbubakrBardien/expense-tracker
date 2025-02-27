# Expense Tracker

The Expense Tracker is in South African Rands \(R\).

![Screenshot](expense_tracker_screenshot.png)

## Installation

Python is obviously required, since this is a python application. It is highly recommended to use a Python Virtual Environment, like `virtualenv` for example.\
For Windows: `pip install virtualenv`\
For Linux: `pipx install virtualenv` (Install `pipx` with your package manager if you haven't already)

### Create Python Virtual Environment:
After cloning the repository, first go into the project folder to create the virtual environment.

Windows:
```cmd
virtualenv .venv
.venv\Scripts\activate
```

Linux:
```bash
virtualenv .venv
source .venv/bin/activate
```

### Install Dependencies:
```bash
pip install -r requirements.txt
```

Then run the 'main\.py' file: `python main.py`
