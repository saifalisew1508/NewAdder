import os
import pickle
import random
import requests
from time import sleep
from colorama import init, Fore
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import PhoneNumberBannedError
from telethon.errors import SessionPasswordNeededError

init()

n = Fore.RESET
lg = Fore.LIGHTGREEN_EX
r = Fore.RED
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [lg, r, w, cy, ye]

API_ID = 3910389  # Your API ID here
API_HASH = '86f861352f0ab76a251866059a6adbd6'  # Your API Hash here

def banner():
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

def get_accounts():
    accounts = []
    if os.path.exists('vars.txt'):
        with open('vars.txt', 'rb') as f:
            while True:
                try:
                    accounts.append(pickle.load(f))
                except EOFError:
                    break
    return accounts

def save_accounts(accounts):
    with open('vars.txt', 'wb') as f:
        for account in accounts:
            pickle.dump(account, f)

async def add_accounts():
    new_accs = []
    with open('vars.txt', 'ab') as g:
        number_to_add = int(input(f'\n{lg} [~] Enter How Many Accounts You Want To Add: {r}'))
        for _ in range(number_to_add):
            phone_number = str(input(f'\n{lg} [~] Enter Phone Number With Country Code: {r}'))
            parsed_number = ''.join(phone_number.split())
            pickle.dump([parsed_number], g)
            new_accs.append(parsed_number)
        print(f'\n{lg} [i] Saved all accounts in vars.txt')
        clr()
        print(f'\n{lg} [*] Logging in from new accounts\n')
        for number in new_accs:
            client = TelegramClient(f'sessions/{number}', API_ID, API_HASH)
            await client.connect()
            if not await client.is_user_authorized():
                await client.send_code_request(number)
                try:
                    await client.sign_in(number, input(f'Enter the code for {number}: '))
                except SessionPasswordNeededError:
                    await client.sign_in(password=input(f'Password for {number}: '))
            print(f'{lg}[+] Login successful')
            await client.disconnect()
        input(f'\nPress enter to goto main menu...')

async def filter_banned_accounts():
    accounts = get_accounts()
    if not accounts:
        print(f'{r}[!] There are no accounts! Please add some and retry')
        sleep(3)
        return

    banned_accs = []
    for account in accounts:
        phone = str(account[0])
        client = TelegramClient(f'sessions/{phone}', API_ID, API_HASH)
        await client.connect()
        if not await client.is_user_authorized():
            try:
                await client.send_code_request(phone)
                print(f'{lg}[+] {phone} is not banned{n}')
            except PhoneNumberBannedError:
                print(r + phone + ' is banned!' + n)
                banned_accs.append(account)
        await client.disconnect()

    if not banned_accs:
        print(f'{lg}Congrats! No banned accounts')
    else:
        for banned_acc in banned_accs:
            accounts.remove(banned_acc)
        save_accounts(accounts)
        print(f'{lg}[i] All banned accounts removed{n}')
    input('\nPress enter to goto main menu...')

def delete_specific_account():
    accounts = get_accounts()
    if not accounts:
        print(f'{r}[!] There are no accounts! Please add some and retry')
        sleep(3)
        return

    print(f'{lg}[i] Choose an account to delete\n')
    for i, account in enumerate(accounts):
        print(f'{lg}[{i}] {account[0]}{n}')
    index = int(input(f'\n{lg}[+] Enter a choice: {n}'))
    phone = str(accounts[index][0])
    session_file = f'sessions/{phone}.session'
    if os.path.exists(session_file):
        os.remove(session_file)
    del accounts[index]
    save_accounts(accounts)
    print(f'\n{lg}[+] Account Deleted{n}')
    input(f'\nPress enter to goto main menu...')

def check_for_updates():
    print(f'\n{lg}[i] Checking for updates...')
    try:
        version = requests.get('https://raw.githubusercontent.com/saifalisew1508/Telegram-Members-Adder/main/version.txt')
    except:
        print(f'{r} You are not connected to the internet')
        print(f'{r} Please connect to the internet and retry')
        exit()

    if float(version.text) > 2.0:
        prompt = str(input(f'{lg}[~] Update available[Version {version.text}]. Download?[y/n]: {r}'))
        if prompt.lower() in {'y', 'yes'}:
            print(f'{lg}[i] Downloading updates...')
            if os.name == 'nt':
                os.system('del add.py')
                os.system('del manager.py')
            else:
                os.system('rm add.py')
                os.system('rm manager.py')
            os.system('curl -l -O https://raw.githubusercontent.com/saifalisew1508/Telegram-Members-Adder/main/add.py')
            os.system('curl -l -O https://raw.githubusercontent.com/saifalisew1508/Telegram-Members-Adder/main/manager.py')
            print(f'{lg}[*] Updated to version: {version.text}')
            input('Press enter to exit...')
            exit()
        else:
            print(f'{lg}[!] Update aborted.')
            input('Press enter to goto main menu...')
    else:
        print(f'{lg}[i] Your Telegram-Members-Adder is already up to date')
        input('Press enter to goto main menu...')

def display_all_accounts():
    accounts = get_accounts()
    if not accounts:
        print(f'{r}[!] There are no accounts! Please add some and retry')
        sleep(3)
        return

    print(f'\n{cy}')
    print(f'\tList Of Phone Numbers Are')
    print('==========================================================')
    for account in accounts:
        print(f'\t{account[0]}')
    print('==========================================================')
    input('\nPress enter to goto main menu')

async def main_menu():
    while True:
        clr()
        banner()
        print(f'{lg}[1] Add new accounts{n}')
        print(f'{lg}[2] Filter all banned accounts{n}')
        print(f'{lg}[3] Delete specific accounts{n}')
        print(f'{lg}[4] Update your Script{n}')
        print(f'{lg}[5] Display All Accounts{n}')
        print(f'{lg}[6] Quit{n}')
        choice = int(input('\nEnter your choice: '))
        if choice == 1:
            await add_accounts()
        elif choice == 2:
            await filter_banned_accounts()
        elif choice == 3:
            delete_specific_account()
        elif choice == 4:
            check_for_updates()
        elif choice == 5:
            display_all_accounts()
        elif choice == 6:
            clr()
            banner()
            exit()
        else:
            print(f'{r}Invalid choice! Please try again.{n}')
            sleep(2)
