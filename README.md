# genai_4_dps_helper
Common functions for the GenAI 4 DPS Course

### Instructions for deploymet
https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/

### VS Code settings.json for _ruff_ config
```
{
    "notebook.formatOnSave.enabled": true,
    "notebook.codeActionsOnSave": {
        "notebook.source.organizeImports": "explicit"
    },
    "[python]": {
        "editor.formatOnSave": true,
        "editor.defaultFormatter": "charliermarsh.ruff",
        "editor.codeActionsOnSave": {
            "source.organizeImports": "explicit"
        }
    }
  }
  ```