import subprocess
import gzip
import json
import csv
import time
from urllib.parse import unquote_plus


def extract(location):

    tsv_data_path = "data/" + location + ".tsv.gz"

    with gzip.open(tsv_data_path, 'rt') as sample_data:

        read_tsv = csv.reader(sample_data, delimiter="\t")
        i = 0
        sample = ""
        check_file = []

        start_time = time.time()

        for row in read_tsv:
            sample = unquote_plus(row[0])

            if("<http://www.wikidata.org/prop/reference" in sample):
                i += 1

                process = subprocess.Popen(["./modules/sparqljs/bin/sparql-to-json",
                                            "--strict", sample], stdout=subprocess.PIPE)
                output_bytes, err = process.communicate()
                print(err)

                if (err == None):
                    output_str = output_bytes.decode("utf-8")

                    output_json = json.loads(output_str)

                    output_json["timestamp"] = row[1]
                    output_json["sourceCategory"] = row[2]
                    output_json["user_agent"] = row[3]
                    print("Queries gefunden: " , i)
                    print("Bisher benötigte Zeit in min: ", (time.time()-start_time)/60 )
                    print("\n")

                    path_to_json = "data/" + location + "/" + str(i) + ".json"

                    with open(path_to_json, "wt") as result_data:
                        json.dump(output_json, result_data)
                    result_data.close()

        print("Pffff.... that took a long time.")
        print(i)

    sample_data.close()
