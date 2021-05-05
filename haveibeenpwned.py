#!/usr/bin/python

import requests, os, cloudscraper, pathlib, hashlib
from colorama import init, Fore, Back, Style
from pathlib import Path

init(convert=True)
scraper = cloudscraper.create_scraper()


def banner():
    os.system("cls")
    e = f"""{Style.RESET_ALL}
                 /$$                                               /$$                       /$$  /$$$$ 
                | $$                                              | $$                      | $$ /$$  $$
                | $$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$$| $$$$$$$   /$$$$$$   /$$$$$$$|__/\ $$
                | $$__  $$ /$$__  $$ /$$__  $$ |____  $$ /$$_____/| $$__  $$ /$$__  $$ /$$__  $$    /$$/
                | $$  \ $$| $$  \__/| $$$$$$$$  /$$$$$$$| $$      | $$  \ $$| $$$$$$$$| $$  | $$   /$$/ 
                | $$  | $$| $$      | $$_____/ /$$__  $$| $$      | $$  | $$| $$_____/| $$  | $$  |__/  
                | $$$$$$$/| $$      |  $$$$$$$|  $$$$$$$|  $$$$$$$| $$  | $$|  $$$$$$$|  $$$$$$$   /$$  
                |_______/ |__/       \_______/ \_______/ \_______/|__/  |__/ \_______/ \_______/  |__/                                                                                                           
""".replace(
        "$", f"{Fore.RED}${Style.RESET_ALL}"
    )
    print(e)


def osint():
    banner()
    email = input(
        f"  {Fore.MAGENTA}[{Fore.GREEN} ? {Fore.MAGENTA}]{Style.RESET_ALL} e-mail: "
    )
    mdp = input(
        f"  {Fore.MAGENTA}[{Fore.GREEN} ? {Fore.MAGENTA}]{Style.RESET_ALL} password: "
    )
    try:
        mydict = scraper.get(f"https://haveibeenpwned.com/unifiedsearch/{email}").json()
        name_list = [i["Name"] for i in mydict["Breaches"]]
        email_breaches = (
            str(name_list).replace("[", "").replace("]", "").replace("'", "")
        )
    except Exception as e:
        print(
            f"\n  {Fore.MAGENTA}[{Fore.GREEN} ! {Fore.MAGENTA}]{Style.RESET_ALL} Incorrect E-mail."
        )
        email_breaches = "Not Found"
        pass

    try:
        encrypt = hashlib.sha1(mdp.encode())
        encrypt = encrypt.hexdigest()
        first_chars = encrypt[0:5]
        first_hash_chars = first_chars.upper()
        r_mdp = scraper.get(
            url="https://api.pwnedpasswords.com/range/" + first_hash_chars
        ).text.replace("\n", "")
        if "prefix" in r_mdp:
            fbm = "Not Found"
        else:
            fbm = "Found"
            pass
        try:
            text_file = open(mdp + "_password.txt", "w")
            text_file.write(r_mdp)
            text_file.close()

        except Exception as e:
            print(e)

    except Exception as e:
        print(e)

    print(
        f"\n  {Fore.MAGENTA}[{Fore.GREEN} ~ {Fore.MAGENTA}]{Style.RESET_ALL} Breached E-mail?:",
        email_breaches,
    )

    print(
        f"\n  {Fore.MAGENTA}[{Fore.GREEN} ~ {Fore.MAGENTA}]{Style.RESET_ALL} Breached Password?: {fbm} (saved hashes as {mdp}_password)"
    )
    input()


osint()
