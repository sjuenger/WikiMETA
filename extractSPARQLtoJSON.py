import subprocess
import gzip
import json
import csv
from urllib.parse import unquote_plus

#import fyzz

with gzip.open('data/2017-06-12_2017-07-09_organic.tsv.gz', 'rt') as sample_data:
    with gzip.open('data/2017-06-12_2017-07-09_organic.json.gz','wt') as result_data:
        with open('data/tmp.sparql','wt') as hand_over_to_js_data:
            read_tsv = csv.reader(sample_data, delimiter="\t")
            i=0
            sample=""
            check_file=[]
            for row in read_tsv:
                sample = unquote_plus(row[0])
                if("<http://www.wikidata.org/prop/reference" in sample):
                    i += 1
                    hand_over_to_js_data.seek(0)
                    hand_over_to_js_data.write(sample)
                    hand_over_to_js_data.truncate()

                    process = subprocess.Popen(["sparqljs", "--strict", "./data/tmp.sparql"], stdout=subprocess.PIPE)
                    output_bytes, err = process.communicate()

                    output_str = output_bytes.decode("utf-8")

                    output_json = json.loads(output_str)

                    output_json["timestamp"] = row[1]
                    output_json["sourceCategory"] = row[2]
                    output_json["user_agent"] = row[3]

                    json.dump(output_json, result_data)

                    if (i == 1):
                        break

        hand_over_to_js_data.close()
    result_data.close()
sample_data.close()