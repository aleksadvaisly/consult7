# Consult7 MCP Server

**Consult7** is a Model Context Protocol (MCP) server that enables AI agents to consult large context window models for analyzing extensive file collections - entire codebases, document repositories, or mixed content that exceed the current agent's context limits. Supports providers *Openrouter*, *OpenAI*, and *Google*.

## Why Consult7?

When working with AI agents that have limited context windows (like Claude with 200K tokens), **Consult7** allows them to leverage models with massive context windows to analyze large codebases or document collections that would otherwise be impossible to process in a single query.

## ✨ New Features

- **🔧 Advanced Model Configuration**: URL-style parameters (`model?thinking=true&temperature=0.8`)
- **🧠 Thinking Mode Control**: Fine-tune reasoning with custom budgets
- **🌡️ Temperature Settings**: Control creativity vs precision
- **⚙️ Environment Variables**: Global defaults with `CONSULT7_DEFAULT_TEMPERATURE`
- **🔄 Backward Compatible**: Legacy `|thinking` format still works

> "For Claude Code users, Consult7 is a game changer."

## How it works

**Consult7** recursively collects all files from a given path that match your regex pattern (including all subdirectories), assembles them into a single context, and sends them to a large context window model along with your query. The result of this query is directly fed back to the agent you are working with.

## Example Use Cases

### Summarize an entire codebase
* **Query:** "Summarize the architecture and main components of this Python project"
* **Pattern:** `".*\.py$"` (all Python files)
* **Path:** `/Users/john/my-python-project`

### Find specific method definitions

* **Query:** "Find the implementation of the authenticate_user method and explain how it handles password verification"
* **Pattern:** `".*\.(py|js|ts)$"` (Python, JavaScript, TypeScript files)
* **Path:** `/Users/john/backend`

### Analyze test coverage
* **Query:** "List all the test files and identify which components lack test coverage"
* **Pattern:** `".*test.*\.py$|.*_test\.py$"` (test files)
* **Path:** `/Users/john/project`

### Complex analysis with thinking mode
* **Query:** "Analyze the authentication flow across this codebase. Think step by step about security vulnerabilities and suggest improvements"
* **Pattern:** `".*\.(py|js|ts)$"`
* **Model:** `"gemini-2.5-flash?thinking=true&temperature=0.3"`
* **Path:** `/Users/john/webapp`

## Installation

### Claude Code

Simply run:

```bash
# OpenRouter
claude mcp add -s user consult7 uvx -- consult7 openrouter your-api-key

# Google AI
claude mcp add -s user consult7 uvx -- consult7 google your-api-key

# OpenAI
claude mcp add -s user consult7 uvx -- consult7 openai your-api-key
```

### Claude Desktop

Add to your Claude Desktop configuration file:

```json
{
  "mcpServers": {
    "consult7": {
      "type": "stdio",
      "command": "uvx",
      "args": ["consult7", "openrouter", "your-api-key"]
    }
  }
}
```

Replace `openrouter` with your provider choice (`google` or `openai`) and `your-api-key` with your actual API key.

No installation required - `uvx` automatically downloads and runs consult7 in an isolated environment.


## Command Line Options

```bash
uvx consult7 <provider> <api-key> [--test]
```

- `<provider>`: Required. Choose from `openrouter`, `google`, or `openai`
- `<api-key>`: Required. Your API key for the chosen provider
- `--test`: Optional. Test the API connection

The model is specified when calling the tool, not at startup. The server shows example models for your provider on startup.

### Model Configuration

Consult7 supports two formats for model configuration:

#### **New URL Query Format (Recommended):**
```bash
model-name?parameter=value&parameter2=value2
```

#### **Legacy Format (Still Supported):**
```bash
model-name|parameter|parameter2
```

### Supported Parameters

| Parameter | Description | Example |
|-----------|-------------|---------|
| `thinking=true` | Enable thinking/reasoning mode | `?thinking=true` |
| `budget=N` | Set thinking token budget (auto-enables thinking) | `?budget=25000` |
| `temperature=N` | Set model temperature (0.0-2.0) | `?temperature=0.3` |
| `context=N` | Set context length (OpenAI only, supports `k` suffix) | `?context=500k` |

### Model Examples

#### Google AI
```bash
# Standard models
"gemini-2.5-flash"
"gemini-2.5-flash-lite-preview-06-17" 
"gemini-2.5-pro"
"gemini-2.0-flash-exp"

# With thinking mode
"gemini-2.5-flash?thinking=true"
"gemini-2.5-flash?thinking=true&budget=25000"
"gemini-2.5-pro?thinking=true&temperature=0.3"

# Legacy format
"gemini-2.5-flash|thinking"
```

#### OpenRouter
```bash
# Standard models
"google/gemini-2.5-pro"
"anthropic/claude-sonnet-4"
"openai/gpt-4.1"

# With reasoning mode
"anthropic/claude-sonnet-4?thinking=true"
"anthropic/claude-sonnet-4?thinking=true&budget=30000"
"google/gemini-2.5-flash?thinking=true&temperature=0.8"

# Legacy format
"anthropic/claude-sonnet-4|thinking"
```

#### OpenAI
```bash
# Standard models (context required)
"gpt-4?context=500k"
"o3-2025-04-16?context=200k"

# With thinking mode (o-series only)
"o1-mini?context=128k&thinking=true"
"o3-2025-04-16?context=200k&thinking=true&temperature=0.2"

# Legacy format
"gpt-4|500k|thinking"
```

### Environment Variables

You can control default behavior with environment variables:

```bash
export CONSULT7_DEFAULT_TEMPERATURE="0.3"  # Default temperature (0.7 if not set)
export CONSULT7_MODEL="gemini-2.5-flash?thinking=true&temperature=0.8"
```

**⚠️ Important:** Always quote model specifications containing `?` or `&` in environment variables!

### Practical Examples

#### Analyzing large codebases with custom settings:
```bash
# High creativity for brainstorming solutions
"gemini-2.5-flash?thinking=true&temperature=1.2&budget=30000"

# Precise analysis for code review
"gemini-2.5-pro?thinking=true&temperature=0.1&budget=25000"

# Fast analysis with balanced creativity
"gemini-2.5-flash-lite-preview-06-17?thinking=true&temperature=0.7"
```

#### In Claude Desktop config:
```json
{
  "mcpServers": {
    "consult7": {
      "command": "uvx",
      "args": ["consult7", "google", "your-api-key"],
      "env": {
        "CONSULT7_MODEL": "gemini-2.5-flash?thinking=true&temperature=0.8",
        "CONSULT7_DEFAULT_TEMPERATURE": "0.3"
      }
    }
  }
}
```

## Testing

```bash
# Test OpenRouter
uvx consult7 openrouter sk-or-v1-... --test

# Test Google AI
uvx consult7 google AIza... --test

# Test OpenAI
uvx consult7 openai sk-proj-... --test
```

## Development Setup (after cloning repository)

If you've cloned the repository and want to use it as a development tool:

1. **Set up environment:**
   ```bash
   python3.11 -m venv .venv
   source .venv/bin/activate
   pip install -e .  # Editable install for development
   ```

2. **Configure environment variables:**
   ```bash
   # Required: API key for your provider
   export CONSULT7_GEMINI_API_KEY=your_api_key      # for Google AI
   # export CONSULT7_OPENAI_API_KEY=your_api_key    # for OpenAI
   # export CONSULT7_OPENROUTER_API_KEY=your_api_key # for OpenRouter
   
   # Optional: Model with new URL query format
   export CONSULT7_MODEL="gemini-2.5-flash?thinking=true&temperature=0.8"
   
   # Optional: Provider (defaults to 'google' if not set)
   export CONSULT7_PROVIDER=google
   
   # Optional: Default temperature for all models
   export CONSULT7_DEFAULT_TEMPERATURE="0.3"
   ```

3. **Add to Claude Desktop config (`claude_desktop_config.json`):**
   
   **Using editable install (recommended):**
   ```json
   {
     "mcpServers": {
       "consult7": {
         "command": "/path/to/consult7/.venv/bin/python",
         "args": ["-m", "consult7.server"],
         "env": {
           "CONSULT7_GEMINI_API_KEY": "your_api_key",
           "CONSULT7_MODEL": "gemini-2.5-flash?thinking=true&budget=25000",
           "CONSULT7_PROVIDER": "google",
           "CONSULT7_DEFAULT_TEMPERATURE": "0.8"
         }
       }
     }
   }
   ```
   
   **⚠️ Important:** Replace `/path/to/consult7` with the actual path to your cloned repository and make sure you've completed steps 1-2 above to create the `.venv` directory.

   **Alternative using uv:**
   ```json
   {
     "mcpServers": {
       "consult7": {
         "command": "uv",
         "args": ["run", "--project", "/path/to/consult7", "consult7"],
         "env": {
           "CONSULT7_GEMINI_API_KEY": "your_api_key",
           "CONSULT7_MODEL": "gemini-2.5-flash?thinking=true&temperature=0.3",
           "CONSULT7_PROVIDER": "google"
         }
       }
     }
   }
   ```

4. **Restart Claude Desktop** to load the new configuration.

**Notes:**
- The model parameter is now optional in tool calls when using environment variables
- Legacy argument-based configuration is still supported as fallback
- **Always quote** model specifications containing `?` or `&` in environment variables
- You can override any parameter in individual tool calls

## Uninstalling

To remove consult7 from Claude Code (or before reinstalling):

```bash
claude mcp remove consult7 -s user
```

