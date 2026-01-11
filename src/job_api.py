
import os
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()
apify_client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# -----------------------------
# LINKEDIN SCRAPER (YOUR ACTOR)
# -----------------------------
def fetch_linkedin_jobs(search_query, location="Germany", rows=60):
    url = f"https://www.linkedin.com/jobs/search/?keywords={search_query}&location={location}"

    run_input = {
        "urls": [url],
        "scrapeCompanyDetails": True,
        "maxJobs": rows
    }

    # YOUR REAL ACTOR ID
    run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs


# -----------------------------
# INDEED SCRAPER (WAITING FOR YOUR REAL ID)
# -----------------------------
def fetch_indeed_jobs(search_query, location="Germany", rows=50):
    run_input = {
        "query": search_query,
        "location": location,
        "maxItems": rows
    }

    # Replace this once you give me your Indeed actor ID
    run = apify_client.actor("REPLACE_WITH_INDEED_ACTOR_ID").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs



