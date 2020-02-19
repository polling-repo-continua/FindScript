#!/usr/bin/env python3

import base64
import re
import sys
import time

import requests


try:
    from github import Github, GithubException

except ImportError as e:
    print(e)
    sys.exit()


GITHUB_TOKEN = "YOUR_TOKEN_HERE"

def search_github(url, extension, pages, unresolvable, script_re, f):

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0"}

    g = Github(GITHUB_TOKEN)

    try:
        g.get_user('0x41CoreDump')

    except GithubException:
        sys.stderr.write("[ERROR] Bad Github credentials\n")
        sys.stderr.flush()
        return

    found = []

    github_search = g.search_code(f"{url} {extension}", order="desc")

    for i in range(pages*10+1):

        try:
            source_link = github_search[i]

        except IndexError:
            break

        try:
            source_code = base64.b64decode(source_link.content).decode("utf-8")

        except TypeError:
            continue

        for script in re.findall(script_re, source_code):

            if script not in found:

                if not unresolvable:

                    try:
                        r = requests.get(script, allow_redirects=False, headers=headers, timeout=10)

                    except requests.exceptions.RequestException:
                        continue

                    if r.status_code != 200:
                        continue

                print(f"[GITHUB] {script}")
                sys.stdout.flush()
                found.append(script)

                if f:
                    f.write(script+"\n")

                time.sleep(0.2)

        time.sleep(0.5)
