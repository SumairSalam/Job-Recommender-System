import sys
import os

# Ensure project root is on Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from mcp.server.fastmcp import FastMCP
from src.job_api import fetch_indeed_jobs, fetch_linkedin_jobs

mcp = FastMCP("Job Recommender MCP Server")

@mcp.tool()
async def fetchlinkedin(keywords: str):
    return fetch_linkedin_jobs(keywords)

@mcp.tool()
async def fetchindeed(keywords: str):
    return fetch_indeed_jobs(keywords)

if __name__ == "__main__":
    mcp.run(transport="stdio")
