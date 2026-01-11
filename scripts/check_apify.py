from dotenv import load_dotenv
import os
from apify_client import ApifyClient
from apify_client.errors import ApifyApiError

load_dotenv()

print('APIFY_API_TOKEN present:', bool(os.getenv('APIFY_API_TOKEN')))

client = ApifyClient(os.getenv('APIFY_API_TOKEN'))

for actor_id in [os.getenv('APIFY_ACTOR_ID', 'apify/linkedin-jobs-scraper'), os.getenv('APIFY_INDEED_ACTOR_ID', 'apify/indeed-jobs-scraper')]:
    print('\nChecking actor:', actor_id)
    try:
        a = client.actor(actor_id).get()
        print('FOUND', actor_id, 'name=', a.get('name'))
    except ApifyApiError as e:
        print('ERROR', str(e))
    except Exception as e:
        print('UNEXPECTED ERROR', type(e), e)
