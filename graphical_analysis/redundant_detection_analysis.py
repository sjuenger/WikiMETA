import seaborn as sns
import pandas as pd
import numpy as nm
import matplotlib.pyplot as plt
import glob
import json
import collections

TIMEFRAMES = [
    "2017-06-12_2017-07-09_organic",
    "2017-07-10_2017-08-06_organic",
    "2017-08-07_2017-09-03_organic",
    "2017-12-03_2017-12-30_organic",
    "2018-01-01_2018-01-28_organic",
    "2018-01-29_2018-02-25_organic",
    "2018-02-26_2018-03-25_organic"
]

DATA_TYPES_REFERENCE = [

    "reference_metadata/only_derived",
    "reference_metadata/only_reference_node",
    "reference_metadata/only_reference_property",
    "reference_metadata/derived_+_reference_node",
    "reference_metadata/derived_+_reference_property",
    "reference_metadata/reference_node_+_reference_property",
    "reference_metadata/all_three"
]

DATA_TYPES_QUALIFIER = [
    "qualifier_metadata/property_qualifier"
]

DATA_TYPES_RANK = [
    "rank_metadata/rank_property",
    "rank_metadata/best_rank_+_rank_property",
    "rank_metadata/normal_rank_+_rank_property",
    "rank_metadata/deprecated_rank_+_rank_property",
    "rank_metadata/best_+_normal_rank_+_rank_property",
    "rank_metadata/best_+_deprecated_rank_+_rank_property",
    "rank_metadata/normal_+_deprecated_rank_+_rank_property",
    "rank_metadata/all_ranks_+_rank_property",
    "rank_metadata/normal_rank",
    "rank_metadata/deprecated_rank",
    "rank_metadata/best_rank",
    "rank_metadata/best_+_normal_rank",
    "rank_metadata/best_+_deprecated_rank",
    "rank_metadata/normal_+_deprecated_rank",
    "rank_metadata/all_ranks"
]



def plot_redundant_detection_data_exact():


    for types in [DATA_TYPES_REFERENCE, DATA_TYPES_QUALIFIER, DATA_TYPES_RANK]:

        # generate .csv ready dataframe, through a formated dictionary for ALL timeframes overall
        csv_ready_dict_overall = {}
        csv_ready_dict_overall["queries"] = []
        csv_ready_dict_overall["total_amount_or_marked"] = []
        csv_ready_dict_overall["datatype"] = []
        csv_ready_dict_overall["metadata"] = []

        csv_ready_timeframe_heatmap_dict = {}
        csv_ready_timeframe_heatmap_dict["metadata_queries"] = []
        csv_ready_timeframe_heatmap_dict["percentage_on_total_metadata_queries"] = []
        csv_ready_timeframe_heatmap_dict["total_amount_or_marked"] = []
        csv_ready_timeframe_heatmap_dict["datatype"] = []
        csv_ready_timeframe_heatmap_dict["metadata"] = []
        csv_ready_timeframe_heatmap_dict["timeframe"] = []

        # to summarize the data from the multiple reference and qualifier data
        csv_ready_dict_overall_one_type = {}
        csv_ready_dict_overall_one_type["queries"] = []
        csv_ready_dict_overall_one_type["total_amount_or_marked"] = []
        csv_ready_dict_overall_one_type["datatype"] = []
        csv_ready_dict_overall_one_type["metadata"] = []

        for location in TIMEFRAMES:

            # generate .csv ready dataframe, through a formated dictionary for every timeframe
            csv_ready_dict_timeframe = {}
            csv_ready_dict_timeframe["queries"] = []
            csv_ready_dict_timeframe["total_amount_or_marked"] = []
            csv_ready_dict_timeframe["datatype"] = []
            csv_ready_dict_timeframe["metadata"] = []

            csv_ready_dict_timeframe_one_type = {}
            csv_ready_dict_timeframe_one_type["queries"] = []
            csv_ready_dict_timeframe_one_type["total_amount_or_marked"] = []
            csv_ready_dict_timeframe_one_type["datatype"] = []
            csv_ready_dict_timeframe_one_type["metadata"] = []

            i = 0
            for type in types:

                # Retrieve the generated redundant_detection data
                information_path = "data/statistical_information/redundant_detection/" + location[:21] + \
                       "/" + type + "_renaming_information.json"

                with open(information_path) as information_data:

                    information_dict = json.load(information_data)

                    print(information_dict)

                    csv_ready_dict_timeframe["queries"].append(information_dict["Total queries: "])
                    csv_ready_dict_timeframe["total_amount_or_marked"].append("Total Queries")

                    csv_ready_dict_timeframe["queries"].append(information_dict["Queries marked: "])
                    csv_ready_dict_timeframe["total_amount_or_marked"].append("Queries marked")


                    csv_ready_timeframe_heatmap_dict["metadata_queries"].\
                        append( information_dict["Total queries: "] )

                    csv_ready_timeframe_heatmap_dict["total_amount_or_marked"].append("Total Queries")

                    csv_ready_timeframe_heatmap_dict["metadata_queries"].\
                        append( information_dict["Queries marked: "] )

                    csv_ready_timeframe_heatmap_dict["total_amount_or_marked"].append("Queries marked")

                    csv_ready_timeframe_heatmap_dict["timeframe"].append(location[:21])
                    csv_ready_timeframe_heatmap_dict["timeframe"].append(location[:21])


                    # format the type a bit nicer
                    # e.g., rank_metadata/deprecated_rank_+_rank_property -> deprecated rank & rank property
                    nice_type = type.split("/")[1].replace("_", " ").replace("+", "&")

                    csv_ready_dict_timeframe["datatype"].append(nice_type)
                    csv_ready_dict_timeframe["datatype"].append(nice_type)

                    csv_ready_timeframe_heatmap_dict["datatype"].append(nice_type)
                    csv_ready_timeframe_heatmap_dict["datatype"].append(nice_type)

                    # extract the metadata
                    # e.g., rank_metadata/deprecated_rank_+_rank_property -> rank metadata
                    metadata = type.split("/")[0].replace(" ", "")

                    csv_ready_dict_timeframe["metadata"].append(metadata)
                    csv_ready_dict_timeframe["metadata"].append(metadata)

                    csv_ready_timeframe_heatmap_dict["metadata"].append(metadata)
                    csv_ready_timeframe_heatmap_dict["metadata"].append(metadata)

                    # update the overall dict and summarize the timeframe values
                    if len(csv_ready_dict_overall["queries"]) <= 2*i:
                        csv_ready_dict_overall["queries"].append(information_dict["Total queries: "])
                        csv_ready_dict_overall["total_amount_or_marked"].append("Total Queries")

                        csv_ready_dict_overall["queries"].append(information_dict["Queries marked: "])
                        csv_ready_dict_overall["total_amount_or_marked"].append("Queries marked")

                        csv_ready_dict_overall["datatype"].append(nice_type)
                        csv_ready_dict_overall["datatype"].append(nice_type)

                        csv_ready_dict_overall["metadata"].append(metadata)
                        csv_ready_dict_overall["metadata"].append(metadata)


                    else:
                        csv_ready_dict_overall["queries"][i] += information_dict["Total queries: "]
                        csv_ready_dict_overall["total_amount_or_marked"][i] = "Total Queries"

                        csv_ready_dict_overall["queries"][i+1] += information_dict["Queries marked: "]
                        csv_ready_dict_overall["total_amount_or_marked"][i+1] = "Queries marked"

                        csv_ready_dict_overall["datatype"][i] = nice_type
                        csv_ready_dict_overall["datatype"][i+1] = nice_type

                        csv_ready_dict_overall["metadata"][i] = metadata
                        csv_ready_dict_overall["metadata"][i+1] = metadata


                    # update the overall dict to narrow it down to one type
                    if len(csv_ready_dict_overall_one_type["queries"]) == 0:
                        csv_ready_dict_overall_one_type["queries"].append(information_dict["Total queries: "])
                        csv_ready_dict_overall_one_type["total_amount_or_marked"].append("Total Queries")

                        csv_ready_dict_overall_one_type["queries"].append(information_dict["Queries marked: "])
                        csv_ready_dict_overall_one_type["total_amount_or_marked"].append("Queries marked")

                        csv_ready_dict_overall_one_type["datatype"].append(nice_type)
                        csv_ready_dict_overall_one_type["datatype"].append(nice_type)

                        csv_ready_dict_overall_one_type["metadata"].append(metadata)
                        csv_ready_dict_overall_one_type["metadata"].append(metadata)



                    else:
                        csv_ready_dict_overall_one_type["queries"][0] += information_dict["Total queries: "]
                        csv_ready_dict_overall_one_type["total_amount_or_marked"][0] = "Total Queries"

                        csv_ready_dict_overall_one_type["queries"][1] += information_dict["Queries marked: "]
                        csv_ready_dict_overall_one_type["total_amount_or_marked"][1] = "Queries marked"

                        csv_ready_dict_overall_one_type["datatype"][0] = metadata
                        csv_ready_dict_overall_one_type["datatype"][1] = metadata

                        csv_ready_dict_overall_one_type["metadata"][0] = metadata
                        csv_ready_dict_overall_one_type["metadata"][1] = metadata



                    # update the overall dict to narrow it down to one type per timeframe
                    if len(csv_ready_dict_timeframe_one_type["queries"]) == 0:
                        csv_ready_dict_timeframe_one_type["queries"].append(information_dict["Total queries: "])
                        csv_ready_dict_timeframe_one_type["total_amount_or_marked"].append("Total Queries")

                        csv_ready_dict_timeframe_one_type["queries"].append(information_dict["Queries marked: "])
                        csv_ready_dict_timeframe_one_type["total_amount_or_marked"].append("Queries marked")

                        csv_ready_dict_timeframe_one_type["datatype"].append(nice_type)
                        csv_ready_dict_timeframe_one_type["datatype"].append(nice_type)

                        csv_ready_dict_timeframe_one_type["metadata"].append(metadata)
                        csv_ready_dict_timeframe_one_type["metadata"].append(metadata)


                    else:
                        csv_ready_dict_timeframe_one_type["queries"][0] += information_dict["Total queries: "]
                        csv_ready_dict_timeframe_one_type["total_amount_or_marked"][0] = "Total Queries"

                        csv_ready_dict_timeframe_one_type["queries"][1] += information_dict["Queries marked: "]
                        csv_ready_dict_timeframe_one_type["total_amount_or_marked"][1] = "Queries marked"

                        csv_ready_dict_timeframe_one_type["datatype"][0] = metadata
                        csv_ready_dict_timeframe_one_type["datatype"][1] = metadata

                        csv_ready_dict_timeframe_one_type["metadata"][0] = metadata
                        csv_ready_dict_timeframe_one_type["metadata"][1] = metadata




                i += 2

            # insert the percentage information for the test dict with the help of the dict per metadata per timeframe
            for index in range(len(csv_ready_timeframe_heatmap_dict["timeframe"])):
                if csv_ready_timeframe_heatmap_dict["timeframe"][index] == location[:21]:
                    if index % 2 == 0:
                        csv_ready_timeframe_heatmap_dict["percentage_on_total_metadata_queries"]. \
                            append(csv_ready_timeframe_heatmap_dict["metadata_queries"][index] / csv_ready_dict_timeframe_one_type["queries"][0])
                    else:
                        csv_ready_timeframe_heatmap_dict["percentage_on_total_metadata_queries"]. \
                            append((csv_ready_timeframe_heatmap_dict["metadata_queries"][index-1]
                                    - csv_ready_timeframe_heatmap_dict["metadata_queries"][index] )
                                   / (csv_ready_dict_timeframe_one_type["queries"][0] -
                                      csv_ready_dict_timeframe_one_type["queries"][1]))


            # save the dict for the timeframe
            timeframe_path = "data/statistical_information/redundant_detection/" + location[:21] \
                        + "/" + type.split("/")[0] +  "/overall_redundant_information_exact.json"
            with open(timeframe_path, "w") as overall_data:
                json.dump(csv_ready_dict_timeframe_one_type, overall_data)

            # plot the timeframe overall data
            df = pd.DataFrame(csv_ready_dict_timeframe_one_type)
            tmp = sns.catplot(x="datatype", y="queries", kind="bar",
                              palette="tab10", hue="total_amount_or_marked",
                              dodge=True,  data=df, ci=None)

            tmp.savefig( "data/statistical_information/redundant_detection/" + location[:21]
                        + "/" + type.split("/")[0] +  "/overall_redundant_information_exact.png")

            plt.close()


            # plot the timeframe data
            df = pd.DataFrame(csv_ready_dict_timeframe)

            # plot with a aspect = 1.5 for the rank metadata and without vertical labels for the qualifiers
            if "rank_metadata" in type:
                tmp = sns.catplot(x="datatype", y="queries", kind="bar",
                                  palette="tab10", hue="total_amount_or_marked",
                                  dodge=True, col="metadata", aspect=1.5, data=df, ci=None)

                plt.gcf().autofmt_xdate()

            elif "qualifier_metadata" in type:
                tmp = sns.catplot(x="datatype", y="queries", kind="bar",
                                  palette="tab10", hue="total_amount_or_marked",
                                  dodge=True, col="metadata", data=df, ci=None)

            else:
                tmp = sns.catplot(x="datatype", y="queries", kind="bar",
                                  palette="tab10", hue="total_amount_or_marked",
                                  dodge=True, col="metadata", data=df, ci=None)

                plt.gcf().autofmt_xdate()

            tmp.savefig("data/statistical_information/redundant_detection/" + location[:21]
                        + "/" + type.split("/")[0] + "/redundant_information_exact.png")

            plt.close()


        # plot the overall data
        df = pd.DataFrame(csv_ready_dict_overall)

        # save the overall dict
        overall_path = "data/statistical_information/redundant_detection/"\
        + types[0].split("/")[0] + "/redundant_information_exact.json"
        with open(overall_path, "w") as overall_data:
            json.dump(csv_ready_dict_overall, overall_data)

        # plot with a aspect = 1.5 for the rank metadata and without vertical labels for the qualifiers
        if "rank_metadata" in types[0]:
            color_list = sns.color_palette("Paired")
            color_list = [color_list[3], color_list[2]]
            tmp = sns.catplot(x="datatype", y="queries", kind="bar",
                              palette=color_list, hue="total_amount_or_marked",
                              dodge=True, col="metadata", aspect=1.5, data=df)

            plt.gcf().autofmt_xdate()

        elif "qualifier_metadata" in types[0]:
            color_list = sns.color_palette("Paired")
            color_list = [color_list[5], color_list[4]]
            tmp = sns.catplot(x="datatype", y="queries", kind="bar",
                              palette=color_list, hue="total_amount_or_marked",
                              dodge=True, col="metadata", data=df)

        else:
            color_list = sns.color_palette("Paired")
            color_list = [color_list[7], color_list[6]]
            tmp = sns.catplot(x="datatype", y="queries", kind="bar",
                              palette=color_list, hue="total_amount_or_marked",
                              dodge=True, col="metadata", data=df)

            plt.gcf().autofmt_xdate()

        tmp.savefig("data/statistical_information/redundant_detection/"
                    + types[0].split("/")[0] + "/redundant_information_exact.png")

        plt.close()



        # plot the overall data for one type only (only for the qualifiers and references,
        # .. because the qualifiers already only have one type)
        df = pd.DataFrame(csv_ready_dict_overall_one_type)

        # save the overall dict
        overall_path = "data/statistical_information/redundant_detection/" \
                       + types[0].split("/")[0] + "/overall_redundant_information_exact.json"
        with open(overall_path, "w") as overall_data:
            json.dump(csv_ready_dict_overall, overall_data)

        color_list = sns.color_palette("Paired")
        color_list = [color_list[1], color_list[0]]

        tmp = sns.catplot(x="datatype", y="queries", kind="bar",
                          palette=color_list,
                          hue="total_amount_or_marked",
                          dodge=True, data=df, ci=None)

        tmp.savefig("data/statistical_information/redundant_detection/"
                    + types[0].split("/")[0] + "/overall_redundant_information_exact.png")

        plt.close()





        # plot the heatmap of redundant occurrences of metadata per type
        tmp_dict = {}
        tmp_dict["datatype"] = []
        tmp_dict["timeframe"] = []
        tmp_dict["queries"] = []
        tmp_dict["percentage_on_total_metadata_queries"] = []

        for i in range(len(csv_ready_timeframe_heatmap_dict["metadata"])):

            if "Total" in csv_ready_timeframe_heatmap_dict["total_amount_or_marked"][i]:

                tmp_dict["datatype"].append(csv_ready_timeframe_heatmap_dict["datatype"][i])
                tmp_dict["timeframe"].append(csv_ready_timeframe_heatmap_dict["timeframe"][i].replace("_", " -\n"))
                tmp_dict["queries"].append(csv_ready_timeframe_heatmap_dict["metadata_queries"][i])
                tmp_dict["percentage_on_total_metadata_queries"].\
                    append(csv_ready_timeframe_heatmap_dict["percentage_on_total_metadata_queries"][i])


        df = pd.DataFrame(tmp_dict)

        print(tmp_dict)
        print(tmp_dict["datatype"])
        print(tmp_dict["timeframe"])
        print(tmp_dict["queries"])
        print(tmp_dict["percentage_on_total_metadata_queries"])
        print(len(tmp_dict["queries"]))

        df = pd.pivot_table(data=df,
                            index='datatype',
                            values='percentage_on_total_metadata_queries',
                            columns='timeframe', sort = False)

        fig, ax = plt.subplots(figsize=(10, 6))
        tmp = sns.heatmap(df, ax=ax, vmin=0, vmax =1, annot=True)
        tmp.figure.tight_layout()
        #tmp.figure.subplots_adjust(left=0.45, bottom=0.6)

        plt.gcf().autofmt_xdate()

        tmp.get_figure().savefig("data/redundant_" + types[0].split("/")[0] + ".png")

        plt.close()


        # plot the heatmap of redundant occurrences of metadata per type
        tmp_dict = {}
        tmp_dict["datatype"] = []
        tmp_dict["timeframe"] = []
        tmp_dict["queries"] = []
        tmp_dict["percentage_on_total_metadata_queries"] = []

        for i in range(len(csv_ready_timeframe_heatmap_dict["metadata"])):

            if "marked" in csv_ready_timeframe_heatmap_dict["total_amount_or_marked"][i]:

                tmp_dict["datatype"].append(csv_ready_timeframe_heatmap_dict["datatype"][i])
                tmp_dict["timeframe"].append(csv_ready_timeframe_heatmap_dict["timeframe"][i].replace("_", " -\n"))
                tmp_dict["queries"].append(csv_ready_timeframe_heatmap_dict["metadata_queries"][i])
                tmp_dict["percentage_on_total_metadata_queries"].append(csv_ready_timeframe_heatmap_dict["percentage_on_total_metadata_queries"][i])


        df = pd.DataFrame(tmp_dict)

        print(tmp_dict)
        print(tmp_dict["datatype"])
        print(tmp_dict["timeframe"])
        print(tmp_dict["queries"])
        print(tmp_dict["percentage_on_total_metadata_queries"])
        print(len(tmp_dict["queries"]))

        df = pd.pivot_table(data=df,
                            index='datatype',
                            values='percentage_on_total_metadata_queries',
                            columns='timeframe', sort = False)

        fig, ax = plt.subplots(figsize=(10, 6))
        tmp = sns.heatmap(df, ax=ax, annot=True, vmin = 0, vmax = 1)
        tmp.figure.tight_layout()
        #tmp.figure.subplots_adjust(left=0.45, bottom=0.6)

        plt.gcf().autofmt_xdate()

        tmp.get_figure().savefig("data/non-redundant_" + types[0].split("/")[0] + ".png")

        plt.close()



