import os

import subprocess
import gzip
import json
import csv
import time
from urllib.parse import unquote_plus

def count_user_agent_usage(timeframes):

    result_dict = {}
    result_dict["timeframe data"] = {}
    result_dict["browser user agent"] = 0
    result_dict["non browser user agent"] = 0

    for location in timeframes:

        result_dict["timeframe data"][location[:21]] = {}
        result_dict["timeframe data"][location[:21]]["browser user agent"] = 0
        result_dict["timeframe data"][location[:21]]["non browser user agent"] = 0

        tsv_data_path = "data/" + location + ".tsv.gz"

        with gzip.open(tsv_data_path, 'rt') as sample_data:

            read_tsv = csv.reader(sample_data, delimiter="\t")

            k = 0

            for row in read_tsv:

                sample_sparql = unquote_plus(row[0])

                sample_sparql = sample_sparql.replace("?query=", "")

                print(location)
                print(k)
                k += 1

                metadata_array = ["<http://www.wikidata.org/prop/qualifier",
                                  "<http://wikiba.se/ontology#BestRank>",
                                  "<http://wikiba.se/ontology#rank>",
                                  "<http://wikiba.se/ontology#DeprecatedRank>",
                                  "<http://wikiba.se/ontology#PreferredRank>",
                                  "<http://wikiba.se/ontology#NormalRank>",
                                  "<http://www.w3.org/ns/prov#wasDerivedFrom>",
                                  "<http://www.wikidata.org/prop/reference",
                                  "<http://www.wikidata.org/reference"]

                for metadata_str in metadata_array:
                    if metadata_str in sample_sparql:

                        if "browser" == row[3]:

                            result_dict["timeframe data"][location[:21]]["browser user agent"] += 1
                            result_dict["browser user agent"] += 1

                        else:
                            result_dict["timeframe data"][location[:21]]["non browser user agent"] += 1
                            result_dict["non browser user agent"] += 1

        sample_data.close()

    # save the resulting json dictionary
    result_path = "data/user_agent_metadata_usage.json"
    with open(result_path, "w") as result_data:
        json.dump(result_dict, result_data)