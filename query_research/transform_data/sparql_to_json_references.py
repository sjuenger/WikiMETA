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

        start_time = time.time()

        k = 0

        for row in read_tsv:
            sample_sparql = unquote_plus(row[0])

            print(k)
            k += 1

            # Information for the strings from https://www.mediawiki.org/wiki/Wikibase/Indexing/RDF_Dump_Format

            contains = "none"

            if "<http://www.w3.org/ns/prov#wasDerivedFrom>" in sample_sparql:

                if "<http://www.wikidata.org/prop/reference" in sample_sparql:

                    if "<http://www.wikidata.org/reference" in sample_sparql:
                        contains = "all_three"
                    else:
                        contains = "derived_+_reference_property"

                elif "<http://www.wikidata.org/reference" in sample_sparql:
                    contains = "derived_+_reference_node"
                else:
                    contains = "only_derived"

            elif "<http://www.wikidata.org/prop/reference" in sample_sparql:

                if "<http://www.wikidata.org/reference" in sample_sparql:
                    contains = "reference_node_+_reference_property"
                else:
                    contains = "only_reference_property"

            elif "<http://www.wikidata.org/reference" in sample_sparql:
                contains = "only_reference_node"




            if contains != "none":
                i += 1

                start_time_ref_query = time.time()

                try:
                    process = subprocess.Popen(["./modules/sparqljs/bin/sparql-to-json",
                                                "--strict", sample_sparql], stdout=subprocess.PIPE)
                    output_bytes, err = process.communicate()
                except subprocess.CalledProcessError as e:
                    print(err)
                    print(e)

                if len(output_bytes) != 0:

                    output_str = output_bytes.decode("utf-8")
                    output_json = json.loads(output_str)


                    output_json["timestamp"] = row[1]
                    output_json["sourceCategory"] = row[2]
                    output_json["user_agent"] = row[3]
                    print("Queries found: ", i)
                    print("Time required so far in min: ", (time.time() - start_time) / 60)

                    path_to_json = "data/" + location[:21] + "/" + \
                                   location[22:] + "/reference_metadata/" + contains + "/" + str(k) + \
                                   " " + unquote_plus(row[1]) + ".json"
                    path_to_sparql = "data/" + location[:21] + "/" + \
                                     location[22:] + "/reference_metadata/" + contains + "/" + str(k) + \
                                     " " +unquote_plus(row[1]) + ".sparql"

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
                    path_to_failed = "data/" + location[:21] + "/" + \
                                  location[22:] + "/reference_metadata/" + "failed_queries" + "/" + str(k)\
                                     + " " + unquote_plus(row[1]) + ".txt"

                    with open(path_to_failed, "wt") as failed_txt:
                        failed_txt.write(unquote_plus(row[0]))
                        failed_txt.write(unquote_plus(row[1]))
                        failed_txt.write(unquote_plus(row[2]))
                        failed_txt.write(unquote_plus(row[3]))
                    failed_txt.close()


        print("Pffff.... that took a long time.")
        print("Total amount of queries found: ", i)
        print("Total amount of queries: ", k)

    sample_data.close()
