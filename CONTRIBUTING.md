# Plugin Development Guide

Each plugin must contain a main Python file that follows these requirements to ensure it can be discovered and executed properly by the system.

## Folder Structure

Each plugin must live in `omnisect/omnisect/plugins/plugins/{your_plugin}/`.

## ✅ Required Components

1. Plugin Class

The main class must:

- Inherit from IPlugin
- Define a constructor **init**(self, logger) to receive a logger instance
- Implement the invoke(...) method — this is the main entry point for your plugin's logic

```python
from plugins.core.iplugin import IPlugin
from plugins.models import Meta

class SamplePlugin(IPlugin):
    def __init__(self, logger):
        super().__init__(logger)
        self.meta = Meta(
            name="Sample Plugin",
            description="sample plugin template",
            version="1.1.1",
            web_id="sfjt6uvQon7xnrXtuuBVxzZYKjIRSexl",  # generated via https://shortunique.id/
        )

    def invoke(self, text: str):
        # Your plugin logic here
        return text.upper()

```

2. File Declaration

The plugin’s main file must be declared in the plugin’s config.yaml:

```yaml
name: "Sample Plugin"
alias: "sample-plugin"
creator: "bl1nkker"
# here
runtime:
  main: "main.py"
repository: "https://github.com/bl1nkker/sample-plugin"
description: "Sample plugin template"
version: "1.1.1"
requirements:
  - name: "tqdm"
    version: "4.48.0"
  - name: "six"
    version: "1.17.0"
```

3. You May Add Additional Files

You can include as many additional files, modules, or helpers as needed within your plugin directory.
Only two things are strictly required:

- A valid config.yaml
- A main Python file (like main.py) with a class implementing the IPlugin interface

## 🚫 What Not to Do

    ❌ Do not import code from other plugins
    ❌ Avoid using global state unless absolutely necessary
    ❌ Do not leave out the invoke() method — it’s mandatory

## 📂 Example Plugin Directory Structure

```arduino
plugins/
└── plugins/
└── my_plugin/
├── config.yaml # required
├── main.py # required (declared in config)
├── helpers.py # optional
└── README.md # optional
```
