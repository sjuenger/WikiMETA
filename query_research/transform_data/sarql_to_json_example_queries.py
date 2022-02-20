import subprocess
import gzip
import json
import csv
import time
from urllib.parse import unquote_plus

def extract_example_queries(location):
    tsv_data_path = "data/" + location + ".tsv.gz"

    with gzip.open(tsv_data_path, 'rt') as sample_data:

        read_tsv = csv.reader(sample_data, delimiter="\t")

        k = 0

        for row in read_tsv:
            sample_sparql = unquote_plus(row[0])

            sample_sparql = sample_sparql.replace("?query=", "")

            print(k)
            k += 1

            try:
                process = subprocess.Popen(["./modules/sparqljs/bin/sparql-to-json",
                                            "--strict", sample_sparql], stdout=subprocess.PIPE)
                output_bytes, err = process.communicate()
            except subprocess.CalledProcessError as e:
                print(e)
                # // does not go in there !!

            print(output_bytes)
            print(sample_sparql)
            if len(output_bytes) != 0:
                output_str = output_bytes.decode("utf-8")

                output_json = json.loads(output_str)

                path_to_json = "data/" + location + "/" + str(k) + ".json"
                path_to_sparql = "data/" + location + "/" + str(k) + ".sparql"

                with open(path_to_json, "wt") as result_data:
                    json.dump(output_json, result_data)
                result_data.close()
                with open(path_to_sparql, "wt") as test_data:
                    test_data.write(sample_sparql)
                test_data.close()


            else:

                path_to_sparql = "data/" + location + "/" + str(k) + "_failed" + ".sparql"
                with open(path_to_sparql, "wt") as test_data:
                    test_data.write(sample_sparql)


    sample_data.close()
