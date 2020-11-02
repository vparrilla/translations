from typing import Dict, Set, Tuple, List

import yaml
import csv
import argparse


def gen_dict_extract(keys: List, var: Dict):
    if hasattr(var, 'items'):
        for k, v in var.items():
            if k in keys:
                yield v
            if isinstance(v, dict):
                for result in gen_dict_extract(keys, v):
                    yield result
            elif isinstance(v, list):
                for d in v:
                    for result in gen_dict_extract(keys, d):
                        yield result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("combined")
    parser.add_argument("outputfile")
    args = parser.parse_args()

    translations: Dict = yaml.full_load(open(args.combined, 'r'))

    output_columns = ["hash", "en", "fr", "de", "it", "es", "pt", "pl"]

    with open(args.outputfile, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=output_columns)
        writer.writeheader()

        result_set: Set[Tuple] = set()

        for label in gen_dict_extract(["label", "edit_label"], translations):
            if not label:
                continue

            normalized: Dict = {k.lower(): v for k, v in label.items() if k.lower() in output_columns}
            result_set.add(tuple(normalized.items()))

        for s in result_set:
            writer.writerow(dict(s))





