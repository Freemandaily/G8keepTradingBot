import json
from web3 import *
from websockets import connect
import asyncio
import time
import ssl
import certifi
from hexbytes import HexBytes
import subprocess
import os
# import psutil,sys
import telegram
from telegram.constants import ParseMode

infura_url = 'https://base-mainnet.g.alchemy.com/v2/ETR-eJGF7AD8ejoi5tzGesiS5s4Kq-DF'
w3 = Web3(Web3.HTTPProvider(infura_url))

contract_address = Web3.to_checksum_address("0x242531c3aD1D7454CD6e916Fc49e646f59c9429f")
async def processEvent(token,hash):
    hashdata = w3.eth.get_transaction(hash)
    print(hashdata['value'])
    value = hashdata['value']
    threshold = 0 # choose threshold of a deployer bought amount
    if value >= threshold:
        subprocess.Popen(['python3','G8v2.py','first_bot',token])  # call trading module



async def processFilter(event_data):
    deployedTokenHash = '0xa972e8e5afb51408a9d3743f5cae264977da49f47267bd8b1ed62f31e026f08c' # DeployedToken function Keckac
    topic0 = event_data['params']['result']['topics'][0]
    if topic0 == deployedTokenHash:
        tokenDeployed = '0x'+ event_data['params']['result']['topics'][1][26:]
        transactionHash = event_data['params']['result']['transactionHash']
        await processEvent(tokenDeployed,transactionHash)

ssl_context = ssl.create_default_context(cafile=certifi.where())
# Main function that is run asynchronously and independently of the rest of the program
async def get_event(): 
# Initiates the connection between your dapp and the network 
    async with connect("wss://base-mainnet.g.alchemy.com/v2/ETR-eJGF7AD8ejoi5tzGesiS5s4Kq-DF",ssl=ssl_context) as ws:

        await ws.send(json.dumps({"id": 1, "method": "eth_subscribe", "params": ["logs", {"address": [f'{contract_address}']}]}))
        # Wait for the subscription completion.
        subscription_response = await ws.recv()
        print(f"Subscription response: {subscription_response}")
        while True:
            print('Waiting For G8keep Token..........')
            try:
                # Wait for the message in websockets and print the contents.
                #message = await asyncio.wait_for(ws.recv(), timeout=10)
                message = await ws.recv()
                event_data = json.loads(message)
                await processFilter(event_data)
            except asyncio.exceptions.TimeoutError:
                continue
            except ValueError as e:
                print('this is the issue')
                print(e)
                continue
def config():
    print('Creating Config file')
    amount = float(input('Enter amount To Buy With\n'))
    duration = int(input('Enter Minute To Wait Before Selling Or Enter 0 if You Are Holding\n'))
    data = {'amount':amount,'time':duration}
    with open('config.json','w') as file:
        json.dump(data,file,indent=3)


try:
   with open('config.json','r') as file:
       print('config file Loaded')
except:
    config()

while True:
    status_check = 'Restarting G8keep'
    try:
        if __name__ == "__main__":
            loop = asyncio.new_event_loop()
            loop.run_until_complete(get_event())
    except:
        print('G8keep Going Down')
        print('Restarting')
        continue

