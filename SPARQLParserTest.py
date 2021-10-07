import gzip
import csv
from urllib.parse import unquote
#import fyzz

with gzip.open('data/2017-06-12_2017-07-09_organic.tsv.gz', 'rt') as sample_data:
    read_tsv = csv.reader(sample_data, delimiter="\t")
    i=0
    sample=""
    check_file=[]
    for row in read_tsv:
        sample = unquote(row[0])
        if("<http://www.wikidata.org/prop/reference" in sample):
            sample = sample.replace("+", " ")
            print(sample)
            if(sample in check_file) :
                print(sample)
                i+=1
                check_file.append((sample, 1)) #add sample | +1 in  the detection
                print("References found: ", i, "\n")

    sample_data.close()