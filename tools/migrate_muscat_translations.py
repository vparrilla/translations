import argparse
import csv
from typing import Dict, Optional, List

import yaml
import logging

log = logging.getLogger(__name__)
logging.basicConfig(format="[%(asctime)s] [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)",
                    level=logging.DEBUG)


def search_csvfile(csv, column: str, needle: str) -> Optional[Dict]:
    for row in csv:
        if row.get(column) and row.get(column) == needle:
            return row
    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("muscat_source")
    parser.add_argument("csv_source")
    parser.add_argument("muscat_output_mapping")
    args = parser.parse_args()

    source: Dict = yaml.full_load(open(args.muscat_source, 'r'))
    csvfile: List[Dict] = list(csv.DictReader(open(args.csv_source, 'r')))
    output: Dict = {}

    for tkey, tvalue in source.items():
        if 'label' in tvalue:
            enval: str = tvalue["label"].get("en")
            en_row: Optional[Dict] = search_csvfile(csvfile, "en", enval)

            if en_row:
                output[tkey] = {"label": en_row["key"]}
            else:
                log.warning("No value found for %s", enval)
                output[tkey] = {"label": ""}

        if 'fields' in tvalue:
            output[tkey]["fields"] = {}
            for fieldkey, fieldval in tvalue["fields"].items():
                field_enval = fieldval["label"].get("en")
                field_row = search_csvfile(csvfile, "en", field_enval)

                if field_row:
                    output[tkey]["fields"][fieldkey] = {"label": field_row["key"]}
                else:
                    log.warning("No value found for %s: %s, %s", tkey, field_enval, fieldval)
                    output[tkey]["fields"][fieldkey] = {"label": ""}

    sorted_output = dict(sorted(output.items()))

    with open(args.muscat_output_mapping, 'w') as f:
        yaml.dump(sorted_output, f, allow_unicode=True, default_style='"')
