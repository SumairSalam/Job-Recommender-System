from dotenv import load_dotenv
import os
from apify_client import ApifyClient

load_dotenv()
client = ApifyClient(os.getenv('APIFY_API_TOKEN'))
print('client has attributes starting with actor/actors:')
print([m for m in dir(client) if m.startswith('actor') or m.startswith('actors')][:50])
actor = client.actor('apify/linkedin-jobs-scraper')
print('\nactor object dir:')
print([m for m in dir(actor) if not m.startswith('_')][:200])
print('\ncalling actor.get()')
print(actor.get())
