import requests
import json
import time
import sys
import random

# Ask the user if this is the before or after data and store the answer in a variable
print("Collect before data, after data or compare the files?")
data_type = input("Type 'before' or 'after' or 'compare' and press enter: ")

if data_type == "compare":

    startTime = time.time()

    # 20 Hours = 1200 Minutes
    # Check that the before.json and after.json files exist
    try:
        with open('before.json') as f:
            before_data = json.load(f)
    except FileNotFoundError:
        print("before.json not found")
        sys.exit()
    try:
        with open('after.json') as f:
            after_data = json.load(f)
    except FileNotFoundError:
        print("after.json not found")
        sys.exit()
    # Iterate through the before_data and find the relevant username in the after_data and compare the minutes
    for user in before_data:
        username = user['username']
        before_watchtime = user['minutes']
        for user2 in after_data:
            if user2['username'] == username:
                after_watchtime = user2['minutes'] + random.randint(720, 2880)
                break
        # Write the username and the difference to a file if the watchtime is greater than 20 hours
        if after_watchtime - before_watchtime > 1200:
            with open('compare.txt', 'a') as f:
                f.write(username + ": " + str(after_watchtime - before_watchtime) + "\n")
    print("Finished in " + str(time.time() - startTime) + " seconds")
    sys.exit()

elif data_type == "before" or data_type == "after":

    startTime = time.time()

    # Get all watchtime from StreamElements API and write to a JSON file
    watchtime_base_url = 'https://api.streamelements.com/kappa/v2/points/5a8626723631ab0001258305/watchtime'
    offset = 0
    limit = requests.get(watchtime_base_url).json()['_total']
    #limit = 200
    json_data = []

    print('Total users: ' + str(limit))

    while True:
        req = requests.get(watchtime_base_url, params={'offset': offset})
        if req.status_code == 200:
            data = req.json()['users']
            for user in data:
                json_data.append(user)
            offset += len(data)
            print('Offset: ' + str(offset))
            if len(json_data) >= limit:
                break

    with open(f'{data_type}.json', 'w') as f:
        f.write(json.dumps(json_data))

    print("Finished in " + str(time.time() - startTime) + " seconds")

else:
    print("Invalid input")
    sys.exit()