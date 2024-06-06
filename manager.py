import asyncio
from telethon import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
import pickle
import os
from colorama import init, Fore
import requests

init()

n = Fore.RESET
lg = Fore.LIGHTGREEN_EX
r = Fore.RED
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [lg, r, w, cy, ye]

def banner():
    import random
    b = [
        '░██████╗███████╗████████╗██╗░░░██╗██████╗░',
        '██╔════╝██╔════╝╚══██╔══╝██║░░░██║██╔══██╗',
        '╚█████╗░█████╗░░░░░██║░░░██║░░░██║██████╔╝',
        '░╚═══██╗██╔══╝░░░░░██║░░░██║░░░██║██╔═══╝░',
        '██████╔╝███████╗░░░██║░░░╚██████╔╝██║░░░░░',
        '╚═════╝░╚══════╝░░░╚═╝░░░░╚═════╝░╚═╝░░░░░'
    ]
    for char in b:
        print(f'{random.choice(colors)}{char}{n}')
    print('Contact below address for get premium script')
    print(f'{lg}Version: {w}2.0{lg} | GitHub: {w}@saifalisew1508{n}')
    print(f'{lg}Telegram: {w}@DearSaif{lg} | Instagram: {w}@_Prince.Babu_{n}')

def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def save_accounts_to_file(accounts):
    with open('vars.txt', 'wb') as f:
        for account in accounts:
            pickle.dump(account, f)

def load_accounts_from_file():
    accounts = []
    with open('vars.txt', 'rb') as f:
        while True:
            try:
                accounts.append(pickle.load(f))
            except EOFError:
                break
    return accounts

async def main():
    while True:
        clr()
        banner()
        print(f'{lg}[1] Add new accounts{n}')
        print(f'{lg}[2] Filter all banned accounts{n}')
        print(f'{lg}[3] Delete specific accounts{n}')
        print(f'{lg}[4] Update your Script{n}')
        print(f'{lg}[5] Display All Accounts{n}')
        print(f'{lg}[6] Quit{n}')
        a = int(input('\nEnter your choice: '))

        if a == 1:
            new_accs = []
            with open('vars.txt', 'ab') as g:
                number_to_add = int(input(f'\n{lg} [~] Enter How Many Accounts You Want To Add: {r}'))
                for _ in range(number_to_add):
                    phone_number = str(input(f'\n{lg} [~] Enter Phone Number With Country Code: {r}'))
                    parsed_number = ''.join(phone_number.split())
                    pickle.dump([parsed_number], g)
                    new_accs.append(parsed_number)
                print(f'\n{lg} [i] Saved all accounts in vars.txt{n}')
                clr()
                print(f'\n{lg} [*] Logging in from new accounts\n{n}')
                for number in new_accs:
                    c = TelegramClient(f'sessions/{number}', 'API_ID', 'API_HASH')
                    await c.start(phone=number)
                    print(f'{lg}[+] Login successful{n}')
                    await c.disconnect()
                input(f'\n Press enter to goto main menu...')

        elif a == 2:
            accounts = load_accounts_from_file()
            banned_accs = []
            if not accounts:
                print(f'{r}[!] There are no accounts! Please add some and retry{n}')
                sleep(3)
            else:
                for account in accounts:
                    phone = str(account[0])
                    client = TelegramClient(f'sessions/{phone}', 'API_ID', 'API_HASH')
                    await client.connect()
                    if not await client.is_user_authorized():
                        try:
                            await client.send_code_request(phone)
                            print(f'{lg}[+] {phone} is not banned{n}')
                        except PhoneNumberBannedError:
                            print(f'{r}{phone} is banned!{n}')
                            banned_accs.append(account)
                if not banned_accs:
                    print(f'{lg}Congrats! No banned accounts{n}')
                else:
                    accounts = [acc for acc in accounts if acc not in banned_accs]
                    save_accounts_to_file(accounts)
                    print(f'{lg}[i] All banned accounts removed{n}')
                input('\nPress enter to goto main menu...')

        elif a == 3:
            accs = load_accounts_from_file()
            print(f'{lg}[i] Choose an account to delete\n{n}')
            for i, acc in enumerate(accs):
                print(f'{lg}[{i}] {acc[0]}{n}')
            index = int(input(f'\n{lg}[+] Enter a choice: {n}'))
            phone = str(accs[index][0])
            session_file = f'sessions/{phone}.session'
            if os.path.exists(session_file):
                os.remove(session_file)
            del accs[index]
            save_accounts_to_file(accs)
            print(f'\n{lg}[+] Account Deleted{n}')
            input(f'\nPress enter to goto main menu...')

        elif a == 4:
            print(f'\n{lg}[i] Checking for updates...{n}')
            try:
                version = requests.get('https://raw.githubusercontent.com/saifalisew1508/Telegram-Members-Adder/main/version.txt')
            except:
                print(f'{r} You are not connected to the internet{n}')
                print(f'{r} Please connect to the internet and retry{n}')
                exit()
            if float(version.text) > 2.0:
                prompt = str(input(f'{lg}[~] Update available [Version {version.text}]. Download? [y/n]: {r}'))
                if prompt.lower() in {'y', 'yes'}:
                    print(f'{lg}[i] Downloading updates...{n}')
                    os.system('curl -O https://raw.githubusercontent.com/saifalisew1508/Telegram-Members-Adder/main/add.py')
                    os.system('curl -O https://raw.githubusercontent.com/saifalisew1508/Telegram-Members-Adder/main/manager.py')
                    print(f'{lg}[*] Updated to version: {version.text}{n}')
                    input('Press enter to exit...')
                    exit()
                else:
                    print(f'{lg}[!] Update aborted.{n}')
                    input('Press enter to goto main menu...')
            else:
                print(f'{lg}[i] Your Telegram-Members-Adder is already up to date{n}')
                input('Press enter to goto main menu...')

        elif a == 5:
            accs = load_accounts_from_file()
            print(f'\n{cy}')
            print(f'\tList Of Phone Numbers Are')
            print('==========================================================')
            for z in accs:
                print(f'\t{z[0]}')
            print('==========================================================')
            input('\nPress enter to goto main menu')

        elif a == 6:
            clr()
            banner()
            exit()
