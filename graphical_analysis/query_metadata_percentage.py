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
    csv_ready_dict_overall["metadata_type"] = []
    csv_ready_dict_overall["counted_metadata_queries_percentage"] = []
    csv_ready_dict_overall["metadata_occurrences_per_overall_queries"] = []
    csv_ready_dict_overall["metadata_occurrences_per_matching_metadata_queries"] = []

    for timeframe in TIMEFRAMES:
        path_to_timeframe_overall_query_information = "data/"+ timeframe[:21] + "/counted_queries.json"

        with open(path_to_timeframe_overall_query_information, "r") as timeframe_query_data:
            timeframe_query_dict = json.load(timeframe_query_data)

            for metadata in ["qualifier", "reference", "rank"]:

                csv_ready_dict_overall["timeframe"].append(timeframe[:21])
                csv_ready_dict_overall["metadata_type"].append(metadata)

                overall_queries = timeframe_query_dict["counted_queries"]
                metadata_queries = timeframe_query_dict["counted_metadata_queries"][metadata + "_metadata"]
                metadata_occurrences = timeframe_query_dict["counted_metadata_occurrences"][metadata + "_metadata"]

                csv_ready_dict_overall["counted_metadata_queries_percentage"].append(metadata_queries / overall_queries)
                csv_ready_dict_overall["metadata_occurrences_per_overall_queries"].\
                    append(metadata_occurrences / overall_queries)
                csv_ready_dict_overall["metadata_occurrences_per_matching_metadata_queries"].\
                    append(metadata_occurrences / metadata_queries)


    # plot the percentage data in a strip diagram

    df = pd.DataFrame(csv_ready_dict_overall)
    tmp = sns.catplot(x="timeframe", y="counted_metadata_queries_percentage", kind="strip",
                      palette="tab10", hue="metadata_type",
                      dodge=True, data=df, ci=None)

    plt.gcf().autofmt_xdate()

    tmp.savefig("data/counted_metadata_queries_percentage.png")

    plt.close()

    # plot the metadata per query data in a strip diagram

    df = pd.DataFrame(csv_ready_dict_overall)
    tmp = sns.catplot(x="timeframe", y="metadata_occurrences_per_overall_queries", kind="strip",
                      palette="tab10", hue="metadata_type",
                      dodge=True, data=df, ci=None)

    plt.gcf().autofmt_xdate()

    tmp.savefig("data/metadata_occurrences_per_overall_queries.png")

    plt.close()

    # plot the metadata per metadata query data in a strip diagram

    df = pd.DataFrame(csv_ready_dict_overall)
    tmp = sns.catplot(x="timeframe", y="metadata_occurrences_per_matching_metadata_queries", kind="strip",
                      palette="tab10", hue="metadata_type",
                      dodge=True, data=df, ci=None)

    plt.gcf().autofmt_xdate()

    tmp.savefig("data/metadata_occurrences_per_matching_metadata_queries.png")

    plt.close()

