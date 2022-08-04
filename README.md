## Requirement

- [python 3.8](https://www.python.org/downloads)

```bash
# check requirement
python --version

# install pipenv
pip install pipenv
```

## How to develop with VSCode?

```js
# .vscode/settings.json
{
  "python.formatting.provider": "autopep8",
  "python.formatting.autopep8Args": [
    "--max-line-length=200",
    "--ignore", "E402"
  ],
  "terminal.integrated.env.linux": {
    "PYTHONPATH": "${workspaceFolder}/src:${env:PYTHONPATH}"
  },
  "terminal.integrated.env.osx": {
    "PYTHONPATH": "${workspaceFolder}/src:${env:PYTHONPATH}"
  },
  "terminal.integrated.env.windows": {
    "PYTHONPATH": "${workspaceFolder}/src;${env:PYTHONPATH}"
  },
  "search.exclude": {
    "**/.git": true,
    "**/node_modules": true,
    "**/bower_components": true,
    "**/tmp": true,
    "**/.venv": true
  },
  "files.exclude": {
    // "**/*.pyc": {
    //   "when": "$(basename).py"
    // },
    "**/__pycache__": true,
  }
}
```

#### Create venv

https://code.visualstudio.com/docs/python/environments

```bash
# macOS/Linux
# You may need to run sudo apt-get install python3-venv first
python3 -m venv .venv

# Windows
python -m venv .venv
# You can also use py -3 -m venv .venv
```

#### Select interpreter

In VScode Status Bar, select interpreter to <span style="color:red">{root folder}/.venv/Scripts/python.exe</span>

```bash
# installs packages
pipenv sync
# update packages
pipenv update
# update specific package
pipenv update pandas
```

## Testing

```bash
# Run test Engine
pytest -c ./pytest.ini -s ./tests/test_api.py -n 2

pytest --cov-report xml:test-report.xml --cov-report html:cov.html --cov=src unittests/
```
