"""Define the configurable parameters for the agent."""

from __future__ import annotations

import os
from dataclasses import dataclass, field, fields
from typing import Annotated, Optional

from langchain_core.runnables import ensure_config
from langgraph.config import get_config

from react_agent import prompts


@dataclass(kw_only=True)
class Configuration:
    """The configuration for the agent."""

    system_prompt: str = field(
        default=prompts.SYSTEM_PROMPT,
        metadata={
            "description": "The system prompt to use for the agent's interactions. "
            "This prompt sets the context and behavior for the agent."
        },
    )

    model: Annotated[str, {"__template_metadata__": {"kind": "llm"}}] = field(
        default="anthropic/claude-3-5-sonnet-20240620",
        metadata={
            "description": "The name of the language model to use for the agent's main interactions. "
            "Should be in the form: provider/model-name."
        },
    )

    max_search_results: int = field(
        default=10,
        metadata={
            "description": "The maximum number of search results to return for each search query."
        },
    )

    tavily_api_key: Optional[str] = field(
        default=None,
        metadata={
            "description": "The API key for the Tavily search engine. "
            "If not provided, it will be loaded from the TAVILY_API_KEY environment variable."
        },
    )

    @classmethod
    def from_context(cls) -> Configuration:
        """Create a Configuration instance from a RunnableConfig object."""
        try:
            config = get_config()
        except RuntimeError:
            config = None
        config = ensure_config(config)
        configurable = config.get("configurable") or {}

        # Create a configuration instance
        _fields = {f.name for f in fields(cls) if f.init}
        instance = cls(**{k: v for k, v in configurable.items() if k in _fields})

        # Set Tavily API key from environment if not provided
        if instance.tavily_api_key is None:
            instance.tavily_api_key = os.environ.get("TAVILY_API_KEY")

        return instance
