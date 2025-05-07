"""This module provides tools for web scraping and search functionality.

It includes a Tavily search function for web search capabilities.

These tools are integrated with LangGraph to provide the agent with the ability
to search the web for information.
"""

from typing import Any, Callable, Dict, List, Optional

from langchain_tavily import TavilySearch  # type: ignore[import-not-found]

from react_agent.configuration import Configuration


async def search(query: str) -> Optional[Dict[str, Any]]:
    """Search for general web results.

    This function performs a search using the Tavily search engine, which is designed
    to provide comprehensive, accurate, and trusted results. It's particularly useful
    for answering questions about current events, facts, and general information.

    Args:
        query: The search query string.

    Returns:
        A dictionary containing search results or None if the search failed.
    """
    configuration = Configuration.from_context()

    # Create a TavilySearch instance with standard configuration
    search_tool = TavilySearch(
        max_results=configuration.max_search_results,
        include_answer=True,
        include_raw_content=True,
        include_images=True,
        api_key=configuration.tavily_api_key,
    )

    # Invoke the search tool with the query
    results = await search_tool.ainvoke({"query": query})

    # Update the state with search results
    return {
        "search_results": results,
        "messages": [
            {
                "role": "tool",
                "tool_call_id": None,  # This will be filled in by the framework
                "name": "search",
                "content": str(results),
            }
        ],
    }


TOOLS: List[Callable[..., Any]] = [search]
