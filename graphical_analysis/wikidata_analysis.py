import seaborn as sns
import pandas as pd
import numpy as nm
import matplotlib.pyplot as plt
import glob
import json

def plot_top_wikidata_research_properties():

    metadata_modes = ["qualifier", "reference"]

    for metadata_mode in metadata_modes:

        recommended_modes = ["_recommended_", "_non_recommended_", "_"]

        for recommended_mode in recommended_modes:

            files_json = glob.glob("data/statistical_information/wikidata_research/properties/" +
                                   "top*[0-9]" + recommended_mode + "for_" + metadata_mode + ".json")

            print(files_json)

            # change up the dictionary to match this schema: {"PID": {}, "label":{}, "qualifier": {}}

            with open(files_json[0], "r") as json_data:

                whole_dict = json.load(json_data)

                props_dict = whole_dict

                print(props_dict["properties"])

                df = pd.DataFrame(props_dict["properties"])

                print(df)

                tmp = sns.catplot(x= "P585", y="qualifier_no", data=df)

                tmp.savefig("tmp.png")




