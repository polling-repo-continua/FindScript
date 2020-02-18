#!/usr/bin/env python3

import argparse
import sys
import threading

from lib.google import search_google
from lib.github import search_github
from lib.wayback import search_wayback

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--url", type=str, required=True)
parser.add_argument("--include-unresolvable", action="store_true")
parser.add_argument("-e", "--extension", type=str, default="js")
parser.add_argument("-gop", "--google-pages", type=int, default=15)
parser.add_argument("-gip", "--github-pages", type=int, default=15)
parser.add_argument("-o", "--output", type=str)
args = parser.parse_args()


def main():

    f = 0

    if args.output:
        f = open(args.output, "a", 1)

    m_url = args.url.replace(".", "\.")

    script_re = r"https?:\/\/[\w\.]*{}\/[\w\.\-]+\.{}".format(m_url, args.extension)

    google = threading.Thread(target=search_google, args=(args.url, args.extension, args.google_pages, args.include_unresolvable, script_re, f,))
    google.daemon = True

    github = threading.Thread(target=search_github, args=(args.url, args.extension, args.github_pages, args.include_unresolvable, script_re, f,))
    github.daemon = True

    wayback = threading.Thread(target=search_wayback, args=(args.url, args.include_unresolvable, script_re, f,))
    wayback.daemon = True

    google.start()
    github.start()
    wayback.start()

    google.join()
    github.join()
    wayback.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit()
