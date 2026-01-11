import sys
import os

# Ensure project root is on Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from mcp.server.fastmcp import FastMCP
from src.job_api import fetch_indeed_jobs, fetch_linkedin_jobs

# Create MCP server instance
mcp = FastMCP("Job Recommender MCP Server")

# -----------------------------
# LinkedIn Tool
# -----------------------------
@mcp.tool()
async def fetchlinkedin(keywords: str):
    """
    Fetch LinkedIn jobs using your job_api function.
    """
    return fetch_linkedin_jobs(keywords)

# -----------------------------
# Indeed Tool
# -----------------------------
@mcp.tool()
async def fetchindeed(keywords: str):
    """
    Fetch Indeed jobs using your job_api function.
    """
    return fetch_indeed_jobs(keywords)

# -----------------------------
# Run MCP server
# -----------------------------
if __name__ == "__main__":
    mcp.run(transport="stdio")
