#!/usr/bin/env python3

import random
import re
import sys
import time

import requests


def search_google(url, extension, pages, unresolvable, script_re, f):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"}

    google_re = "(?<=\<div class=\"r\"\>\<a href\=\")https?://[a-zA-Z\.0-9\/\@\_-]*(?=\")"
    google_tld = ["com", "fr", "dk", "de", "ca", "se", "ro", "ru", "nl", "pl", "es", "it"]

    query = f"{url} {extension}"

    found = []

    for start in range(0, (pages*10)+10, 10):

        tld = random.choice(google_tld)

        url = f"https://google.{tld}/search?q={query}&start={start}"

        try:
            r = requests.get(url, headers=headers, timeout=10)

        except requests.exceptions.RequestException as e:
            sys.stderr.write(f"[ERROR] {e}\n")
            sys.stderr.flush()
            return

        for result in re.findall(google_re, r.text):

            try:
                r = requests.get(result, headers=headers, timeout=10)

            except requests.exceptions.RequestException:
                continue

            for script in re.findall(script_re, r.text):

                if script not in found:

                    if not unresolvable:

                        try:
                            r = requests.get(script, allow_redirects=False, headers=headers, timeout=10)

                        except requests.exceptions.RequestException:
                            continue

                        if r.status_code != 200:
                            continue

                    print(f"[GOOGLE] {script}")
                    sys.stdout.flush()
                    found.append(script)

                    if f:
                        f.write(script+"\n")

            time.sleep(0.2)

        time.sleep(0.5)

