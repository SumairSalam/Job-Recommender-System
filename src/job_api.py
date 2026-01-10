import os
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

apify_client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

def fetch_linkedin_jobs(search_query, location="Germany", rows=60):
    run_input = {
        "title": search_query,
        "location": location,
        "rows": rows,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"]
        }
    }
    run = apify_client.actor("BHzefUZlZRkWxkTck").call(run_input=run_input)
    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs

def fetch_indeed_jobs(search_query, location="Germany", rows=70):
    run_input = {
        "title": search_query,
        "location": location,
        "rows": rows,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"]
        }
    }
    run = apify_client.actor("apify/linkedin-jobs-scraper").call(
    run_input=run_input
)



    jobs = list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs
