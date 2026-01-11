import os
from apify_client import ApifyClient
from apify_client.errors import ApifyApiError
from dotenv import load_dotenv

load_dotenv()

# Minimal, forgiving Apify wrapper so the app doesn't crash on missing actors/tokens.
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
apify_client = ApifyClient(APIFY_API_TOKEN) if APIFY_API_TOKEN else None


def _run_actor_and_get_jobs(actor_id, run_input):
    """Helper: runs an actor and returns job items or empty list on failure."""
    if not apify_client:
        return []
    try:
        run = apify_client.actor(actor_id).call(run_input=run_input)
        return list(apify_client.dataset(run.get("defaultDatasetId")).iterate_items())
    except ApifyApiError:
        return []
    except Exception:
        return []


def fetch_linkedin_jobs(search_query, location="Germany", rows=60):
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
    return _run_actor_and_get_jobs(actor_id, run_input)


def fetch_indeed_jobs(search_query, location="Germany", rows=70):
    actor_id = os.getenv("APIFY_INDEED_ACTOR_ID", "apify/indeed-jobs-scraper")
    run_input = {
        "title": search_query,
        "location": location,
        "rows": rows,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"]
        }
    }
    return _run_actor_and_get_jobs(actor_id, run_input)


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
