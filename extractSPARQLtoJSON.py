import subprocess
import gzip
import json
import csv
from urllib.parse import unquote_plus


def extract():
    with gzip.open('data/2017-06-12_2017-07-09_organic.tsv.gz', 'rt') as sample_data:
        with gzip.open('data/2017-06-12_2017-07-09_organic.json.gz','wt') as result_data:
            read_tsv = csv.reader(sample_data, delimiter="\t")
            i = 0
            sample = ""
            check_file = []
            for row in read_tsv:
                sample = unquote_plus(row[0])
                if("<http://www.wikidata.org/prop/reference" in sample):
                    i += 1

                    process = subprocess.Popen(["./modules/sparqljs/bin/sparql-to-json", "--strict", sample], stdout=subprocess.PIPE)
                    output_bytes, err = process.communicate()
                    print(err)

                    if (err == None):
                        output_str = output_bytes.decode("utf-8")

                        output_json = json.loads(output_str)

                        output_json["timestamp"] = row[1]
                        output_json["sourceCategory"] = row[2]
                        output_json["user_agent"] = row[3]
                        print(i)

                        json.dump(output_json, result_data)

            print("Pffff.... that took a long time.")
            print(i)

        result_data.close()
    sample_data.close()
