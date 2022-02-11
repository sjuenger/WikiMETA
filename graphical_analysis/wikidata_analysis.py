import seaborn as sns
import pandas as pd
import numpy as nm
import matplotlib.pyplot as plt
import glob
import json
import collections

def plot_top_wikidata_research_properties():

    metadata_modes = ["qualifier", "reference"]

    for metadata_mode in metadata_modes:

        recommended_modes = ["_recommended_", "_non_recommended_", "_"]

        for recommended_mode in recommended_modes:

            files_json = glob.glob("data/statistical_information/wikidata_research/properties/" +
                                   "top*[0-9]" + recommended_mode + "for_" + metadata_mode + ".json")

            print(files_json)

            with open(files_json[0], "r") as json_data:

                whole_dict = json.load(json_data)

                tmp = collections.OrderedDict(sorted(whole_dict["properties"].items(), key=lambda item: int(item[1][metadata_mode + "_no"]) ))

                print(whole_dict)
                print(tmp)

                whole_dict["properties"] = tmp

                # change up the dictionary to match this schema: {"PID": {}, "label":{}, "qualifier": {}}
                # from this: {'P585': {'label': 'point in time', 'datatype': 'Time', 'statement_no': '833621',

                dataframe_dict = {}
                dataframe_dict["PID/label"] = []
                dataframe_dict["qualifier_percentage"] = []
                dataframe_dict["reference_percentage"] = []
                dataframe_dict["qualifier_class"] = []
                dataframe_dict["is_reference"] = []

                for PID in whole_dict["properties"]:

                    dataframe_dict["PID/label"].append(PID + " / " + whole_dict["properties"][PID]["label"])
                    dataframe_dict["qualifier_percentage"].append( int(whole_dict["properties"][PID]["qualifier_no"]) / int(whole_dict[ "total_usages_of_" + metadata_mode ]) )
                    dataframe_dict["reference_percentage"].append( int(whole_dict["properties"][PID]["reference_no"]) / int(whole_dict[ "total_usages_of_" + metadata_mode ]) )
                    dataframe_dict["qualifier_class"].append(whole_dict["properties"][PID]["qualifier_class"])
                    dataframe_dict["is_reference"].append(whole_dict["properties"][PID]["is_reference"])

                print(dataframe_dict)

                df = pd.DataFrame(dataframe_dict)

                print(df)

                #tmp = sns.catplot(y= "PID/label", x=metadata_mode + "_percentage" , hue="is_reference", kind="bar",  data=df)
                tmp = sns.catplot(y= "PID/label", x=metadata_mode + "_percentage" , kind="bar",  data=df)

                tmp.savefig("tmp_" + metadata_mode + "_" + recommended_mode +".png")




