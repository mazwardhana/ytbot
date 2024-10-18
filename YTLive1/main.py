# TOOL INI MENGGUNAKAN OAUTH PLAYGROUND BUKAN SELENIUM JADI LEBIH SIMPEL DAN MUDAH DI GUNAKAN 

# HARGA MURAH KUALITAS MURAH
##############################
# HANYA BISA MENGIRIM 200 PESAN PER HARI DAN PER AKUN

# BISA MENGIRIM PESAN LAGI BESOK HARI DI RISET JAM 3-4 SORE
##############################
#
# Termux install 
# pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client rich

# Ubuntu install ( VPS OTHER )
# pip3 install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client rich

###### MOHON UNTUK TIDAK MENGHAPUS ATAU MENGUBAH APAPUN DARI FILE 𝙙𝙗.𝙩𝙭𝙩
###### UNTUK MENAMBAHKAN AKUN BACA FILE 𝙏𝙖𝙢𝙗𝙖𝙝𝙠𝙖𝙣 𝙖𝙠𝙪𝙣.𝙩𝙭𝙩 ATAU 𝘽𝙖𝙘𝙖 𝙞𝙣𝙞.𝙩𝙭𝙩

import google.oauth2.credentials
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
import threading
import time
import re
import sys
import os
import random
from rich.console import Console

def ychat(chat):
    for yt in chat + '\n':
        sys.stdout.write(yt)
        sys.stdout.flush()
        time.sleep(0.003)

def yt(chat):
    for yt in chat + '\n':
        sys.stdout.write(yt)
        sys.stdout.flush()
        time.sleep(0.1)

os.system("clear")
print("                                         ")

def read_accounts_from_file(file_path):
    accounts = []
    with open(file_path, "r") as file:
        account_data = {}
        for line in file:
            line = line.strip()
            if line:
                key, value = line.split("=")
                account_data[key] = value
            else:
                if account_data:
                    accounts.append(account_data)
                    account_data = {}
        if account_data:
            accounts.append(account_data)
    return accounts

def add_account_to_file(file_path, access_token, refresh_token, client_id, client_secret):
    with open(file_path, "a") as file:
        file.write(f"\naccess_token={access_token}\n")
        file.write(f"refresh_token={refresh_token}\n")
        file.write(f"client_id={client_id}\n")
        file.write(f"client_secret={client_secret}\n\n")
    ychat("                                                 ")
    ychat("  [+] Account successfully added to database")
    time.sleep(3)

def extract_video_id(input_text):
    match = re.search(r"(?:v=|\/live\/|\/embed\/|\/watch\?v=|\/\?v=|\/)([a-zA-Z0-9_-]{11})", input_text)
    if match:
        return match.group(1)
    return input_text

def extract_channel_id(input_text):
    if "youtube.com" in input_text:
        match = re.search(r"(?:\/channel\/|\/user\/|\/c\/|\/@)([a-zA-Z0-9_-]+)", input_text)
        if match:
            return match.group(1)
    return input_text

def get_authenticated_service(account):
    credentials = google.oauth2.credentials.Credentials(
        token=account["access_token"],
        refresh_token=account["refresh_token"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=account["client_id"],
        client_secret=account["client_secret"],
        scopes=["https://www.googleapis.com/auth/youtube.force-ssl"]
    )

    if credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    
    return build("youtube", "v3", credentials=credentials)

def extract_username(url):
    match = re.search(r'(?<=\/@)([a-zA-Z0-9_-]+)', url)
    if match:
        return f"@{match.group(1)}"
    return None

def get_channel_id_from_username(youtube, username):
    try:
        response = youtube.search().list(
            part="snippet",
            q=username,
            type="channel"
        ).execute()

        if "items" in response and len(response["items"]) > 0:
            return response["items"][0]["snippet"]["channelId"]
        else:
            yt(f"          [-] No channel found for username: {username}")
            sys.exit()
    except Exception as e:
        yt(f"          [-] Error fetching channel ID: {e}")
        sys.exit()

def get_channel_id(youtube, channel_input):
    if "youtube.com" in channel_input:
        
        username = extract_username(channel_input)
        if username:
            return get_channel_id_from_username(youtube, username)
        else:
            yt(f"          [-] No username found in URL: {channel_input}")
            sys.exit()
    else:
        return get_channel_id_from_username(youtube, channel_input)


def get_live_chat_id(youtube, video_id):
    response = youtube.videos().list(
        part="liveStreamingDetails",
        id=video_id
    ).execute()
    
    live_chat_id = response["items"][0]["liveStreamingDetails"]["activeLiveChatId"]
    return live_chat_id

failed_to_subscribe = False

def subscribe_to_channel(youtube, channel_id):
    global failed_to_subscribe 
    try:
        youtube.subscriptions().insert(
            part="snippet",
            body={
                "snippet": {
                    "resourceId": {
                        "kind": "youtube#channel",
                        "channelId": channel_id
                    }
                }
            }
        ).execute()
        print(f"          [+] Subscribed to channel: {channel_id}")
    except Exception as e:
        if not failed_to_subscribe:
            print(f"          [-] Failed to subscribe")
            failed_to_subscribe = True  



def process_account(account, video_id, message, channel_id):
    youtube = get_authenticated_service(account)
    
    subscribe_to_channel(youtube, channel_id)

    return youtube  

def wait_after_subscribe(sleep_time):
    print(f"          [+] Now waiting {sleep_time} seconds")
    time.sleep(sleep_time)  
    print(f"          [+] We are loading the client...")
    

def send_message(youtube, live_chat_id, message, client_secret):
    youtube.liveChatMessages().insert(
        part="snippet",
        body={
            "snippet": {
                "liveChatId": live_chat_id,
                "type": "textMessageEvent",
                "textMessageDetails": {
                    "messageText": message
                }
            }
        }
    ).execute()
    accounts = read_accounts_from_file("db.txt")
    device = random_device_name()
    masked_client_secret = mask_client_secret(client_secret)
    print(f"          \033[35m[+]\033[0m \033[37mBroadcast to\033[0m \033[35m{len(accounts)}\033[0m \033[37mClients 🔥 | .......\033[0m{masked_client_secret} \033[37m| \033[0m \033[35m{device}\033[0m")

def random_device_name():
    devices = [
        "iPhone 12", "Samsung Galaxy S21", "Google Pixel 5", "Xiaomi Mi 11", 
        "OnePlus 9", "Huawei P40", "Oppo Find X3", "Sony Xperia 1", 
        "Realme GT 2 Pro", "OnePlus 9 Pro", "Huawei P30 Pro"
    ]
    return random.choice(devices)

def mask_client_secret(client_secret):
    return '.......' + client_secret[-11:]
    

console = Console()

def ychat(message):
    console.print(message, style="bold cyan")

def yt(message):
    console.print(message, style="bold yellow")

def main_menu():
    while True:
        os.system("clear")
        ychat("                                             ")
        accounts = read_accounts_from_file("db.txt")
        ychat("                                             ")
        ychat("[white]         | APP023 [red]YouTube [white]Live chat - The Spammer is Reborn[/white]")
        ychat("         [white]|\\				")
        ychat("[white]         |\\______|  [red][[white]+[red]][red] [white]YouTube Live Chat V2.0 🔥 - @RosarioBNB__2.0[/white]")
        ychat(f"[white]         |\\______|  [red][[white]+[red][red]] [white]Client both: - [green]{len(accounts)} ⚡[/white]")
        ychat(f"[white]         |\\______| [red] [[white]+[red]][white] Version: [green]-Troll {len(accounts)} [red]| [green]V2.0 NEW ⚡[/white]")
        ychat("[white]         |\\______| [red] [[white]+[red]][red] [white]Developer: -@RosarioBNB__2.0 / Telegram 🗨️[/white]")
        ychat("[white]         |\\______|  [red][[white]+[red]][red] [white]Made just to troll people in Live Chat 📍[/white]")
        ychat("         [white]|\\_________________________________________________[white]")
        ychat("        [white] |\\")
        ychat("[white]         |\\______|  [red] [[white]1[red]] [white]Add account/client 📍 [/white]")
        ychat("[white]         |\\______|  [red] [[white]2[red]] [white]Available client 👾[/white]")
        ychat("[white]         |\\______|  [red] [[white]3[red]] [white]YouTube Live Chat (__[green]New`1.2[white]__) 🗨️ [/white]")
        ychat("[white]         |\\______|  [red] [[white]4[red]] [white]YouTube Live Chat (Subscribe mode__[green]New`1.3[white]) 🗨️ [/white]")
        ychat("[white]         |\\______|  [red] [[white]5[red]] [white]Troll Spammer 🗨️ (Beta)[/white]")  
        ychat("[white]         |\\______|  [red] [[white]6[red]] Logout 💣[/white]")
        ychat("         [white]|\\_______________________________________________________________________[white]")
        ychat("         [white]|_____________________The latest version of YouTube Troll [red]```[green]07/10/24")
        ychat("         [white]|_____________________API will be available")
        ychat("         [white]|_____________________[red]@[white]RosarioBNB [red]- [white]Contact me on telegram")
        ychat("         [white]|__________| Engineered using Selenium ❤️")
        ychat("         ")
        choice = input("          [+] @RosarioBNB [YTLC]: ")

        if choice == "1":
            ychat("                                           ")
            access_token = input("          [+] Enter Access Token: ")
            refresh_token = input("          [+] Enter Refresh Token: ")
            client_id = input("          [+] Enter Client ID: ")
            client_secret = input("          [+] Enter Client Secret: ")

            add_account_to_file("db.txt", access_token, refresh_token, client_id, client_secret)

        elif choice == "2":
            accounts = read_accounts_from_file("db.txt")
            yt(f"          [+] There are {len(accounts)} client in database")
            time.sleep(3)

        elif choice == "3":
            ychat("                                           ")
            input_video = input("          [+] Enter Video ID or URL: ")
            video_id = extract_video_id(input_video)
            message = input("          [+] Enter message: ")
            
            try:
                loop_count = int(input("          [+] Enter the number of times to send the message: "))
            except ValueError:
                print("          [-] Invalid input! Please enter a valid number.")
                return  
            for _ in range(loop_count):
                threads = []
                error_messages = []  
                for account in accounts:
                    def thread_function(a):
                        try:
                            service = get_authenticated_service(a)
                            live_chat_id = get_live_chat_id(service, video_id)
                            send_message(service, live_chat_id, message, a["client_secret"])
                        except Exception as e:
                            error_messages.append(f"          [-] Error sending message...{e}")
                            time.sleep(4)

                    thread = threading.Thread(target=thread_function, args=(account,))
                    threads.append(thread)
                    thread.start()

                for thread in threads:
                    thread.join()

                if error_messages:
                    for error in error_messages:
                        print(error)

                print(f"          [+] Message sent! {loop_count - _ - 1} loops remaining.")


        elif choice == "4":
            ychat("                                           ")
            input_video = input("          [+] Enter Video ID or URL: ")
            video_id = extract_video_id(input_video)
            channel_input = input("          [+] Enter Channel ID or URL: ")
            youtube = get_authenticated_service(accounts[0])
            channel_id = get_channel_id(youtube, channel_input)
            
            sleep_time = input("          [+] Enter time (in seconds, default 300): ")
            if not sleep_time.isdigit():
                sleep_time = 300 
            else:
                sleep_time = int(sleep_time)

            while True:
                try:
                    message = input("          [+] Enter message (or type 'back' to back): ")
                    if message.lower() == "back":
                        break
                    ychat("				")
                    
                    threads = []
                    waiting_messages = []  
                    for account in accounts:
                        thread = threading.Thread(target=lambda q, a: q.append(process_account(a, video_id, message, channel_id)), args=(waiting_messages, account))
                        threads.append(thread)
                        thread.start()

                    for thread in threads:
                        thread.join()

                    
                    wait_after_subscribe(sleep_time)

                    
                    for account in accounts:
                        try:
                            youtube = get_authenticated_service(account)
                            live_chat_id = get_live_chat_id(youtube, video_id)
                            send_message(youtube, live_chat_id, message, account["client_secret"])
                        except Exception as e:
                            print(f"          [-] Error sending message...")

                    yt("          [+] All clients have done the task...")
                
                except Exception as e:
                    print(f"          [-] An error occurred")
                    yt("          [+] Continuing execution despite the error.")

        elif choice == "5":
            
            yt("          [+] Troll Spammer feature is not yet implemented.")
            time.sleep(3)

        elif choice == "6":
            yt("          [+] Logout process initiated.")
            break

if __name__ == "__main__":
    main_menu()

