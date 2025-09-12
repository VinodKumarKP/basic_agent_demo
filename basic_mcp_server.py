#!/usr/bin/env python3
"""
Simple MCP Server with FastMCP that returns dummy names
"""

import asyncio
from typing import List
from fastmcp import FastMCP

# Create the MCP server instance
mcp = FastMCP("DummyNamesServer")

# Sample dummy names data
DUMMY_NAMES = [
    "Alice Johnson",
    "Bob Smith",
    "Carol Davis",
    "David Wilson",
    "Emma Brown",
    "Frank Miller",
    "Grace Taylor",
    "Henry Anderson",
    "Ivy Martinez",
    "Jack Thompson",
    "Kate White",
    "Liam Harris",
    "Mia Clark",
    "Noah Lewis",
    "Olivia Walker"
]


@mcp.tool()
def get_dummy_names(count: int = 10) -> List[str]:
    """
    Returns a list of dummy names.

    Args:
        count: Number of names to return (default: 10, max: 15)

    Returns:
        List of dummy names
    """
    # Ensure count is within reasonable bounds
    count = max(1, min(count, len(DUMMY_NAMES)))

    return DUMMY_NAMES[:count]


@mcp.tool()
def get_random_names(count: int = 5) -> List[str]:
    """
    Returns a random selection of dummy names.

    Args:
        count: Number of random names to return (default: 5, max: 15)

    Returns:
        List of randomly selected dummy names
    """
    import random

    # Ensure count is within reasonable bounds
    count = max(1, min(count, len(DUMMY_NAMES)))

    return random.sample(DUMMY_NAMES, count)


@mcp.tool()
def search_names(query: str) -> List[str]:
    """
    Search for names containing the query string.

    Args:
        query: Search term to find in names

    Returns:
        List of names matching the search query
    """
    query = query.lower()
    matching_names = [name for name in DUMMY_NAMES if query in name.lower()]
    return matching_names



if __name__ == "__main__":
    mcp.run()
