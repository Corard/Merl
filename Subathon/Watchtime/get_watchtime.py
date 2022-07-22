import csv
import requests
import json
import math
import sys
from alive_progress import alive_bar

# Ask the user if this is the before or after data and store the answer in a variable
print("Collect before data, after data or compare the files?")
data_type = input("Type 'before' or 'after' or 'compare' and press enter: ")

if data_type == "compare":

    print("Comparing data...")

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
    
    # Name, Before, After, Difference, Done?
    header = ["Name", "Before", "After", "Difference", "Done?"]
    data = []

    with alive_bar(len(before_data)) as bar:    
        for user in before_data:
            a_data = []
            a_data.append(user["username"])
            a_data.append(user["minutes"])
            for after_user in after_data:
                if after_user["username"] == user["username"]:
                    if after_user["minutes"] - user["minutes"] > 100:
                        a_data.append(after_user["minutes"])
                        a_data.append(after_user["minutes"] - user["minutes"])
                        a_data.append("")
                        data.append(a_data)
                        break
            bar()
    with open('compare.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(data)

    sys.exit()

elif data_type == "before" or data_type == "after":

    # Get all watchtime from StreamElements API and write to a JSON file
    watchtime_base_url = 'https://api.streamelements.com/kappa/v2/points/5a8626723631ab0001258305/watchtime?offset='
    limit = requests.get(watchtime_base_url).json()['_total']
    json_data = []

    print('Total users: ' + str(limit) + ' // ' + str(math.ceil(limit/25)) + ' requests')
    
    with alive_bar(math.ceil(limit/25)) as bar:
        for offset in range(0, limit, 25):
            url = f'{watchtime_base_url}{offset}'
            req = requests.get(url)
            if req.status_code == 200:
                data = req.json()['users']
                for user in data:
                    json_data.append(user)
                bar()

    with open(f'{data_type}.json', 'w') as f:
        f.write(json.dumps(json_data))

else:
    print("Invalid input")
    sys.exit()