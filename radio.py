#!/usr/bin/env python
from pick import pick
import requests
import re
import os
import pyfscache

cache_it = pyfscache.FSCache('~/.cache/radio/digitallyimported', days=10)
BASE = 'http://pub5.di.fm/'

@cache_it
def get_index():
    html = requests.get(BASE).text
    urls = re.findall(r'<h3>Mount Point /(.*?)</h3>', html)
    names = re.findall(r'Stream Title:</td><td class="streamdata">(.*?)</td>', html)
    names = [re.sub(r' DIGITALLY IMPORTED -', '', name)[:100] for name in names]
    names = [re.sub(r'DI - ', '', name) for name in names]
    names = [name.split(" - ")[0] for name in names]
    return names, urls

names, urls = get_index()
styles = set(names)
stations = zip(names, urls)

title = 'Please choose which station to play'
style, _ = pick(sorted(list(styles)), title)
options = [station[1] for station in stations if station[0] == style]
option, _ = pick(options, title)
argv = ["/usr/bin/mplayer", "{}{}".format(BASE, option)]
os.execv("/usr/bin/mplayer", argv)
