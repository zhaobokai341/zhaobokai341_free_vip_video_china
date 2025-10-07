import random
import requests
import json
import re
from urllib3.exceptions import InsecureRequestWarning
import warnings

warnings.filterwarnings('ignore', category=InsecureRequestWarning)
url_regex = r'https?://.+..+'
def read_file(file_name):
    with open(file_name, 'r') as file:
        data = file.read()
        data = json.loads(data)
    return data

def check_valid_url(url, regex_pattern):
    if re.match(regex_pattern, url):
        return True
    else:
        return False

def check_can_access(url):
    user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36",
    "Mozilla/5.0 (iPad; CPU OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/99.0.4844.73 Mobile/15E148 Safari/604.1",
    # Add more User-Agent strings as needed
    ]

    random_user_agent = random.choice(user_agents)
    try:
        response = requests.get(url, timeout=10, headers={"User-Agent": random_user_agent}, verify=False)
        if response.status_code == 200 and response.url == url:
            return True
        else:
            return False
    except:
        return False

def save_result(file_name, json_data):
    with open(file_name, 'w') as file:
        json.dump(json_data, file, ensure_ascii=False, indent=4)

def remove_same_url(json_data):
    json_data['pirated'] = list({v['url']: v for v in json_data['pirated']}.values())
    json_data['pirated2'] = list({v['url']: v for v in json_data['pirated2']}.values())
    return json_data

json_data = read_file('pirated.json')
#json_data = read_file('test/test.json')
print(json_data)
for item in json_data['pirated']:
    print(f"Checking URL: {item['url']}")
    if not check_valid_url(item['url'], url_regex):
        print("Invalid URL")
        item['error'] = "Invalid URL"
    elif not check_can_access(item['url']):
        print("Cannot access URL or HTTPS status code is not 200 or URL redirected")
        item['error'] = "Cannot access URL or HTTPS status code is not 200 or URL redirected"
    else:
        print("ok")
        item['error'] = "ok"

for item in json_data['pirated2']:
    print(f"Checking URL: {item['url']}")
    if not check_valid_url(item['url'], url_regex):
        print("Invalid URL")
        item['error'] = "Invalid URL"
    elif not check_can_access(item['url'].replace('{url}', 'https://www.mgtv.com')):
        print("Cannot access URL or HTTPS status code is not 200")
        item['error'] = "Cannot access URL or HTTPS status code is not 200"
    else:
        print("ok")
        item['error'] = "ok"
json_data = remove_same_url(json_data)
save_result('pirated_result.json', json_data)
print("Done")