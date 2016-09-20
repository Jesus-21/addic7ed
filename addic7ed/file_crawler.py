import os
import re

from collections import OrderedDict
from termcolor import colored

from addic7ed.shows import Shows
from addic7ed.config import Config
from addic7ed.constants import EXT_TO_CHECK

REGEX = r"(.*)\.[s|S]?([0-9]{1,2})[x|X|e|E]?([0-9]{2})\..*([0-9]+p)?.*"


class FileCrawler:
    def __init__(self):
        self.shows = Shows()
        self.episodes = OrderedDict()
        listfile = Config.paths or sorted(os.listdir())
        for f in listfile:
            if Config.dont_check_ext or f.endswith(tuple(EXT_TO_CHECK)):
                ep = self._parse_filename(f)
                if ep:
                    self.episodes[f] = ep

    def _parse_filename(self, filename):
        m = re.match(REGEX, os.path.basename(filename))
        print(colored("%s... " % filename, "white", attrs=["dark"]),
              end="", flush=True)
        if m:
            serie = self.shows.get(m.group(1).replace('.', ' ').title())
            season = int(m.group(2))
            episode = int(m.group(3))
            print(colored("OK", "green"))

            return Episode(filename, serie, season, episode)
        else:
            print(colored("No match", "red"))
            return None


class Episode:
    def __init__(self, f, serie, season, episode):
        self.infos = {
            "serie": serie,
            "season": season,
            "episode": episode,
        }
        self.dir = os.path.dirname(f) or '.'
        self.filename, self.ext = os.path.splitext(os.path.basename(f))
        m = re.search(r"-(.*)%s$" % self.ext, f)
        self.infos["group"] = m.group(1) if m else ""

    def rename(self, new_name):
        try:
            os.rename("%s/%s%s" % (self.dir, self.filename, self.ext),
                      "%s/%s%s" % (self.dir, new_name, self.ext))
            ret = colored("Renamed %s to %s" % (self.filename, new_name),
                          "green")
            self.filename = new_name
        except Exception as e:
            ret = colored(e, "red")

        return ret

    def __str__(self):
        return colored("%s - Season %02d Episode %02d (%s)" % (
            self.infos["serie"],
            self.infos["season"],
            self.infos["episode"],
            self.filename
        ), "blue")
