# Python Project Setup with `uv` and Virtual Environment

This project uses [`uv`](https://github.com/astral-sh/uv) to create and manage a Python virtual environment for faster and more efficient package handling.

## Prerequisites

- Python 3.8+
- [`uv`](https://github.com/astral-sh/uv) installed

You can install `uv` via:

1.  using pip
    ```bash
    pip install uv
    ```    

2. using curl
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

3. using cargo
    ```bash
    cargo install uv
    ```

1. Setting Up the Environment
To set up and activate the virtual environment using uv:

```bash
uv venv
source .venv/bin/activate

or .venv/Scripts/activate
```

2. Install dependencies via requirements.txt

```bash
uv pip install -r requirements.txt
```

3. Run the project via

for CLI
```bash
python main.py
```

for GUI

```bash
python gui/main_gui.py
```