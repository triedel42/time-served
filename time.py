#!/usr/bin/env python3
#curl -X POST --data "grant_type=client_credentials&client_id=$FT_UID&client_secret=$FT_SECRET" https://api.intra.42.fr/oauth/token

import os
import sys
from getpass import getuser
from pprint import pprint
from datetime import datetime, timedelta

from requests import get, post

uid = os.getenv('FT_UID')
sec = os.getenv('FT_SECRET')

if not uid or not sec:
    sys.exit('Error: Set $FT_UID and $FT_SECRET to your API credentials.')

# Read in user from either argv, or user input (default is system user)
user = None
if len(sys.argv) > 1:
	user = sys.argv[1]

if not user:
	user = os.getenv('FT_USER', None)

if not user:
	inp = input(f'user ({getuser()}): ')
	if inp:
		user = inp
	else:
		user = getuser()

# prepare request
data = {
    'grant_type': 'client_credentials',
    'client_id': uid,
    'client_secret': sec,
}

resp = post('https://api.intra.42.fr/oauth/token', data=data).json()
#pprint(resp)
token = resp['access_token']

auth_header = {
        'Authorization': 'Bearer ' + token
}

base = 'https://api.intra.42.fr/v2/'
# endp = sys.argv[1]
# url = base + endp




def get_logtime(user, win=1):
    week_start = (datetime.today() - timedelta(days=datetime.today().isoweekday() % 7) - timedelta(weeks=win - 1))
    week_end = (week_start + timedelta(weeks=win)).date().strftime("%Y-%m-%d")
    week_start = week_start.date().strftime("%Y-%m-%d")
    params = {
        'begin_at': week_start,
        'end_at': week_end
    }
    r = get(base + 'users/' + user + '/locations_stats', params=params, headers=auth_header).json()
    total = timedelta()
    for key, val in r.items():
        # import pdb; pdb.set_trace()
        day = datetime.fromisoformat(key)
        print(day.strftime("%Y-%m-%d"), f'(week {day.isocalendar()[1]}): {val}')
        h, m, s = map(int, val.split('.')[0].split(':'))
        total += timedelta(hours=h, minutes=m, seconds=s)
    print('=' * 42)
    print(f'Total log time for {user} from {week_start} to {week_end} \n' + str(total.total_seconds() / 3600))


get_logtime(user)

# print('getting: ' + endp)
# r = get(url, headers=auth_header)
# print(r)
# pprint(r.json())
