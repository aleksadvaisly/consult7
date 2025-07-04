"""Tool descriptions and model examples for Consult7 MCP server."""


class ToolDescriptions:
    """Centralized management of tool descriptions and model examples."""

    MODEL_EXAMPLES = {
        "openrouter": [
            '"google/gemini-2.5-pro" (intelligent, 1M context)',
            '"google/gemini-2.5-flash" (fast, 1M context)',
            '"google/gemini-2.5-flash-lite-preview-06-17" (ultra fast, 1M context)',
            '"anthropic/claude-sonnet-4" (Claude Sonnet, 200k context)',
            '"openai/gpt-4.1" (GPT-4.1, 1M+ context)',
            '"anthropic/claude-sonnet-4?thinking=true" (Claude with reasoning)',
            '"anthropic/claude-sonnet-4?thinking=true&budget=30000" (Claude with custom budget)',
            '"google/gemini-2.5-flash?thinking=true" (ultra fast with reasoning)',
            '"anthropic/claude-sonnet-4|thinking" (legacy format)',
        ],
        "google": [
            '"gemini-2.5-flash" (fast, standard mode)',
            '"gemini-2.5-flash-lite-preview-06-17" (ultra fast, lite model)',
            '"gemini-2.5-pro" (intelligent, standard mode)',
            '"gemini-2.0-flash-exp" (experimental model)',
            '"gemini-2.5-flash?thinking=true" (fast with deep reasoning)',
            '"gemini-2.5-flash?thinking=true&budget=15000" (fast with custom budget)',
            '"gemini-2.5-pro?thinking=true" (intelligent with deep reasoning)',
            '"gemini-2.5-flash|thinking" (legacy format)',
        ],
        "openai": [
            '"gpt-4.1-2025-04-14?context=1000k" (1M+ context, very fast)',
            '"gpt-4.1-nano-2025-04-14?context=1000k" (1M+ context, ultra fast)',
            '"o3-2025-04-16?context=200k" (advanced reasoning model)',
            '"o4-mini-2025-04-16?context=200k" (fast reasoning model)',
            '"o1-mini?context=128k&thinking=true" (mini reasoning with thinking)',
            '"o3-2025-04-16?context=200k&thinking=true" (advanced with thinking)',
            '"gpt-4.1-2025-04-14|1047576" (legacy format)',
        ],
    }

    @classmethod
    def get_consultation_tool_description(cls, provider: str) -> str:
        """Get the main description for the consultation tool."""
        provider_notes = cls._get_provider_notes(provider)

        return f"""Consult an LLM about code files matching a pattern in a directory.

This tool collects all files matching a regex pattern from a directory tree,
formats them into a structured document, and sends them to an LLM along with
your query. The LLM analyzes the code and returns insights.

{provider_notes}

Notes:
- Automatically ignores: __pycache__, .env, secrets.py, .DS_Store, .git, node_modules
- File size limit: 10MB per file, 100MB total (optimized for large context models)
- Large files are skipped with an error message
- Includes detailed errors for debugging (permissions, missing paths, etc.)"""

    @classmethod
    def get_model_parameter_description(cls, provider: str) -> str:
        """Get the model parameter description with provider-specific examples."""
        examples = cls.MODEL_EXAMPLES.get(provider, [])

        if provider == "openai":
            model_desc = (
                "The model to use. New format: model?context=200k&thinking=true or "
                'legacy format: model|200k|thinking.\nExamples:'
            )
        else:
            model_desc = "The model to use. New format: model?thinking=true&budget=15000 or legacy: model|thinking. Examples:"

        # Add examples on new lines, but check where to add thinking note
        thinking_examples_start = -1
        for i, example in enumerate(examples):
            if ("?thinking=true" in example or "|thinking" in example) and thinking_examples_start == -1:
                thinking_examples_start = i
                # Add the thinking note before the first thinking example
                if provider in ["google", "openrouter"]:
                    suffix_type = "thinking" if provider == "google" else "reasoning"
                    model_desc += f"\n\nWith {suffix_type} mode:"
                elif provider == "openai":
                    model_desc += "\n\nWith thinking mode (o-series models):"
            model_desc += f"\n  {example}"

        return model_desc

    @classmethod
    def get_path_description(cls) -> str:
        """Get the path parameter description."""
        return "Absolute filesystem path to search from (e.g., /Users/john/myproject)"

    @classmethod
    def get_pattern_description(cls) -> str:
        """Get the pattern parameter description."""
        return (
            'Regex to match filenames. Common patterns: ".*\\.py$" for '
            'Python files, ".*\\.(js|ts)$" for JavaScript/TypeScript'
        )

    @classmethod
    def get_query_description(cls) -> str:
        """Get the query parameter description."""
        return "Your question about the code (e.g., 'Which functions handle authentication?')"

    @classmethod
    def get_exclude_pattern_description(cls) -> str:
        """Get the exclude_pattern parameter description."""
        return 'Optional regex to exclude files (e.g., ".*test.*" to skip tests)'

    @classmethod
    def _get_provider_notes(cls, provider: str) -> str:
        """Get provider-specific notes."""
        if provider == "openai":
            return ""  # Move note to model parameter description
        elif provider == "google":
            return (
                "Thinking Mode: Use ?thinking=true for deep reasoning (e.g., gemini-2.5-flash?thinking=true).\n"
                "Advanced: For custom thinking limits, use ?thinking=true&budget=30000\n"
                "Legacy: |thinking format still supported\n"
                "Important: Always quote models with ? or & in environment variables"
            )
        elif provider == "openrouter":
            return (
                "Reasoning Mode: Use ?thinking=true to enable deeper analysis.\n"
                "Advanced: For custom limits, use ?thinking=true&budget=30000\n"
                "Legacy: |thinking format still supported\n"
                "Important: Always quote models with ? or & in environment variables"
            )
        else:
            return "Note: Model context windows are auto-detected from the API"
