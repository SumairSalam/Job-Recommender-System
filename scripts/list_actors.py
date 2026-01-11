from dotenv import load_dotenv
import os
from apify_client import ApifyClient

load_dotenv()
client = ApifyClient(os.getenv('APIFY_API_TOKEN'))
print('Listing first 50 actors accessible to token:')
try:
    actors_resource = client.actors()
    print('actors_resource type:', type(actors_resource))
    print('actors_resource dir sample:', [m for m in dir(actors_resource) if not m.startswith('_')][:50])
    # Try calling list with limit/offset
    res = actors_resource.list(limit=50, offset=0)
    print('list returned type:', type(res))
    # If result has 'items' key, print first few
    if isinstance(res, dict) and 'items' in res:
        print('items count:', len(res['items']))
        for a in res['items'][:10]:
            print('-', a.get('id'), '|', a.get('name'))
    else:
        print('list result not a dict with items, printing repr')
        print(res)
except Exception as e:
    print('Error listing actors:', type(e), e)
# Try to find known public actors by safe_id
candidates = ['apify/linkedin-jobs-scraper', 'apify/indeed-jobs-scraper']
for cid in candidates:
    try:
        print('\nChecking candidate', cid)
        a = client.actor(cid).get()
        print('Result:', a)
    except Exception as e:
        print('Error for', cid, type(e), e)
