import json
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as nm

TIMEFRAMES = [
    "2017-06-12_2017-07-09_organic",
    "2017-07-10_2017-08-06_organic",
    "2017-08-07_2017-09-03_organic",
    "2017-12-03_2017-12-30_organic",
    "2018-01-01_2018-01-28_organic",
    "2018-01-29_2018-02-25_organic",
    "2018-02-26_2018-03-25_organic"
]

# this method calculates and shows the percentage of queries with metadata to queries without metadata per timeframe
def display_percentage_queries_with_metadata():

    csv_ready_dict_overall = {}
    csv_ready_dict_overall["timeframe"] = []
    csv_ready_dict_overall["metadata type"] = []

    csv_ready_dict_overall["counted metadata queries percentage"] = []
    csv_ready_dict_overall["counted metadata queries"] = []

    csv_ready_dict_overall["counted non redundant metadata queries"] = []


    csv_ready_dict_overall["metadata occurrences per overall queries"] = []
    csv_ready_dict_overall["metadata occurrences per matching queries"] = []

    csv_ready_dict_overall["non redundant metadata occurrences per matching queries"] = []

    for timeframe in TIMEFRAMES:
        path_to_timeframe_overall_query_information = "data/"+ timeframe[:21] + "/counted_queries.json"

        with open(path_to_timeframe_overall_query_information, "r") as timeframe_query_data:
            timeframe_query_dict = json.load(timeframe_query_data)

            for metadata in ["qualifier", "reference", "rank"]:

                csv_ready_dict_overall["timeframe"].append(timeframe[:21].replace("_", " - "))
                csv_ready_dict_overall["metadata type"].append(metadata)

                overall_queries = timeframe_query_dict["counted_queries"]
                metadata_queries = timeframe_query_dict["counted_metadata_queries"][metadata + "_metadata"]
                metadata_occurrences = timeframe_query_dict["counted_metadata_occurrences"][metadata + "_metadata"]

                non_redundant_metadata_queries = \
                    timeframe_query_dict["counted_non_redundant_metadata_queries"][metadata + "_metadata"]
                non_redundant_metadata_occurrences = \
                    timeframe_query_dict["counted_non_redundant_metadata_occurrences"][metadata + "_metadata"]

                csv_ready_dict_overall["counted metadata queries"].append(metadata_queries)
                csv_ready_dict_overall["counted non redundant metadata queries"].append(non_redundant_metadata_queries)

                csv_ready_dict_overall["counted metadata queries percentage"].append(metadata_queries / overall_queries)
                csv_ready_dict_overall["metadata occurrences per overall queries"].\
                    append(metadata_occurrences / overall_queries)

                csv_ready_dict_overall["metadata occurrences per matching queries"].\
                    append(metadata_occurrences / metadata_queries)
                csv_ready_dict_overall["non redundant metadata occurrences per matching queries"].\
                    append(non_redundant_metadata_occurrences / non_redundant_metadata_queries)



    # plot the percentage data in a strip diagram
    df = pd.DataFrame(csv_ready_dict_overall)
    tmp = sns.catplot(x="timeframe", y="counted metadata queries percentage", kind="point",
                      palette="tab10", hue="metadata type", ymin=0,
                      dodge=True, data=df, ci=None)

    plt.gcf().autofmt_xdate()
    plt.ylim(0,)

    tmp.savefig("data/counted_metadata_queries_percentage_strip.png")

    plt.close()

    # plot the metadata per query data in a strip diagram
    df = pd.DataFrame(csv_ready_dict_overall)
    tmp = sns.catplot(x="timeframe", y="metadata occurrences per overall queries", kind="point",
                      palette="tab10", hue="metadata type",  ymin=0,
                      dodge=True, data=df, ci=None)

    plt.gcf().autofmt_xdate()
    plt.ylim(0,)

    tmp.savefig("data/metadata_occurrences_per_overall_queries_strip.png")

    plt.close()

    # plot the metadata per matching metadata query data in a strip diagram
    df = pd.DataFrame(csv_ready_dict_overall)
    tmp = sns.catplot(x="timeframe", y="metadata occurrences per matching queries", kind="point",
                      palette="tab10", hue="metadata type",  ymin=0,
                      dodge=True, data=df, ci=None)

    plt.gcf().autofmt_xdate()
    plt.ylim(0,)

    tmp.savefig("data/metadata_occurrences_per_matching_metadata_queries_strip.png")

    plt.close()


    # plot the non_redundant metadata per non_redundant matching metadata query data in a strip diagram
    df = pd.DataFrame(csv_ready_dict_overall)
    tmp = sns.catplot(x="timeframe", y="non redundant metadata occurrences per matching queries",
                      kind="point",
                      palette="tab10", hue="metadata type",  ymin=0,
                      dodge=True, data=df, ci=None)

    plt.gcf().autofmt_xdate()
    plt.ylim(0,)

    tmp.savefig("data/non_redundant_metadata_occurrences_per_matching_non_redundant_metadata_queries_strip.png")

    plt.close()


    # plot the absolute amount of metadata queries
    df = pd.DataFrame(csv_ready_dict_overall)
    tmp = sns.catplot(x="metadata type", y="counted metadata queries", kind="strip",
                      palette="tab10",
                      dodge=True, data=df, ci=None)

    plt.gcf().autofmt_xdate()
    plt.ylim(0,)

    tmp.savefig("data/counted_metadata_queries_strip.png")

    plt.close()




