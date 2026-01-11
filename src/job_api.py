import os
import apify_client
from apify_client import ApifyClient
from dotenv import load_dotenv

load_dotenv()

# Ensure APIFY API token is present
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
if not APIFY_API_TOKEN:
    raise RuntimeError("APIFY_API_TOKEN is not set. Please set it in your environment or .env file.")

apify_client = ApifyClient(APIFY_API_TOKEN)

def fetch_linkedin_jobs(search_query, location="Germany", rows=60):
    """Fetch LinkedIn jobs using Apify's LinkedIn jobs scraper actor.

    Actor ID can be overridden with the APIFY_ACTOR_ID env var (defaults to 'apify/linkedin-jobs-scraper').
    """
    actor_id = os.getenv("APIFY_ACTOR_ID", "apify/linkedin-jobs-scraper")

    run_input = {
        "title": search_query,
        "location": location,
        "rows": rows,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"]
        }
    }

    try:
        run = apify_client.actor(actor_id).call(run_input=run_input)
    except apify_client.errors.ApifyApiError as e:
        # Provide a clearer error message for common causes
        msg = str(e)
        if "Actor was not found" in msg:
            raise RuntimeError(f"Apify actor '{actor_id}' was not found. Check APIFY_ACTOR_ID or that the actor exists and your token has access.") from e
        raise

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
