import httpx
import asyncio
import logging
import itertools
import regex
import json
import random

logging.basicConfig(
        level=logging.INFO,
        format='\u001b[36;1m[\u001b[0m%(asctime)s\u001b[36;1m]\u001b[0m %(message)s\u001b[0m',
        datefmt='%H:%M:%S'
        )



class DiscordWebhookSpam():
    def __init__(self):
        self.webhook                = open('data/webhook.txt', 'r', encoding='utf-8').read()
        self.message                = open('data/message.txt', 'r', encoding='utf-8').read()
        self.proxy                  = open('data/proxy.txt', 'r', encoding='utf-8').read()
        self.username               = open('data/username.txt', 'r', encoding='utf-8').read()
        self.cycle_message          = itertools.cycle(self.message.split('\n'))
        self.cycle_webhook          = itertools.cycle(self.webhook.split('\n'))
        self.cycle_proxy            = itertools.cycle(self.proxy.split('\n'))
        self.cycle_username         = itertools.cycle(self.username.split('\n'))

    async def WebhookSpam(self):
        async with httpx.AsyncClient(
                proxies = {

                    'http://': 'http://' + self.cycle_proxy.__next__()
                },
                verify=False
        ) as client:

            while True:
                webhook = next(self.cycle_webhook)
                message = next(self.cycle_message)
                username = next(self.cycle_username)
                try:
                    response = await client.post(
                        webhook,
                        data = {
                            "content": message,
                            "username": username
                            }
                    )
                    if response.status_code == 200:
                        webhook_data = await client.get(webhook);webhook_data = json.loads(webhook_data.text);guild_id = webhook_data['guild_id'];channel_id = webhook_data['channel_id']
                        logging.info(f'Spammed • Guild >> {guild_id} • Channel >> {channel_id} • {message} • {response.status_code}')
                    
                    elif response.status_code == 429:
                        logging.info(f'Rate Limited • {response.status_code}')
                
                    elif response.status_code == 404:
                        logging.info(f'Webhook Not Found • {response.status_code}')

                    else:
                        logging.info(f'Failed • {response.status_code}')

                except Exception as e:
                    logging.info(e)


    async def gather_coroutines():
        tasks = []
        for _ in range(24):
            tasks.append(asyncio.create_task(DiscordWebhookSpam().WebhookSpam()))
        await asyncio.gather(*tasks)
    

if __name__ == "__main__":
    asyncio.run(DiscordWebhookSpam().gather_coroutines())