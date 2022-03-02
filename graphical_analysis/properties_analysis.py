import json
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import collections

# only plot the non_redundant data

def plot_top_properties_timeframe(timeframes,metadata_mode ,recommended_mode):

    if metadata_mode not in ["reference_metadata", "qualifier_metadata"]:
        raise Exception

    if recommended_mode not in ["recommended", "non_recommended", "all"]:
        raise Exception

    for timeframe in timeframes:

        csv_ready_properties_dict = {}
        csv_ready_properties_dict["timeframe"] = []
        csv_ready_properties_dict["label"] = []
        csv_ready_properties_dict["properties"] = []
        csv_ready_properties_dict["is_reference"] = []
        csv_ready_properties_dict["qualifier_class"] = []
        csv_ready_properties_dict["recommended_mode"] = []


        timeframe_files = glob.glob("data/" + timeframe[:21] + "/" + timeframe[22:] + \
                                    "/statistical_information/non_redundant/" + metadata_mode + "/" + \
                                    recommended_mode + "/properties/top_*_properties.json")
        with open(timeframe_files[0], "r") as timeframe_data:
            timeframe_dict = json.load(timeframe_data)

            # order the timeframe dict, so that the most used properties are in front
            print(timeframe_dict["properties"])
            timeframe_dict["properties"] = \
                collections.OrderedDict(
                    sorted(timeframe_dict["properties"].items(), key = lambda item: int(item[1])))
            print(timeframe_dict["properties"])

            PID_to_facets_path = "data/" + timeframe[:21] + "/" + timeframe[22:] + \
                                 "/statistical_information/non_redundant/" + metadata_mode + "/" + \
                                 "raw_counted_properties/properties_facets_and_datatypes.json"

            with open(PID_to_facets_path, "r") as PID_to_facets_data:
                PID_to_facets_dict = json.load(PID_to_facets_data)

                for PID in timeframe_dict["properties"]:
                    csv_ready_properties_dict["label"].append(
                        PID_to_facets_dict["real_wikidata_properties"][PID]["label"])
                    csv_ready_properties_dict["timeframe"].append(timeframe[:21])
                    csv_ready_properties_dict["properties"].append(
                        PID_to_facets_dict["real_wikidata_properties"][PID]["occurrences"])

                    csv_ready_properties_dict["is_reference"].append(
                        PID_to_facets_dict["real_wikidata_properties"][PID]["is_reference"])
                    csv_ready_properties_dict["qualifier_class"].append(str(
                        PID_to_facets_dict["real_wikidata_properties"][PID]["qualifier_class"]))

                    csv_ready_properties_dict["recommended_mode"].append(recommended_mode)


        df = pd.DataFrame(csv_ready_properties_dict)

        print(df)

        if metadata_mode == "reference_metadata":
            tmp = sns.catplot(x="label", y="properties", kind="bar",
                              palette="Set2", dodge=False, col="timeframe",
                              data=df, hue="is_reference")
        elif metadata_mode == "qualifier_metadata":
            tmp = sns.catplot(x="label", y="properties", kind="bar",
                              palette="Set2", dodge=False, col="timeframe",
                              data=df, hue="qualifier_class")

        plt.gcf().autofmt_xdate()

        tmp.savefig("data/statistical_information/query_research/non_redundant/"
                    + metadata_mode + "/" + recommended_mode + "/properties/" +
                    timeframe[:22] + "properties.png")

        plt.close()


def plot_top_properties_overall(metadata_mode ,recommended_mode):

    if metadata_mode not in ["reference_metadata", "qualifier_metadata"]:
        raise Exception

    if recommended_mode not in ["recommended", "non_recommended", "all"]:
        raise Exception


    csv_ready_properties_dict = {}
    csv_ready_properties_dict["label"] = []
    csv_ready_properties_dict["properties"] = []
    csv_ready_properties_dict["is_reference"] = []
    csv_ready_properties_dict["qualifier_class"] = []
    csv_ready_properties_dict["recommended_mode"] = []


    timeframe_files = glob.glob("data/statistical_information/query_research/"
                                "non_redundant/" + metadata_mode + "/" + \
                                recommended_mode + "/properties/top_*_properties.json")

    with open(timeframe_files[0], "r") as timeframe_data:
        # order the timeframe dict, so that the most used properties are in front
        timeframe_dict = json.load(timeframe_data)
        timeframe_dict["properties"] = \
        collections.OrderedDict(
            sorted(timeframe_dict["properties"].items(), key = lambda item: int(item[1])))

        PID_to_facets_path = "data/property_dictionary.json"

        with open(PID_to_facets_path, "r") as PID_to_facets_data:
            PID_to_facets_dict = json.load(PID_to_facets_data)

            for PID in timeframe_dict["properties"]:
                csv_ready_properties_dict["label"].append(
                    PID_to_facets_dict[PID]["label"])
                csv_ready_properties_dict["properties"].append(
                    timeframe_dict["properties"][PID])

                csv_ready_properties_dict["is_reference"].append(
                    PID_to_facets_dict[PID]["is_reference"])
                csv_ready_properties_dict["qualifier_class"].append(str(
                    PID_to_facets_dict[PID]["qualifier_class"]))

                csv_ready_properties_dict["recommended_mode"].append(recommended_mode)

    df = pd.DataFrame(csv_ready_properties_dict)

    print(df)

    if metadata_mode == "reference_metadata":
        tmp = sns.catplot(x="label", y="properties", kind="bar", col="recommended_mode",
                          palette="Set2", dodge=False,
                          data=df, hue="is_reference")
    elif metadata_mode == "qualifier_metadata":
        tmp = sns.catplot(x="label", y="properties", kind="bar", col="recommended_mode",
                          palette="Set2", dodge=False,
                          data=df, hue="qualifier_class")

    plt.gcf().autofmt_xdate()

    tmp.savefig("data/statistical_information/query_research/non_redundant/"
                + metadata_mode + "/" + recommended_mode + "/properties/properties_overall.png")

    plt.close()




def plot_top_properties_overall_percentage(metadata_mode ,recommended_mode):

    if metadata_mode not in ["reference_metadata", "qualifier_metadata"]:
        raise Exception

    if recommended_mode not in ["recommended", "non_recommended", "all"]:
        raise Exception


    csv_ready_properties_dict = {}
    csv_ready_properties_dict["label"] = []
    csv_ready_properties_dict["properties_percentages"] = []
    csv_ready_properties_dict["is_reference"] = []
    csv_ready_properties_dict["qualifier_class"] = []
    csv_ready_properties_dict["recommended_mode"] = []


    timeframe_files = glob.glob("data/statistical_information/query_research/"
                                "non_redundant/" + metadata_mode + "/" + \
                                recommended_mode + "/properties/top_*_properties.json")

    with open(timeframe_files[0], "r") as timeframe_data:
        # order the timeframe dict, so that the most used properties are in front
        timeframe_dict = json.load(timeframe_data)
        timeframe_dict["properties"] = \
        collections.OrderedDict(
            sorted(timeframe_dict["properties"].items(), key = lambda item: int(item[1])))

        PID_to_facets_path = "data/property_dictionary.json"

        with open(PID_to_facets_path, "r") as PID_to_facets_data:
            PID_to_facets_dict = json.load(PID_to_facets_data)

            for PID in timeframe_dict["properties"]:
                csv_ready_properties_dict["label"].append(
                    PID_to_facets_dict[PID]["label"])
                csv_ready_properties_dict["properties_percentages"].append(
                    timeframe_dict["properties"][PID] / timeframe_dict["total_properties"])

                csv_ready_properties_dict["is_reference"].append(
                    PID_to_facets_dict[PID]["is_reference"])
                csv_ready_properties_dict["qualifier_class"].append(str(
                    PID_to_facets_dict[PID]["qualifier_class"]))

                csv_ready_properties_dict["recommended_mode"].append(recommended_mode)


    df = pd.DataFrame(csv_ready_properties_dict)

    print(df)

    if metadata_mode == "reference_metadata":
        tmp = sns.catplot(x="label", y="properties_percentages", kind="bar",
                          palette="Set2", dodge=False, col="recommended_mode",
                          data=df, hue="is_reference")
    elif metadata_mode == "qualifier_metadata":
        tmp = sns.catplot(x="label", y="properties_percentages", kind="bar",
                          palette="Set2", dodge=False, col="recommended_mode",
                          data=df, hue="qualifier_class")

    plt.gcf().autofmt_xdate()

    tmp.savefig("data/statistical_information/query_research/non_redundant/"
                + metadata_mode + "/" + recommended_mode +
                "/properties/properties_overall_percentage.png")

    plt.close()


