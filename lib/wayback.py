#!/usr/bin/env python3

import json
import re
import sys
import time

import requests


def search_wayback(url, unresolvable, script_re, f):

    found = []

    try:
        r = requests.get(f"http://web.archive.org/cdx/search/cdx?url=*.{url}/*&output=json&fl=original&collapse=urlkey", timeout=10)

    except requests.exceptions.RequestException:
        sys.stderr.write("[ERROR] Unable to connect to web.archive.org\n")
        sys.stderr.flush()
        return

    j = json.loads(r.text)

    for result in j:

        result = result[0]

        if re.match(script_re, result):

            if not unresolvable:

                try:
                   r = requests.get(result, allow_redirects=False, timeout=10)

                except requests.exceptions.RequestException:
                    continue

                if r.status_code != 200:
                    continue

            print(f"[WAYBACK] {result}")
            sys.stdout.flush()
            found.append(result)

            if f:
                f.write(result+"\n")

        time.sleep(0.2)

