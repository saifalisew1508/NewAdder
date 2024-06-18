import os
import sys
import time
import pickle
import random
import asyncio
from colorama import init, Fore
from telethon.sync import TelegramClient
from telethon.errors.rpcerrorlist import (
    PeerFloodError, UserPrivacyRestrictedError, PhoneNumberBannedError,
    ChatAdminRequiredError, ChatWriteForbiddenError, UserBannedInChannelError,
    UserAlreadyParticipantError, FloodWaitError
)
from telethon.tl.functions.channels import InviteToChannelRequest, JoinChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest, AddChatUserRequest
from telethon.tl.types import InputPeerChannel

init()

# Define colors for output
r = Fore.RED
lg = Fore.GREEN
rs = Fore.RESET
w = Fore.WHITE
cy = Fore.CYAN
ye = Fore.YELLOW
colors = [r, lg, w, ye, cy]

# Output styles
info = f'{lg}[{w}i{lg}]{rs}'
error = f'{lg}[{r}!{lg}]{rs}'
success = f'{w}[{lg}*{w}]{rs}'
INPUT = f'{lg}[{cy}~{lg}]{rs}'
plus = f'{w}[{lg}+{w}]{rs}'
minus = f'{w}[{lg}-{w}]{rs}'

# Telegram API details
API_ID = 3910389  # Replace with your API ID
API_HASH = '86f861352f0ab76a251866059a6adbd6'  # Replace with your API Hash

def banner():
    b = [
        '░█████╗░██████╗░██████╗░███████╗██████╗░',
        '██╔══██╗██╔══██╗██╔══██╗██╔════╝██╔══██╗',
        '███████║██║░░██║██║░░██║█████╗░░██████╔╝',
        '██╔══██║██║░░██║██║░░██║██╔══╝░░██╔══██╗',
        '██║░░██║██████╔╝██████╔╝███████╗██║░░██║',
        '╚═╝░░╚═╝╚═════╝░╚═════╝░╚══════╝╚═╝░░╚═╝'
    ]
    for char in b:
        print(f'{random.choice(colors)}{char}{rs}')
    print('Contact below address for get premium script')
    print(f'{lg}Version: {w}2.0{lg} | GitHub: {w}@saifalisew1508{rs}')
    print(f'{lg}Telegram: {w}@DearSaif{lg} | Instagram: {w}@_Prince.Babu_{rs}')

def clr():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

async def check_banned_accounts(accounts):
    print('\n' + info + lg + ' Checking for banned accounts...' + rs)
    banned = []
    for a in accounts:
        phn = a[0]
        print(f'{plus}{Fore.LIGHTWHITE_EX} Checking {lg}{phn}')
        client = TelegramClient(f'sessions/{phn}', API_ID, API_HASH)
        await client.connect()
        if not await client.is_user_authorized():
            try:
                await client.send_code_request(phn)
                print('OK')
            except PhoneNumberBannedError:
                print(f'{error} {w}{phn} {r}is banned!{rs}')
                banned.append(a)
        await client.disconnect()
        time.sleep(0.5)

    for z in banned:
        accounts.remove(z)
        print(info + lg + ' Banned account removed [Remove permanently using manager.py]' + rs)

    return accounts

def log_status(scraped, index):
    with open('status.dat', 'wb') as f:
        pickle.dump([scraped, int(index)], f)
    print(f'{info}{lg} Session stored in {w}status.dat{lg}')

def exit_window():
    input(f'\n{cy} Press enter to exit...')
    clr()
    banner()
    sys.exit()

async def main():
    clr()
    banner()

    accounts = []
    with open('vars.txt', 'rb') as f:
        while True:
            try:
                accounts.append(pickle.load(f))
            except EOFError:
                break

    accounts = await check_banned_accounts(accounts)
    print(f'{info} Sessions created!')
    clr()
    banner()

    try:
        with open('status.dat', 'rb') as f:
            status = pickle.load(f)
        resume = input(f'{INPUT}{cy} Resume scraping members from {w}{status[0]}{lg}? [y/n]: {r}')
        if 'y' in resume:
            scraped_grp = status[0]
            index = int(status[1])
        else:
            os.remove('status.dat')
            scraped_grp = input(f'{INPUT}{cy} Public/Private group url link to scrape members: {r}')
            index = 0
    except:
        scraped_grp = input(f'{INPUT}{cy} Public/Private group url link to scrape members: {r}')
        index = 0

    print(f'{info}{lg} Total accounts: {w}{len(accounts)}')
    number_of_accs = int(input(f'{INPUT}{cy} How Many Accounts You Want Use In Adding: {r}'))
    print(f'{info}{cy} Choose an option{lg}')
    print(f'{cy}[0]{lg} Add to public group')
    print(f'{cy}[1]{lg} Add to private group')
    choice = int(input(f'{INPUT}{cy} Enter choice: {r}'))
    if choice == 0:
        target = str(input(f'{INPUT}{cy} Enter public group url link: {r}'))
    else:
        target = str(input(f'{INPUT}{cy} Enter private group url link: {r}'))

    print(f'{Fore.LIGHTWHITE_EX}_' * 50)
    status_choice = str(input(f'{INPUT}{cy} Do you wanna add active members?[y/n]: {r}'))
    to_use = list(accounts[:number_of_accs])
    for l in to_use: 
        accounts.remove(l)
    with open('vars.txt', 'wb') as f:
        for a in accounts:
            pickle.dump(a, f)
        for ab in to_use:
            pickle.dump(ab, f)

    sleep_time = int(input(f'{INPUT}{cy} Enter delay time per request{w}[{lg}0 for None, I suggest enter 30 to add members properly{w}]: {r}'))
    print(f'{info}{lg} Joining group from {w}{number_of_accs} accounts...')
    print(f'{Fore.LIGHTWHITE_EX}-' * 50)
    print(f'{success}{lg} -- Adding members from {w}{len(to_use)}{lg} account(s) --')

    adding_status = 0
    approx_members_count = 0

    for acc in to_use:
        stop = index + 60
        client = TelegramClient(f'sessions/{acc[0]}', API_ID, API_HASH)
        print(f'{plus}{Fore.LIGHTWHITE_EX} User: {cy}{acc[0]}{lg} -- {cy}Starting session...')
        await client.start(acc[0])
        acc_name = (await client.get_me()).first_name

        try:
            if '/joinchat/' in scraped_grp:
                g_hash = scraped_grp.split('/joinchat/')[1]
                try:
                    await client(ImportChatInviteRequest(g_hash))
                    print(f'{plus}{Fore.LIGHTWHITE_EX} User: {cy}{acc_name}{lg} -- Joined group to scrape')
                except UserAlreadyParticipantError:
                    pass
            else:
                await client(JoinChannelRequest(scraped_grp))
                print(f'{plus}{Fore.LIGHTWHITE_EX} User: {cy}{acc_name}{lg} -- Joined group to scrape')

            scraped_grp_entity = await client.get_entity(scraped_grp)
            if choice == 0:
                await client(JoinChannelRequest(target))
                print(f'{plus}{Fore.LIGHTWHITE_EX} User: {cy}{acc_name}{lg} -- Joined group to add')
                target_entity = await client.get_entity(target)
                target_details = InputPeerChannel(target_entity.id, target_entity.access_hash)
            else:
                try:
                    grp_hash = target.split('/joinchat/')[1]
                    await client(ImportChatInviteRequest(grp_hash))
                    print(f'{plus}{Fore.LIGHTWHITE_EX} User: {cy}{acc_name}{lg} -- Joined group to add')
                except UserAlreadyParticipantError:
                    pass
                target_entity = await client.get_entity(target)
                target_details = target_entity
        except Exception as e:
            print(f'{error}{r} User: {cy}{acc_name}{lg} -- Failed to join group')
            print(f'{error} {r}{e}')
            continue

        print(f'{plus}{Fore.LIGHTWHITE_EX} User: {cy}{acc_name}{lg} -- {cy}Retrieving entities...')
        await client.get_dialogs()

        try:
            members = await client.get_participants(scraped_grp_entity, aggressive=False)
        except Exception as e:
            print(f'{error}{r} Couldn\'t scrape members')
            print(f'{error}{r} {e}')
            continue

        approx_members_count = len(members)
        assert approx_members_count != 0

        if index >= approx_members_count:
            print(f'{error}{lg} No members to add!')
            continue

        print(f'{info}{lg} Start: {w}{index}')
        adding_status = 0
        peer_flood_status = 0

        for user in members[index:stop]:
            index += 1
            if peer_flood_status == 10:
                print(f'{error}{r} Too many Peer Flood Errors! Closing session...')
                break
            try:
                if choice == 0:
                    await client(InviteToChannelRequest(target_details, [user]))
                else:
                    await client(AddChatUserRequest(target_details.id, user, 42))

                user_id = user.first_name
                target_title = target_entity.title
                print(f'{plus}{Fore.LIGHTWHITE_EX} User: {cy}{acc_name}{lg} -- {cy}{user_id} {lg}--> {cy}{target_title}')
                adding_status += 1
                print(f'{info}{Fore.LIGHTWHITE_EX} User: {cy}{acc_name}{lg} -- Sleep {w}{sleep_time} {lg}second(s)')
                await asyncio.sleep(sleep_time)
            except UserPrivacyRestrictedError:
                print(f'{minus}{Fore.LIGHTWHITE_EX} User: {cy}{acc_name}{lg} -- {r}User Privacy Restricted Error')
                continue
            except PeerFloodError:
                print(f'{error}{Fore.LIGHTWHITE_EX} User: {cy}{acc_name}{lg} -- {r}Peer Flood Error.')
                peer_flood_status += 1
                continue
            except ChatWriteForbiddenError:
                print(f'{error}{r} Can\'t add to group. Contact group admin to enable members adding')
                if index < approx_members_count:
                    log_status(scraped_grp, index)
                exit_window()
            except UserBannedInChannelError:
                print(f'{error}{Fore.LIGHTWHITE_EX} User: {cy}{acc_name}{lg} -- {r}Banned from writing in groups')
                break
            except ChatAdminRequiredError:
                print(f'{error}{Fore.LIGHTWHITE_EX} User: {cy}{acc_name}{lg} -- {r}Chat Admin rights needed to add')
                break
            except UserAlreadyParticipantError:
                print(f'{minus}{Fore.LIGHTWHITE_EX} User: {cy}{acc_name}{lg} -- {r}User is already a participant')
                continue
            except FloodWaitError as e:
                print(f'{error}{r} {e}')
                break
            except ValueError:
                print(f'{error}{r} Error in Entity')
                continue
            except KeyboardInterrupt:
                print(f'{error}{r} ---- Adding Terminated ----')
                if index < len(members):
                    log_status(scraped_grp, index)
                exit_window()
            except Exception as e:
                print(f'{error} {e}')
                continue

        if adding_status != 0:
            print(f"\n{info}{lg} Adding session ended")

        try:
            if index < approx_members_count:
                log_status(scraped_grp, index)
                exit_window()
        except:
            exit_window()
