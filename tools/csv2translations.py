import os
from collections import defaultdict
from typing import Dict, Set, Tuple, List

import yaml
import csv
import argparse


class AutoDict(dict):
    """
    Implements 'autovivication' for dictionaries. Taken from Wikipedia:
    https://en.wikipedia.org/wiki/Autovivification#Python
    """
    def __missing__(self, key):
        value = self[key] = type(self)()
        return value


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cleaned")
    args = parser.parse_args()

    with open(args.cleaned, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        # {'en': {}, 'fr': {}, etc.}
        output: AutoDict = AutoDict({k: {} for k in reader.fieldnames if k != "key"})

        for row in reader:
            if (kval := row['key']) is None or kval == "":
                continue

            for lang, translated in row.items():
                if lang == "key":
                    continue

                group, key = kval.split(".")

                if group is None or key is None:
                    continue

                if group not in output[lang]:
                    output[lang][group] = {}

                output[lang][group][key] = translated

        for lang, values in output.items():
            if not os.path.exists("locales/"):
                os.mkdir("locales")

            lfile = open(f"locales/{lang}.yml", 'w')
            yaml.dump({lang: values}, lfile, allow_unicode=True)
            lfile.close()



