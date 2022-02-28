import json
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# only plot the non_redundant data

def plot_top_properties_timeframe(timeframes,metadata_mode ,recommended_mode):

    if metadata_mode not in ["reference_metadata", "qualifier_metadata", "rank_metadata"]:
        raise Exception

    if recommended_mode not in ["recommended", "non_recommended", "all"]:
        raise Exception


    csv_ready_properties_dict = {}
    csv_ready_properties_dict["timeframe"] = []
    csv_ready_properties_dict["label"] = []
    csv_ready_properties_dict["properties"] = []


    for timeframe in timeframes:

        timeframe_files = glob.glob("data/" + timeframe[:21] + "/" + timeframe[22:] + \
            "/statistical_information/non_redundant/" + metadata_mode + "/" + \
            recommended_mode + "/properties/top_*_properties.json")

        with open(timeframe_files[0], "r") as timeframe_data:
            timeframe_dict = json.load(timeframe_data)

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

    df = pd.DataFrame(csv_ready_properties_dict)

    print(df)

    tmp = sns.catplot(x="label", y="properties", kind="bar",
                      palette="tab10", dodge=True, hue="timeframe",
                      data=df, aspect=1.6)

    plt.gcf().autofmt_xdate()

    tmp.savefig("data/statistical_information/query_research/non_redundant/"
                + metadata_mode + "/" + recommended_mode + "/properties/properties.png")

    plt.close()


def plot_top_properties_overall(metadata_mode ,recommended_mode):

    if metadata_mode not in ["reference_metadata", "qualifier_metadata"]:
        raise Exception

    if recommended_mode not in ["recommended", "non_recommended", "all"]:
        raise Exception


    csv_ready_properties_dict = {}
    csv_ready_properties_dict["label"] = []
    csv_ready_properties_dict["properties"] = []


    timeframe_files = glob.glob("data/statistical_information/query_research/"
                                "non_redundant/" + metadata_mode + "/" + \
                                recommended_mode + "/properties/top_*_properties.json")

    with open(timeframe_files[0], "r") as timeframe_data:
        timeframe_dict = json.load(timeframe_data)

        PID_to_facets_path = "data/property_dictionary.json"

        with open(PID_to_facets_path, "r") as PID_to_facets_data:
            PID_to_facets_dict = json.load(PID_to_facets_data)

            for PID in timeframe_dict["properties"]:
                csv_ready_properties_dict["label"].append(
                    PID_to_facets_dict[PID]["label"])
                csv_ready_properties_dict["properties"].append(
                    timeframe_dict["properties"][PID])

    df = pd.DataFrame(csv_ready_properties_dict)

    print(df)

    tmp = sns.catplot(x="label", y="properties", kind="bar",
                      palette="tab10", dodge=True,
                      data=df, aspect=1.6)

    plt.gcf().autofmt_xdate()

    tmp.savefig("data/statistical_information/query_research/non_redundant/"
                + metadata_mode + "/" + recommended_mode + "/properties/properties_overall.png")

    plt.close()



