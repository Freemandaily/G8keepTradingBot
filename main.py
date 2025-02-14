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

print('Update 2')

YOUR_INFURA_API = 'd049a2241d97413da17d774171eb0edb'
infura_url = 'https://base-mainnet.g.alchemy.com/v2/ETR-eJGF7AD8ejoi5tzGesiS5s4Kq-DF'
w3 = Web3(Web3.HTTPProvider(infura_url))

# hash = '0x68d2bcbcd5a98b314f5da8a2aca73d4f13eeed537f71f6291e00865707a0fd67'
# receipt = w3.eth.get_transaction_receipt(hash)
# logs = receipt.get('logs',[])
# syncHash = '0x1c411e9a96e071241c2f21f7726b17ae89e3cab4c78be50e062b03a9fffbbad1'
# #print(logs)
# for log in logs:
#     topics = log['topics']
#     topic0 = topics[0].hex()
#     if topic0 == syncHash:
#         data = log['data'].hex()[2:]
#         pooledETH = int(data[:len(data)//2],16)/10**18
#         if pooledETH >= 0.1:
#             print(pooledETH)




def status(status):
        bot_token = '6344573464:AAF_dIkl-hJ5aFT_f0IbUMCmwtOhIm41tvc'
        async def main():
            try:
                bot=telegram.Bot(bot_token)
            except:
                bot=telegram.Bot(bot_token)
            async with bot:
                await bot.send_message(text=f'G8Keep Notification\n\nStatus:{status}',
                chat_id=963648721)
        if __name__=='__main__':
            asyncio.run(main())


contract_address = Web3.to_checksum_address("0x242531c3aD1D7454CD6e916Fc49e646f59c9429f")
async def processEvent(token,hash):
    hashdata = w3.eth.get_transaction(hash)
    print(hashdata['value'])
    value = hashdata['value']
    threshold = 0 #0.0015*10**18
    if value >= threshold:
        # call trading module
        subprocess.Popen(['python3','G8v2.py','first_bot',token])
        #time.sleep(0.1)
        #subprocess.Popen(['python3','G8.py','second_bot',token])
        #time.sleep(0.1)
        #subprocess.Popen(['python3','G8.py','third_bot',token])



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
                #print(event_data['params']['result']['topics'][1])
                #print(event_data['params']['result']['transactionHash'])
            except asyncio.exceptions.TimeoutError:
                continue
            except ValueError as e:
                print('this is the issue')
                print(e)
                continue

pid = str(os.getpid())
with open('G8keep.pid','w') as pid_file:
    pid_file.write(pid)

while True:
    status_check = 'Restarting G8keep'
    status(status_check)
    try:
        if __name__ == "__main__":
            loop = asyncio.new_event_loop()
            loop.run_until_complete(get_event())
    except:
        print('G8keep Going Down')
        #os.remove('G8keep.pid')
        print('Restarting')
        continue

