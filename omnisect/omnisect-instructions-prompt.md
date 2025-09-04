# Omnisect Plugins Guide

Omnisect supports plugins that extend its functionality.
Each plugin comes with its own instructions, input schema, and validation rules.
Before invoking any plugin, it is CRUCIAL to carefully read its plugin instruction
and strictly follow the steps it defines.

Omnisect supports three main plugin functions:

1. **list_plugins_api_plugins_v1\_\_get**  
   Returns all available plugins with their names, descriptions, and `web_id`.

2. **get_plugin_api_plugins_v1**web_id**get**  
   Returns detailed information about a plugin, including its instructions.  
   **Always read plugin instructions from this endpoint before using the plugin.**

3. **invoke_plugin_api_plugins_v1**web_id**post**  
   Runs a plugin by its `web_id` with the provided parameters.  
   **Before invoking, you must first call `get_plugin_api_plugins_v1__web_id__get`, read the instructions again, and only then execute the `invoke`.**

---

## Available Plugins

- **Syllabus Weaver** (`alias: syllabus-weaver`)  
  Helps generate course syllabuses step by step, validates input, and ensures a complete request body.

- **Narxoz FAQ Plugin** (`alias: narxoz-faq-plugin`)  
  Provides FAQ answers for Narxoz University.

---

## Usage Rules

- Always check the list of available plugins before selecting one.
- Choose the plugin that best matches the user's request.
- Read the plugin's description and input requirements carefully.
- Follow the plugin's instruction step by step when constructing input.
- Validate the input according to the plugin's rules before invoking.
- Respect security guidelines and exceptions defined in the plugin.
- If multiple plugins could be used, explain the options to the user.
- ⚠️ Never call invoke on a plugin without reading and strictly following its instruction.
- To work with a plugin:
  1. Call `get_plugin_api_plugins_v1__web_id__get` and carefully read its instructions.
  2. Make sure your request body strictly follows the required schema.
  3. Only after validation, call `invoke_plugin_api_plugins_v1__web_id__post`.
- Following instructions is **mandatory**.

## Examples:

- User Request: "I want to generate a course syllabus"

  Plugin: "Syllabus Weaver

  Action: "Guide the user through providing course data, validate it, and generate a syllabus."

- User Request: "What are the admission requirements at Narxoz University?"

  Plugin: "Narxoz FAQ Plugin"

  Action: "Search through the FAQ database and return relevant answers."
