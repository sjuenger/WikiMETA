import json
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import collections

# only plot the non_redundant data

def plot_top_accumulated_facets_timeframe(timeframes,metadata_mode ,recommended_mode, x):

    if metadata_mode not in ["reference_metadata", "qualifier_metadata"]:
        raise Exception

    if recommended_mode not in ["recommended", "non_recommended", "all"]:
        raise Exception

    for timeframe in timeframes:

        csv_ready_facets_dict = {}
        csv_ready_facets_dict["timeframe"] = []
        csv_ready_facets_dict["facets"] = []
        csv_ready_facets_dict["labels"] = []
        csv_ready_facets_dict["recommended mode"] = []

        timeframe_files = glob.glob("data/" + timeframe[:21] + "/" + timeframe[22:] + \
                                    "/statistical_information/non_redundant/" + metadata_mode + "/" + \
                                    recommended_mode + "/accumulated_facets" +
                                                       "/top_" + str(x) + "_accumulated_facets.json")
        with open(timeframe_files[0], "r") as timeframe_data:
            timeframe_dict = json.load(timeframe_data)

            # order the timeframe dict, so that the most used facets are in front
            timeframe_dict["facets"] = \
                collections.OrderedDict(
                    sorted(timeframe_dict["facets"].items(), key = lambda item: int(item[1])))

            for ID in timeframe_dict["facets"]:
                csv_ready_facets_dict["facets"].append(timeframe_dict["facets"][ID])
                csv_ready_facets_dict["labels"].append(ID)
                csv_ready_facets_dict["timeframe"].append(timeframe[:21].replace("_", " - "))
                csv_ready_facets_dict["recommended mode"].append(recommended_mode)

        df = pd.DataFrame(csv_ready_facets_dict)

        tmp = sns.catplot(x="labels", y="facets", kind="bar",
                          palette="Set2", dodge=False, hue="timeframe", col="recommended mode",
                          data=df, aspect=1.4)

        plt.gcf().autofmt_xdate()

        tmp.savefig("data/statistical_information/query_research/non_redundant/"
                    + metadata_mode + "/" + recommended_mode + "/accumulated_facets/" +
                    timeframe[:22] + "accumulated_facets.png")

        plt.close()


def plot_top_accumulated_facets_overall(metadata_mode, recommended_mode, x):

    if metadata_mode not in ["reference_metadata", "qualifier_metadata"]:
        raise Exception

    if recommended_mode not in ["recommended", "non_recommended", "all"]:
        raise Exception


    csv_ready_facets_dict = {}
    csv_ready_facets_dict["facets"] = []
    csv_ready_facets_dict["labels"] = []
    csv_ready_facets_dict["recommended mode"] = []


    timeframe_files = glob.glob("data/statistical_information/query_research/"
                                "non_redundant/" + metadata_mode + "/" + \
                                recommended_mode + "/accumulated_facets" + \
                                "/top_" + str(x) + "_accumulated_facets.json")

    with open(timeframe_files[0], "r") as timeframe_data:
        # order the timeframe dict, so that the most used facets are in front
        timeframe_dict = json.load(timeframe_data)
        timeframe_dict["facets"] = \
        collections.OrderedDict(
            sorted(timeframe_dict["facets"].items(), key = lambda item: int(item[1])))

        for ID in timeframe_dict["facets"]:
            csv_ready_facets_dict["facets"].append(timeframe_dict["facets"][ID])
            csv_ready_facets_dict["labels"].append(ID)
            csv_ready_facets_dict["recommended mode"].append(recommended_mode)

    df = pd.DataFrame(csv_ready_facets_dict)

    tmp = sns.catplot(x="labels", y="facets", kind="bar",
                      palette="Set2", dodge=False, col="recommended mode",
                      data=df, aspect=1.4)


    plt.gcf().autofmt_xdate()

    tmp.savefig("data/statistical_information/query_research/non_redundant/"
                + metadata_mode + "/" + recommended_mode + "/accumulated_facets" +
                                "/accumulated_facets_overall.png")

    plt.close()




def plot_top_accumulated_facets_overall_percentage(metadata_mode ,recommended_mode, x):

    if metadata_mode not in ["reference_metadata", "qualifier_metadata"]:
        raise Exception

    if recommended_mode not in ["recommended", "non_recommended", "all"]:
        raise Exception


    csv_ready_facets_dict = {}
    csv_ready_facets_dict["facets percentages"] = []
    csv_ready_facets_dict["labels"] = []
    csv_ready_facets_dict["recommended mode"] = []

    timeframe_files = glob.glob("data/statistical_information/query_research/"
                                "non_redundant/" + metadata_mode + "/" +
                                recommended_mode + "/accumulated_facets" +
                                "/top_" + str(x) + "_accumulated_facets.json")

    overall_query_data_path = "data/statistical_information/query_research/" + \
                                "non_redundant/" + metadata_mode + "/" + \
                                "all" + "/accumulated_facets" + \
                                "/top_" + str(x) + "_accumulated_facets.json"

    with open(timeframe_files[0], "r") as timeframe_data:
        with open(overall_query_data_path, "r") as overall_query_data:
            overall_query_dict = json.load(overall_query_data)

            # order the timeframe dict, so that the most used facets are in front
            timeframe_dict = json.load(timeframe_data)
            timeframe_dict["facets"] = \
            collections.OrderedDict(
                sorted(timeframe_dict["facets"].items(), key = lambda item: int(item[1])))

            for ID in timeframe_dict["facets"]:
                csv_ready_facets_dict["labels"].append(ID)
                csv_ready_facets_dict["facets percentages"].append(
                    timeframe_dict["facets"][ID] / overall_query_dict["total_accumulated_facets"])
                csv_ready_facets_dict["recommended mode"].append(recommended_mode)


    df = pd.DataFrame(csv_ready_facets_dict)

    tmp = sns.catplot(x="labels", y="facets percentages", kind="bar",
                      palette="Set2", dodge=False, col="recommended mode",
                      data=df, aspect=1.4)

    plt.gcf().autofmt_xdate()

    tmp.savefig("data/statistical_information/query_research/non_redundant/"
                + metadata_mode + "/" + recommended_mode +
                "/accumulated_facets/accumulated_facets_overall_percentage.png")

    plt.close()


