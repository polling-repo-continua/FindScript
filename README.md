# FindScript

A tool that scrapes Google, Github and the Wayback Machine to find files with a given extension for a given url.

### Dependencies

FindScript uses [PyGithub](https://github.com/PyGithub/PyGithub). <br/>
`pip3 install -r requirements.txt`
<br/> <br/>
You will also need to create a Github Token with no permissions. You can do that here: https://github.com/settings/tokens. Save the token and replace `YOUR_TOKEN_HERE` with your token in [lib/github.py](lib/github.py). 

### Usage

```
$ python3 FindScript.py -h
usage: findscript.py [-h] -u URL [--include-unresolvable] [-e EXTENSION] [-gop GOOGLE_PAGES] [-gip GITHUB_PAGES] [-o OUTPUT]

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL
  --include-unresolvable
  -e EXTENSION, --extension EXTENSION
  -gop GOOGLE_PAGES, --google-pages GOOGLE_PAGES
  -gip GITHUB_PAGES, --github-pages GITHUB_PAGES
  -o OUTPUT, --output OUTPUT
```

Example: `python3 findscript.py -u hackerone.com`
