import requests
import json


authorization = '' #YOUR DISCORD AUTH TOKEN
channel = '' #WHERE YOUR WEBHOOKS ARE AT
url = "https://discordapp.com/api/v6/channels/" + str(channel) + "/messages?limit=100"
SKU = ''

headers = {
    'authorization': authorization,
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) discord/0.0.306 Chrome/78.0.3904.130 Electron/7.1.11 Safari/537.36'
}

email_list = []
id_list = []
site = []
sku = []

r = requests.get(url, headers=headers)
messageJson = json.loads(r.text)

for x in messageJson: #Iterates through the whole response that discord sends so we can analyze each message 1 by 1
    if 'Wrath Success' in str(x): #Want to look for Wrath webhooks only
        if 'SKU' in str(x): #We want only footsites orders and footsites orders only have SKUs
            embeds = x['embeds'] #Want to get embed so we can iterate through that
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
    print('[' + str(sku[counter]) + '] ' + '(' + str(site[counter]) + ') ' + str(email_list[counter]) + ':' + str(id_list[counter]))
    counter += 1
