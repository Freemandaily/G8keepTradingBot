from web3 import *
import time,os,sys
import telegram
import asyncio
from telegram.constants import ParseMode


abi = [{"inputs":[{"components":[{"internalType":"string","name":"TOKEN_NAME","type":"string"},{"internalType":"string","name":"TOKEN_SYMBOL","type":"string"},{"internalType":"uint256","name":"FID","type":"uint256"},{"internalType":"string","name":"IMAGE","type":"string"},{"internalType":"string","name":"CAST_HASH","type":"string"},{"internalType":"uint112","name":"TOTAL_SUPPLY","type":"uint112"},{"internalType":"address","name":"G8KEEP_FEE_WALLET","type":"address"},{"internalType":"uint16","name":"G8KEEP_FEE","type":"uint16"},{"internalType":"uint16","name":"LIQUIDITY_SUPPLEMENT_FEE","type":"uint16"},{"internalType":"address","name":"DEPLOYER","type":"address"},{"internalType":"uint112","name":"DEPLOYER_REWARD","type":"uint112"},{"internalType":"contract INonfungiblePositionManager","name":"UNISWAP_POSITION_MANAGER","type":"address"},{"internalType":"contract IG8keepLockerFactory","name":"LOCKER_FACTORY","type":"address"},{"internalType":"uint24","name":"UNISWAP_FEE_TIER","type":"uint24"},{"internalType":"address","name":"WETH","type":"address"},{"internalType":"uint112","name":"LIQUIDITY_SHIFT","type":"uint112"},{"internalType":"uint112","name":"MIGRATION_MINIMUM_LIQUIDITY","type":"uint112"},{"internalType":"uint40","name":"SNIPE_PROTECTION_SECONDS","type":"uint40"},{"internalType":"uint40","name":"SNIPE_PROTECTION_HEAVY_PENALTY_SECONDS","type":"uint40"},{"internalType":"uint8","name":"SNIPE_PROTECTION_HEAVY_EXPONENT_START","type":"uint8"},{"internalType":"uint160","name":"START_SQRT_PRICE","type":"uint160"}],"internalType":"struct Parameters","name":"parameters","type":"tuple"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"CurveMigrated","type":"error"},{"inputs":[],"name":"InsufficientAllowance","type":"error"},{"inputs":[],"name":"InsufficientBalance","type":"error"},{"inputs":[],"name":"InsufficientOutput","type":"error"},{"inputs":[],"name":"InvalidAmount","type":"error"},{"inputs":[],"name":"InvalidCaller","type":"error"},{"inputs":[],"name":"InvalidReserves","type":"error"},{"inputs":[],"name":"NotMigrated","type":"error"},{"inputs":[],"name":"PoolAlreadyCreated","type":"error"},{"inputs":[],"name":"ZeroAddress","type":"error"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"owner","type":"address"},{"indexed":True,"internalType":"address","name":"spender","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"buyer","type":"address"},{"indexed":False,"internalType":"uint256","name":"ethAmountA","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"ethAmountB","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"classA","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"classB","type":"uint256"}],"name":"Buy","type":"event"},{"anonymous":False,"inputs":[],"name":"MigrationFailed","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"seller","type":"address"},{"indexed":False,"internalType":"uint256","name":"tokenAmount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"ethAmount","type":"uint256"}],"name":"Sell","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"pair","type":"address"},{"indexed":True,"internalType":"address","name":"lpLocker","type":"address"},{"indexed":False,"internalType":"uint256","name":"ethAmount","type":"uint256"},{"indexed":False,"internalType":"uint256","name":"tokenAmount","type":"uint256"}],"name":"TokenMigrated","type":"event"},{"anonymous":False,"inputs":[{"indexed":True,"internalType":"address","name":"from","type":"address"},{"indexed":True,"internalType":"address","name":"to","type":"address"},{"indexed":False,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"inputs":[],"name":"G8KEEP_FEE_WALLET","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"_allowance","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"_balance","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"to","type":"address"},{"internalType":"uint256","name":"minimumOut","type":"uint256"}],"name":"buy","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint256","name":"minimumOut","type":"uint256"}],"name":"buy","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"uint112","name":"ethAmount","type":"uint112"}],"name":"calculateBuy","outputs":[{"internalType":"uint112","name":"tokenAmount","type":"uint112"},{"internalType":"uint112","name":"ethA","type":"uint112"},{"internalType":"uint112","name":"ethB","type":"uint112"},{"internalType":"uint112","name":"classA","type":"uint112"},{"internalType":"uint112","name":"classB","type":"uint112"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"from","type":"address"},{"internalType":"uint112","name":"tokenAmount","type":"uint112"}],"name":"calculateSell","outputs":[{"internalType":"uint112","name":"ethAmount","type":"uint112"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"castHash","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"classBalanceOf","outputs":[{"internalType":"uint256","name":"_balanceA","type":"uint256"},{"internalType":"uint256","name":"_balanceB","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"fid","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCurveSettings","outputs":[{"components":[{"internalType":"address","name":"deployer","type":"address"},{"internalType":"uint112","name":"deployerReward","type":"uint112"},{"internalType":"address","name":"g8keepFeeWallet","type":"address"},{"internalType":"uint16","name":"g8keepFee","type":"uint16"},{"internalType":"uint112","name":"liquidityShift","type":"uint112"},{"internalType":"uint16","name":"liquiditySupplementFee","type":"uint16"},{"internalType":"uint112","name":"migrationMinimumLiquidity","type":"uint112"},{"internalType":"address","name":"migrationPositionManager","type":"address"},{"internalType":"uint24","name":"migrationFeeTier","type":"uint24"},{"internalType":"uint40","name":"genesisTime","type":"uint40"},{"internalType":"uint40","name":"snipeProtectionEnd","type":"uint40"},{"internalType":"uint40","name":"snipeProtectionSeconds","type":"uint40"},{"internalType":"uint40","name":"snipeProtectionHeavySeconds","type":"uint40"},{"internalType":"uint8","name":"snipeProtectionHeavyExponentStart","type":"uint8"},{"internalType":"address","name":"pairAddress","type":"address"},{"internalType":"address","name":"lpLocker","type":"address"}],"internalType":"struct CurveSettings","name":"curveSettings","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"getCurveStatus","outputs":[{"components":[{"internalType":"uint112","name":"reserve0","type":"uint112"},{"internalType":"uint112","name":"reserve1","type":"uint112"}],"internalType":"struct g8keepBondingCurve.Reserves","name":"_aReserve","type":"tuple"},{"components":[{"internalType":"uint112","name":"reserve0","type":"uint112"},{"internalType":"uint112","name":"reserve1","type":"uint112"}],"internalType":"struct g8keepBondingCurve.Reserves","name":"_bReserve","type":"tuple"},{"internalType":"uint256","name":"_liquiditySupplement","type":"uint256"},{"internalType":"uint256","name":"_minimumLiquiditySupplement","type":"uint256"},{"internalType":"bool","name":"_curveLiquidityMet","type":"bool"},{"internalType":"bool","name":"_curveVolumeMet","type":"bool"},{"internalType":"bool","name":"_curveMigrated","type":"bool"},{"internalType":"bool","name":"_migrationFailed","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"image","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"maxBuyWithoutPenalty","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint112","name":"amount","type":"uint112"},{"internalType":"uint112","name":"minimumOut","type":"uint112"}],"name":"sell","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"_totalSupply","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"int256","name":"amount0Delta","type":"int256"},{"internalType":"int256","name":"amount1Delta","type":"int256"},{"internalType":"bytes","name":"","type":"bytes"}],"name":"uniswapV3SwapCallback","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"withdrawExcess","outputs":[],"stateMutability":"nonpayable","type":"function"},{"stateMutability":"payable","type":"receive"}]




connect = Web3(Web3.HTTPProvider('https://base-mainnet.infura.io/v3/b85969aaf3834a839de1811356c099a6'))


def Alert(hash,token,action):
        bot_token = '6880639936:AAEAz6H3X8cBOP9pNJWh3zljPrtBsQlX4No'
        hashLink = f'https://basescan.org/tx/{hash}'
        tradeInfo = f'TRADE(BASE) NOTIFICATION  \n\n'\
                    f'CLICK <a href="{hashLink}">HASH </a> TO VIEW TRANSCTION\n\n'\
                    f'{action}:{token}\n\n'
                    
        async def main():
            try:
                bot=telegram.Bot(bot_token)
            except:
                bot=telegram.Bot(bot_token)
            async with bot:
                await bot.send_message(text=tradeInfo,parse_mode=ParseMode.HTML,chat_id=963648721)
        if __name__=='__main__':
            asyncio.run(main())


def failed_to_trade(token,e,action):
        bot_token = '6344573464:AAF_dIkl-hJ5aFT_f0IbUMCmwtOhIm41tvc'
        async def main():
            try:
                bot=telegram.Bot(bot_token)
            except:
                bot=telegram.Bot(bot_token)
            async with bot:
                await bot.send_message(text=f'Failure : {action}\n\n\nnToken: {token}\n\nERROR:{e}',
                chat_id=963648721)
        if __name__=='__main__':
            asyncio.run(main())



def verifyHash(hash):
        topic = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
        invalidhash = 0
        while True:
            try:
                receipt = connect.eth.get_transaction_receipt(hash)
                logs = receipt.get('logs',[])
                topics = ['0x'+log['topics'][0].hex() for log in logs]
                if topic in topics :
                    print('Transaction Is Successfull')
                    break  
            except Exception as e:
                if invalidhash == 20:
                    break
                print('Transaction Not Yet Mined')
                invalidhash += 1
                time.sleep(4)


def required(priv,token):
    contract = connect.eth.contract(address=connect.to_checksum_address(token),abi=abi)
    account = Account.from_key(priv) 
    balance = connect.eth.get_balance(account.address)/10**18
    if balance <= 0.001:
        print('insufficient balance')
        action = 'Checking Eth Blance'
        error = 'Insufficient Eth'
        failed_to_trade(token,error,action)
        sys.exit()
    return contract,account



def tokenList(token):
    with open('G8keep.txt','a') as TokenFile:
        TokenFile.write(token+'\n')


def buy(token,priv):
    contract,account = required(priv,token)
    try:
        transaction = contract.functions.buy(
            account.address,
            1*10**18
            ).build_transaction({
                'from': account.address,
                'value': connect.to_wei('0.00018','ether'),
                'gas':200000,
                'maxPriorityFeePerGas': connect.to_wei('0.06','gwei'),
                'maxFeePerGas': connect.to_wei('0.1', 'gwei'),
                'nonce': connect.eth._get_transaction_count(account.address)
            })

        sign = connect.eth.account.sign_transaction(transaction,priv)
        send = connect.eth.send_raw_transaction(sign.raw_transaction)
        hash = '0x'+send.hex()
        action = 'Token bought'
        print(hash)
        verifyHash(hash)
        Alert(hash,token,action)
        tokenList(token)
    except Exception as e:
        print('Error is because of {e}')
        action = 'Token Buying'
        failed_to_trade(token,e,action)

def sell(token,priv):
    contract,account = required(priv,token)
    try:
        transaction = contract.functions.sell(
            account.address,
            1*10**18
            ).build_transaction({
                'from': account.address,
                #'value': connect.to_wei('0.00018','ether'),
                'gas':200000,
                'maxPriorityFeePerGas': connect.to_wei('0.06','gwei'),
                'maxFeePerGas': connect.to_wei('0.2', 'gwei'),
                'nonce': connect.eth._get_transaction_count(account.address)
            })

        sign = connect.eth.account.sign_transaction(transaction,priv)
        send = connect.eth.send_raw_transaction(sign.raw_transaction)
        hash = '0x'+send.hex()
        action = 'Token bought'
        print(hash)
        verifyHash(hash)
        Alert(hash,token,action)
        tokenList(token)
    except Exception as e:
        print('Error is because of {e}')
        action = 'Token Buying'
        failed_to_trade(token,e,action)




def check_balance(contract,account):
    balance = contract.functions.balanceOf(account.address).call()
    return balance


def sell(priv,token):
    contract,account = required(priv,token)
    balance = check_balance(contract,account)
    amountTo_sell = balance/2
    try:
        transaction = contract.functions.sell(
            int(amountTo_sell),
            int(0.0000000001*10**18)
            ).build_transaction({
                'from': account.address,
                'gas':200000,
                'maxPriorityFeePerGas': connect.to_wei('0.06','gwei'),
                'maxFeePerGas': connect.to_wei('0.1', 'gwei'),
                'nonce': connect.eth._get_transaction_count(account.address)
            })

        sign = connect.eth.account.sign_transaction(transaction,priv)
        send = connect.eth.send_raw_transaction(sign.raw_transaction)
        hash = '0x'+send.hex()
        action = 'Token Sold'
        print(hash)
        verifyHash(hash)
        Alert(hash,token,action)
    except Exception as e:
        print('Error is because of {e}')
        action = 'Token Selling'
        failed_to_trade(token,e,action)





walletCommand = sys.argv[1]
token = sys.argv[2]
if walletCommand == 'first_bot':
    priv = os.environ.get('first_bot')
    buy(token,priv)
    time.sleep(600)
    sell(priv,token)
    
elif walletCommand == 'second_bot':
    priv = os.environ.get('second_bot')
    buy(token,priv)
    time.sleep(600)
    sell(priv,token)

elif walletCommand == 'third_bot':
    priv = os.environ.get('first_bot')
    buy(token,priv)
    time.sleep(600)
    sell(priv,token)