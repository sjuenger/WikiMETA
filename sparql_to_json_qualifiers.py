import subprocess
import gzip
import json
import csv
import time
from urllib.parse import unquote_plus


def extract_SPARQL_to_JSON(location):
    tsv_data_path = "data/" + location + ".tsv.gz"

    with gzip.open(tsv_data_path, 'rt') as sample_data:

        read_tsv = csv.reader(sample_data, delimiter="\t")

        i = 0
        failed_conversions = 0

        start_time = time.time()

        k = 0
        for row in read_tsv:
            sample_sparql = unquote_plus(row[0])
            print(k)
            k += 1
            if "<http://www.wikidata.org/prop/qualifier" in sample_sparql:
                i += 1

                start_time_ref_query = time.time()
                try:
                    process = subprocess.Popen(["./modules/sparqljs/bin/sparql-to-json",
                                                "--strict", sample_sparql], stdout=subprocess.PIPE)
                    output_bytes, err = process.communicate()
                except subprocess.CalledProcessError as e:
                    print(err)
                    print(e)
                    failed_conversions += 1
                    # // does not go in there !!

                if len(output_bytes) != 0:
                    output_str = output_bytes.decode("utf-8")

                    output_json = json.loads(output_str)

                    output_json["timestamp"] = row[1]
                    output_json["sourceCategory"] = row[2]
                    output_json["user_agent"] = row[3]
                    print("Queries found: ", i)
                    print("Time required so far in min: ", (time.time() - start_time) / 60)

                    path_to_json = "data/" + location[:21] + "/" + \
                                   location[22:] + "/qualifier_metadata/" + "property_qualifier" + "/" + str(
                        i) + ".json"
                    path_to_sparql = "data/" + location[:21] + "/" + \
                                     location[22:] + "/qualifier_metadata/" + "property_qualifier" + "/" + str(
                        i) + ".sparql"

                    with open(path_to_json, "wt") as result_data:
                        json.dump(output_json, result_data)
                    result_data.close()
                    with open(path_to_sparql, "wt") as test_data:
                        test_data.write(sample_sparql)
                    test_data.close()

                    end_time_ref_query = time.time()
                    time_taken_ref_query = end_time_ref_query - start_time_ref_query
                    print("Time taken for this query in sec: ", time_taken_ref_query)
                    print("Time taken on average for a query:", (time.time() - start_time) / i)
                    print("\n")

                else:
                    print(sample_sparql)
                    failed_conversions += 1
                    path_to_failed = "data/" + location[:21] + "/" + \
                                  location[22:] + "/qualifier_metadata/" + "failed_queries" + "/" + str(k)\
                                     + " " + unquote_plus(row[1]) + ".txt"

                    with open(path_to_failed, "wt") as failed_txt:
                        failed_txt.write(unquote_plus(row[0]))
                        failed_txt.write(unquote_plus(row[1]))
                        failed_txt.write(unquote_plus(row[2]))
                        failed_txt.write(unquote_plus(row[3]))


        path_to_txt = "data/" + location[:21] + "/" + \
                      location[22:] + "/qualifier_metadata/" + "property_qualifier" + "/" + str(
            failed_conversions) + ".txt"

        with open(path_to_txt, "wt") as failed_txt:
            failed_txt.write(failed_conversions.to_string())

        print("Pffff.... that took a long time.")
        print("Total amount of queries found: ", i)
        print("Total amount of queries: ", k)
        print("Total amount of failed query conversions: ", failed_conversions)

    sample_data.close()
