import requests
import json
import time

authorization = '' #YOUR DISCORD AUTH TOKEN
channel = '' #DISCORD CHANNEL
url = "https://discordapp.com/api/v6/channels/" + str(channel) + "/messages?limit=100"
headers = {
    'authorization': authorization,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.306 Chrome/78.0.3904.130 Electron/7.1.11 Safari/537.36'
}

email_list = []
id_list = []
site = []
sku = []
messages_count = 1000 #DO IN INCREMENTS OF 100
repeat = (messages_count - 100) / 100

r = requests.get(url, headers=headers)
initial_text = r.text

load = json.loads(initial_text)
for x in load:
    id = x['id']

repeated = 0

while repeated <= repeat:
    back_text = 'https://discordapp.com/api/v8/channels/' + channel + '/messages?before=' + id + '&limit=100'
    r = requests.get(back_text, headers=headers)
    counts = 0
    for x in json.loads(r.text):
        id = x['id']
    repeated += 1
    jsoned = (json.loads(initial_text) + json.loads(r.text))
    for x in jsoned:
        if 'Wrath Success' in str(x):  # Want to look for Wrath webhooks only
            if 'SKU' in str(x):  # We want only footsites orders and footsites orders only have SKUs
                embeds = x['embeds']  # Want to get embed so we can iterate through that
                for x in embeds:
                    try:
                        author = x['author']
                    except:
                        pass
                    try:
                        fields = x['fields']
                        site_splitter = str(fields).split("'")
                        site.append(site_splitter[7])
                        sku.append(site_splitter[126])
                    except:
                        pass
                    if (author['name']) == 'Wrath Success':
                        if 'SKU' in str(x):
                            for x in fields:
                                if '||' in str(x):
                                    found = str(x)
                                    if 'Email' in found:
                                        splitter = str(x).split('||')
                                        email = (splitter[1])
                                        email_list.append(email)
                                    if 'Order ID' in found:
                                        splitter = str(x).split('||')
                                        order_id = (splitter[1])
                                        id_list.append(order_id)
amount = (len(email_list) - 1)
counter = 0
while counter <= amount:
    print(
        '[' + str(sku[counter]) + '] ' + '(' + str(site[counter]) + ') ' + str(email_list[counter]) + ':' + str(
            id_list[counter]))
    counter += 1
array_counter = 0
while array_counter < len(email_list):
    session = requests.Session()

    sessionHeaders = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "content-type": "application/json"
    }

    s = session.get('https://www.footlocker.com/api/session', headers=sessionHeaders)
    loadedData = json.loads(s.text)
    csrfToken = loadedData['data']['csrfToken']

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "accept": "application/json",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive",
        "content-type": "application/json",
        "x-csrf-token": csrfToken
    }

    payload = {
        "code": id_list[array_counter],
        "customerEmail": email_list[array_counter]
    }

    checkReq = session.post('https://www.footlocker.com/api/users/orders/status', headers=headers, json=payload)
    if 'Check your email address and confirmation number' in checkReq.text:
        print('Invalid Email/Conf Number')
        exit()
    d = checkReq.text.split(':')
    status = (d[5].replace('"', '').replace(',', '').replace('shipAddresses', ''))
    print('[' + (str(array_counter)) + ']' + ' ' + email_list[array_counter] + ':' + id_list[array_counter] + ' ' + status)
    array_counter += 1
