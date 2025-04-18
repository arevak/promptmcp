# prompt-library

A CLI application to create, manage, and serve prompt templates following the MCP JSON structure.

## Installation

Requires Python >=3.13

```bash
pip install .
# or for development
pip install -e .
```

## Usage

The CLI is installed as `promptmcp` via the entry point.

### Create a new prompt

```bash
promptmcp create <promptkey> <description> [--dir DIR]
```

- `<promptkey>`: unique name for the prompt
- `<description>`: human-readable description
- `--dir DIR`: optional directory to store prompt JSON files (default `~/.promptmcp`)

Example:

```bash
promptmcp create hello_name "Say Hello to $name"
> Paste your prompt template: Hello, ${name}
```

This creates `~/.promptmcp/hello_name.json`:

```json
{
    "name": "hello_name",
    "description": "Say Hello to $name",
    "arguments": [
        { "name": "name", "required": true }
    ]
}
```

### Serve prompts via HTTP API

```bash
promptmcp serve [--dir DIR]
```

Runs a FastAPI server on `http://0.0.0.0:8000`, serving prompts from the specified directory.

+ #### Alternative: serve with uvicorn CLI
+
+ You can serve the ASGI app directly using uvicorn (the module exports `app`):
+
+ ```bash
+ # via python -m uvicorn
+ python -m uvicorn prompt_library.main:app --reload --host 0.0.0.0 --port 8000
+
+ # via uvicorn
+ uvicorn prompt_library.main:app --reload --host 0.0.0.0 --port 8000
+
+ # alias `uv` if installed
+ uv run prompt_library.main:app --reload --host 0.0.0.0 --port 8000
+
+ # alias `uvx` if available
+ uvx prompt_library.main:app --reload --host 0.0.0.0 --port 8000
+ ```

#### Endpoints

- `GET /prompts` - list all prompts
- `GET /prompts/{prompt_name}` - get a specific prompt by name

## Testing

Run the integration tests:

```bash
pytest
```

## Linting

Use [ruff](https://github.com/charliermarsh/ruff) for linting:

```bash
ruff .