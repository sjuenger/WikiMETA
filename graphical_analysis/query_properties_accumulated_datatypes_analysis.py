import json
import glob
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import collections

# only plot the non_redundant data

def plot_top_accumulated_datatypes_timeframe(timeframes,metadata_mode ,recommended_mode):

    if metadata_mode not in ["reference_metadata", "qualifier_metadata"]:
        raise Exception

    if recommended_mode not in ["recommended", "non_recommended", "all"]:
        raise Exception

    for timeframe in timeframes:

        csv_ready_datatypes_dict = {}
        csv_ready_datatypes_dict["timeframe"] = []
        csv_ready_datatypes_dict["datatypes"] = []
        csv_ready_datatypes_dict["labels"] = []
        csv_ready_datatypes_dict["recommended_mode"] = []

        timeframe_files = glob.glob("data/" + timeframe[:21] + "/" + timeframe[22:] + \
                                    "/statistical_information/non_redundant/" + metadata_mode + "/" + \
                                    recommended_mode + "/accumulated_datatypes" +
                                                       "/accumulated_datatypes.json")
        with open(timeframe_files[0], "r") as timeframe_data:
            timeframe_dict = json.load(timeframe_data)

            # order the timeframe dict, so that the most used datatypes are in front
            timeframe_dict["datatypes"] = \
                collections.OrderedDict(
                    sorted(timeframe_dict["datatypes"].items(), key = lambda item: int(item[1])))

            for ID in timeframe_dict["datatypes"]:
                csv_ready_datatypes_dict["datatypes"].append(timeframe_dict["datatypes"][ID])
                csv_ready_datatypes_dict["labels"].append(ID)
                csv_ready_datatypes_dict["timeframe"].append(timeframe[:21])
                csv_ready_datatypes_dict["recommended_mode"].append(recommended_mode)

        df = pd.DataFrame(csv_ready_datatypes_dict)

        tmp = sns.catplot(x="labels", y="datatypes", kind="bar",
                          palette="Set2", dodge=False, hue="timeframe", col="recommended_mode",
                          data=df, aspect=1.4)

        plt.gcf().autofmt_xdate()

        tmp.savefig("data/statistical_information/query_research/non_redundant/"
                    + metadata_mode + "/" + recommended_mode + "/accumulated_datatypes/" +
                    timeframe[:22] + "accumulated_datatypes.png")

        plt.close()


def plot_top_accumulated_datatypes_overall(metadata_mode, recommended_mode):

    if metadata_mode not in ["reference_metadata", "qualifier_metadata"]:
        raise Exception

    if recommended_mode not in ["recommended", "non_recommended", "all"]:
        raise Exception


    csv_ready_datatypes_dict = {}
    csv_ready_datatypes_dict["datatypes"] = []
    csv_ready_datatypes_dict["labels"] = []
    csv_ready_datatypes_dict["recommended_mode"] = []


    timeframe_files = glob.glob("data/statistical_information/query_research/"
                                "non_redundant/" + metadata_mode + "/" + \
                                recommended_mode + "/accumulated_datatypes" + \
                                "/accumulated_datatypes.json")

    with open(timeframe_files[0], "r") as timeframe_data:
        # order the timeframe dict, so that the most used datatypes are in front
        timeframe_dict = json.load(timeframe_data)
        timeframe_dict["datatypes"] = \
        collections.OrderedDict(
            sorted(timeframe_dict["datatypes"].items(), key = lambda item: int(item[1])))

        for ID in timeframe_dict["datatypes"]:
            csv_ready_datatypes_dict["datatypes"].append(timeframe_dict["datatypes"][ID])
            csv_ready_datatypes_dict["labels"].append(ID)
            csv_ready_datatypes_dict["recommended_mode"].append(recommended_mode)

    df = pd.DataFrame(csv_ready_datatypes_dict)

    tmp = sns.catplot(x="labels", y="datatypes", kind="bar",
                      palette="Set2", dodge=False, col="recommended_mode",
                      data=df, aspect=1.4)


    plt.gcf().autofmt_xdate()

    tmp.savefig("data/statistical_information/query_research/non_redundant/"
                + metadata_mode + "/" + recommended_mode + "/accumulated_datatypes" +
                                "/accumulated_datatypes_overall.png")

    plt.close()




def plot_top_accumulated_datatypes_overall_percentage(metadata_mode ,recommended_mode):

    if metadata_mode not in ["reference_metadata", "qualifier_metadata"]:
        raise Exception

    if recommended_mode not in ["recommended", "non_recommended", "all"]:
        raise Exception


    csv_ready_datatypes_dict = {}
    csv_ready_datatypes_dict["datatypes_percentages"] = []
    csv_ready_datatypes_dict["labels"] = []
    csv_ready_datatypes_dict["recommended_mode"] = []

    timeframe_files = glob.glob("data/statistical_information/query_research/"
                                "non_redundant/" + metadata_mode + "/" +
                                recommended_mode + "/accumulated_datatypes" +
                                "/accumulated_datatypes.json")

    with open(timeframe_files[0], "r") as timeframe_data:
        # order the timeframe dict, so that the most used datatypes are in front
        timeframe_dict = json.load(timeframe_data)
        timeframe_dict["datatypes"] = \
        collections.OrderedDict(
            sorted(timeframe_dict["datatypes"].items(), key = lambda item: int(item[1])))

        for ID in timeframe_dict["datatypes"]:
            csv_ready_datatypes_dict["labels"].append(ID)
            csv_ready_datatypes_dict["datatypes_percentages"].append(
                timeframe_dict["datatypes"][ID] / timeframe_dict["total_accumulated_datatypes"])
            csv_ready_datatypes_dict["recommended_mode"].append(recommended_mode)


    df = pd.DataFrame(csv_ready_datatypes_dict)

    tmp = sns.catplot(x="labels", y="datatypes_percentages", kind="bar",
                      palette="Set2", dodge=False, col="recommended_mode",
                      data=df, aspect=1.4)

    plt.gcf().autofmt_xdate()

    tmp.savefig("data/statistical_information/query_research/non_redundant/"
                + metadata_mode + "/" + recommended_mode +
                "/accumulated_datatypes/accumulated_datatypes_overall_percentage.png")

    plt.close()


