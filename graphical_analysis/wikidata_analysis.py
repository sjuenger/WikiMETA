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

            # if the recommended option is set (i.e. not null), is it necessary to query the overall files
            # .. to get the number of both recommended / not recommended reference property usages
            # --> to be able to calculate the percantage of e.g. the usages of a recommended property against
            # .. .. the overall value of reference property usages (both recommended properties +
            # .. .. .. non_recommended properties)

            overall_usages = 0

            overall_json = glob.glob("data/statistical_information/wikidata_research/properties/" +
                               "top*[0-9]_for_" + metadata_mode + ".json")
            with open(overall_json[0], "r") as overall_json:

                overall_dict = json.load(overall_json)

                overall_usages = int( overall_dict[ "total_usages_of_" + metadata_mode ] )


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
                #dataframe_dict["PID/label"] = []
                dataframe_dict["label"] = []
                dataframe_dict["qualifier_percentage"] = []
                dataframe_dict["reference_percentage"] = []
                dataframe_dict["qualifier_class"] = []
                dataframe_dict["is_reference"] = []

                for PID in whole_dict["properties"]:

                    #dataframe_dict["PID/label"].append(PID + " / " + whole_dict["properties"][PID]["label"])
                    dataframe_dict["label"].\
                        append(whole_dict["properties"][PID]["label"])
                    dataframe_dict["qualifier_percentage"].\
                        append( int(whole_dict["properties"][PID]["qualifier_no"]) / overall_usages)
                    dataframe_dict["reference_percentage"].\
                        append( int(whole_dict["properties"][PID]["reference_no"]) / overall_usages )

                    # if the qualifier class is null -> insert: " - not a recommended qualifier - "
                    if whole_dict["properties"][PID]["qualifier_class"] == "":
                        dataframe_dict["qualifier_class"]. \
                            append("- not a recommended qualifier -")
                    elif len(whole_dict["properties"][PID]["qualifier_class"])==2:
                        print(whole_dict["properties"][PID]["qualifier_class"])
                        raise Exception
                    else:
                        dataframe_dict["qualifier_class"].\
                            append(whole_dict["properties"][PID]["qualifier_class"])
                    dataframe_dict["is_reference"].\
                        append(whole_dict["properties"][PID]["is_reference"])

                print(dataframe_dict)

                df = pd.DataFrame(dataframe_dict)

                print(df)

                #tmp = sns.catplot(x= "label", y=metadata_mode + "_percentage",
                #                  hue="is_reference", kind="bar", dodge=False,
                #                  data=df, height=4, aspect=1.5)

                if (metadata_mode == "reference") :

                    tmp = sns.catplot(x= "label", y=metadata_mode + "_percentage",
                                      hue="is_reference", kind="bar", dodge=False,
                                      data=df)

                else:

                    tmp = sns.catplot(x= "label", y=metadata_mode + "_percentage",
                                      hue="qualifier_class", kind="bar", dodge=False,
                                      data=df)

                #tmp = sns.catplot(x= "label", y=metadata_mode + "_percentage" , kind="bar",  data=df, estimator=nm.median)

                #plt.ylim(0,1)
                #plt.xlim(0,0.3)

                #plt.xticks(rotation=-45)
                #plt.tight_layout()

                #plt.gcf().autofmt_xdate(rotation=-45, ha = "left")
                plt.gcf().autofmt_xdate()
                #fig.autofmt_xdate()

                #plt.figure(figsize=(5000,5000))
                #plt.legend(bbox_to_anchor=(1, 1), loc=2)

                tmp.savefig("tmp_" + metadata_mode + "_" + recommended_mode +".png")

                # fix the % from ALL qualifiers / references




