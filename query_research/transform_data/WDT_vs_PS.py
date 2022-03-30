import os

import subprocess
import gzip
import json
import csv
import time
from urllib.parse import unquote_plus

def count_WDT_usage_vs_PS_usage(timeframes):

    result_dict = {}
    result_dict["timeframe data"] = {}
    result_dict["WDT usages"] = 0
    result_dict["PS usages"] = 0
    result_dict["TOTAL usages"] = 0
    result_dict["TOTAL queries"] = 0

    for location in timeframes:

        result_dict["timeframe data"][location[:21]] = {}
        result_dict["timeframe data"][location[:21]]["WDT usages"] = 0
        result_dict["timeframe data"][location[:21]]["PS usages"] = 0
        result_dict["timeframe data"][location[:21]]["TOTAL usages"] = 0
        result_dict["timeframe data"][location[:21]]["TOTAL queries"] = 0

        tsv_data_path = "data/" + location + ".tsv.gz"

        with gzip.open(tsv_data_path, 'rt') as sample_data:

            read_tsv = csv.reader(sample_data, delimiter="\t")

            k = 0

            for row in read_tsv:

                result_dict["timeframe data"][location[:21]]["TOTAL queries"] += 1
                result_dict["TOTAL queries"] += 1

                sample_sparql = unquote_plus(row[0])

                sample_sparql = sample_sparql.replace("?query=", "")

                print(location)
                print(k)
                k += 1

                if "<http://www.wikidata.org/prop/statement/P" in sample_sparql:
                    PS_count = sample_sparql.count("<http://www.wikidata.org/prop/statement/P")

                    result_dict["timeframe data"][location[:21]]["PS usages"] += PS_count
                    result_dict["PS usages"] += PS_count
                    result_dict["timeframe data"][location[:21]]["TOTAL usages"] += PS_count
                    result_dict["TOTAL usages"] += PS_count
                if "<http://www.wikidata.org/prop/direct/P" in sample_sparql:
                    WDT_count = sample_sparql.count("<http://www.wikidata.org/prop/direct/P")
                    result_dict["timeframe data"][location[:21]]["WDT usages"] += WDT_count
                    result_dict["WDT usages"] += WDT_count
                    result_dict["timeframe data"][location[:21]]["TOTAL usages"] += WDT_count
                    result_dict["TOTAL usages"] += WDT_count

        sample_data.close()

    # save the resulting json dictionary
    result_path = "data/WDT_vs_PS_usage.json"
    with open(result_path, "w") as result_data:
        json.dump(result_dict, result_data)