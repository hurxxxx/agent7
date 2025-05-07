#!/usr/bin/env python
"""
Test script for TavilySearch implementation.

This script tests the TavilySearch implementation directly using the TavilySearch class.
It performs a simple search query and prints the results.
"""

import asyncio
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Import TavilySearch directly
from langchain_tavily import TavilySearch

async def test_search():
    """Test the TavilySearch with a simple query."""
    print("Testing TavilySearch implementation...")

    # Check if TAVILY_API_KEY is set
    if not os.environ.get("TAVILY_API_KEY"):
        print("Error: TAVILY_API_KEY environment variable is not set.")
        return

    # Create a TavilySearch instance
    search_tool = TavilySearch(
        max_results=5,
        include_answer=True,
        include_raw_content=True,
        include_images=True,
    )

    # Perform a search
    query = "What is LangGraph?"
    print(f"Searching for: {query}")

    try:
        results = await search_tool.ainvoke({"query": query})

        if results:
            print("\nSearch successful!")
            print("\nResults:")
            print(results)
        else:
            print("Error: No search results returned.")
    except Exception as e:
        print(f"Error during search: {e}")

if __name__ == "__main__":
    asyncio.run(test_search())
