[Instructors gihub repo] (https://github.com/nordquant/mcp-course)

### Environment setup
We will use UV as package manager for Python 
```
pip install uv
```

- To collect all dependencies used in venv
```
pip freeze > requirements.py
```

- To create virtual env with uv
```
uv virtualenv .venv
```

We will use pyproject.toml to specify dependencies.

- To install dependencies:
```
uv sync
```
