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

        recommended_modes = ["recommended", "non_recommended", "all"]

        for recommended_mode in recommended_modes:

            files_json = glob.glob("data/statistical_information/wikidata_research/" +
                                   metadata_mode + "/" + recommended_mode +
                                   "/properties/" + "top*" + ".json")

            # if the recommended option is set (i.e. not null), is it necessary to query the overall files
            # .. to get the number of both recommended / not recommended reference/qualifier property usages
            # --> to be able to calculate the percentage of e.g. the usages of a recommended property against
            # .. .. the overall value of reference/qualifier property usages (both recommended properties +
            # .. .. .. non_recommended properties)

            overall_usages = 0

            overall_json = glob.glob("data/statistical_information/wikidata_research/" +
                                     metadata_mode + "/all/properties/top*.json")
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

                dataframe_dict["recommended_mode"] = recommended_mode.replace("_", " ") + " " + metadata_mode + "s"

                for PID in whole_dict["properties"]:

                    #dataframe_dict["PID/label"].append(PID + " / " + whole_dict["properties"][PID]["label"])
                    dataframe_dict["label"].\
                        append(whole_dict["properties"][PID]["label"])
                    dataframe_dict["qualifier_percentage"].\
                        append( int(whole_dict["properties"][PID]["qualifier_no"]) / overall_usages)
                    dataframe_dict["reference_percentage"].\
                        append( int(whole_dict["properties"][PID]["reference_no"]) / overall_usages )

                    # if the qualifier class is null -> insert: " - not a recommended qualifier - "
                    if whole_dict["properties"][PID]["qualifier_class"] == []:
                        dataframe_dict["qualifier_class"]. \
                            append("- not a recommended qualifier -")
                    else:
                        dataframe_dict["qualifier_class"].\
                            append(str( whole_dict["properties"][PID]["qualifier_class"]))
                        print(str( whole_dict["properties"][PID]["qualifier_class"]))
                    dataframe_dict["is_reference"].\
                        append(whole_dict["properties"][PID]["is_reference"])

                print(dataframe_dict)

                df = pd.DataFrame(dataframe_dict)

                print(df)

                #tmp = sns.catplot(x= "label", y=metadata_mode + "_percentage",
                #                  hue="is_reference", kind="bar", col = "", dodge=False,
                #                  data=df, height=4, aspect=1.5)

                if (metadata_mode == "reference") :

                    tmp = sns.catplot(x= "label", y=metadata_mode + "_percentage",
                                      hue="is_reference", hue_order=[True, False], kind="bar",
                                      palette="tab10", dodge=False, col="recommended_mode",
                                      data=df)

                else:

                    tmp = sns.catplot(x= "label", y=metadata_mode + "_percentage",
                                      hue="qualifier_class",
                                      hue_order=["[\'Wikidata qualifier\']",
                                                 "[\'restrictive qualifier\']",
                                                 "[\'non-restrictive qualifier\']",
                                                 "[\'Wikidata property used as \"depicts\" (P180) qualifier on Commons\']",
                                                 "[\'non-restrictive qualifier\', \'Wikidata property used as \"depicts\" (P180) qualifier on Commons\']",
                                                 "[\'restrictive qualifier\', \'Wikidata property used as \"depicts\" (P180) qualifier on Commons\']",
                                                 "[\'restrictive qualifier\', \'non-restrictive qualifier\', \'Wikidata property used as \"depicts\" (P180) qualifier on Commons\']",
                                                 "- not a recommended qualifier -"
                                      ],
                                      kind="bar", dodge=False, col="recommended_mode",
                                      data=df)
                    # kind = point for the timeframes !

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

                tmp.savefig("data/statistical_information/wikidata_research/" +
                            metadata_mode + "/" + recommended_mode +
                            "/properties/properties.png")

                plt.close()


def plot_top_wikidata_research_accumulated_facets():

    metadata_modes = ["qualifier", "reference"]

    for metadata_mode in metadata_modes:

        recommended_modes = ["recommended", "non_recommended", "all"]

        for recommended_mode in recommended_modes:

            files_json = glob.glob("data/statistical_information/wikidata_research/" +
                                   metadata_mode + "/" + recommended_mode + "/accumulated_facets/" +
                                   "top*.json")

            # if the recommended option is set (i.e. not null), is it necessary to query the overall files
            # .. to get the number of both recommended / not recommended reference/qualifier facets usages
            # --> to be able to calculate the percentage of e.g. the usages of a recommended facet against
            # .. .. the overall value of reference/qualifier facets usages (both recommended facets +
            # .. .. .. non_recommended facets)

            overall_usages = 0

            overall_json = glob.glob("data/statistical_information/wikidata_research/" +
                                     metadata_mode + "/all/accumulated_facets/accumulated_facets.json")

            with open(overall_json[0], "r") as overall_json:

                overall_dict = json.load(overall_json)

                overall_usages = int( overall_dict["total_accumulated_facets"] )


            print(files_json)

            with open(files_json[0], "r") as json_data:

                whole_dict = json.load(json_data)

                tmp = collections.OrderedDict(sorted(whole_dict["facets"].items(), key=lambda item: int(item[1]) ))

                print(whole_dict)
                print(tmp)

                whole_dict["facets"] = tmp

                dataframe_dict = {}
                dataframe_dict["label"] = []
                dataframe_dict["accumulated_facets_percentage"] = []

                dataframe_dict["recommended_mode"] = recommended_mode.replace("_", " ") + " " + metadata_mode + "s"

                for ID in whole_dict["facets"]:

                    dataframe_dict["label"].\
                        append(ID)
                    dataframe_dict["accumulated_facets_percentage"].\
                        append( int(whole_dict["facets"][ID]) / overall_usages)


                print(dataframe_dict)

                df = pd.DataFrame(dataframe_dict)

                print(df)


                tmp = sns.catplot(x= "label", y="accumulated_facets_percentage", kind="bar",
                                  palette="tab10", dodge=False, col="recommended_mode",
                                  data=df)


                plt.gcf().autofmt_xdate()


                tmp.savefig("data/statistical_information/wikidata_research/"+
                            metadata_mode + "/" + recommended_mode +
                            "/accumulated_facets/accumulated_facets.png")

                plt.close()


def plot_top_wikidata_research_accumulated_datatypes():

    metadata_modes = ["qualifier", "reference"]

    for metadata_mode in metadata_modes:

        recommended_modes = ["recommended", "non_recommended", "all"]

        for recommended_mode in recommended_modes:

            files_json = glob.glob("data/statistical_information/wikidata_research/" +
                                   metadata_mode + "/" + recommended_mode +
                                   "/accumulated_datatypes/accumulated_datatypes.json")

            # if the recommended option is set (i.e. not null), is it necessary to query the overall files
            # .. to get the number of both recommended / not recommended reference/qualifier datatypes usages
            # --> to be able to calculate the percentage of e.g. the usages of a recommended datatypes against
            # .. .. the overall value of reference/qualifier datatypes usages (both recommended datatypes +
            # .. .. .. non_recommended datatypes)

            overall_usages = 0

            overall_json = glob.glob("data/statistical_information/wikidata_research/" +
                                     metadata_mode + "/all/accumulated_datatypes/accumulated_datatypes.json")
            with open(overall_json[0], "r") as overall_json:

                overall_dict = json.load(overall_json)

                overall_usages = int( overall_dict["total_accumulated_datatypes"] )


            print(files_json)

            with open(files_json[0], "r") as json_data:

                whole_dict = json.load(json_data)

                tmp = collections.OrderedDict(sorted(whole_dict["datatypes"].items(), key=lambda item: int(item[1]) ))

                print(whole_dict)
                print(tmp)

                whole_dict["datatypes"] = tmp

                dataframe_dict = {}
                dataframe_dict["label"] = []
                dataframe_dict["accumulated_datatypes_percentage"] = []

                dataframe_dict["recommended_mode"] = recommended_mode.replace("_", " ") + " " + metadata_mode + "s"

                for ID in whole_dict["datatypes"]:

                    dataframe_dict["label"].\
                        append(ID)
                    dataframe_dict["accumulated_datatypes_percentage"].\
                        append( int(whole_dict["datatypes"][ID]) / overall_usages)


                print(dataframe_dict)

                df = pd.DataFrame(dataframe_dict)

                print(df)


                tmp = sns.catplot(x= "label", y="accumulated_datatypes_percentage", kind="bar",
                                  palette="tab10", dodge=False, col="recommended_mode",
                                  data=df, aspect=1.6)


                plt.gcf().autofmt_xdate()


                tmp.savefig("data/statistical_information/wikidata_research/" +
                            metadata_mode + "/" + recommended_mode +
                            "/accumulated_datatypes/accumulated_datatypes.png")

                plt.close()





