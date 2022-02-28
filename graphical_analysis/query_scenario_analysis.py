import json
import glob
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt

# plot only the NON-redundant data
def plot_timeframe_metadata_distribution_per_datatype(timeframes, datatypes_list):

    for datatypes in datatypes_list:

        for datatype in datatypes:

            csv_ready_scenario_per_datatype_dict = {}
            csv_ready_scenario_per_datatype_dict["timeframe"] = []
            csv_ready_scenario_per_datatype_dict["datatype"] = []
            csv_ready_scenario_per_datatype_dict["type_looking_for"] = []
            csv_ready_scenario_per_datatype_dict["scenario_name"] = []
            csv_ready_scenario_per_datatype_dict["scenario_count"] = []
            csv_ready_scenario_per_datatype_dict["scenario_percentage"] = []
            csv_ready_scenario_per_datatype_dict["total_occurrences"] = []
            csv_ready_scenario_per_datatype_dict["total_queries"] = []
            csv_ready_scenario_per_datatype_dict["total_scenarios"] = []


            for timeframe in timeframes:


                # get the path to the location information of the timeframe scenario data per
                #   datatype
                information_path = "data/" + timeframe[:21] + "/" + timeframe[22:] + \
                                    "/" + datatype.split("/")[0] + \
                                   "/statistical_information/non_redundant/" +\
                                    datatype.split("/")[1] + ".json"

                with open(information_path, "r") as stat_info_scenarios_data:
                    stat_info_scenarios_dict = json.load(stat_info_scenarios_data)

                    for dict in stat_info_scenarios_dict["found_scenarios"]["list_per_search"]:

                        for PID in dict:
                            if PID not in ["looking_for", "total_occurrences", "total_scenarios"]:

                                csv_ready_scenario_per_datatype_dict["scenario_name"].append(PID)
                                csv_ready_scenario_per_datatype_dict["scenario_count"].\
                                    append(dict[PID])
                                if dict["total_occurrences"]>0:
                                    csv_ready_scenario_per_datatype_dict["scenario_percentage"].\
                                        append(dict[PID] / dict["total_scenarios"])
                                else:
                                    csv_ready_scenario_per_datatype_dict["scenario_percentage"].\
                                        append(0)

                                csv_ready_scenario_per_datatype_dict["timeframe"].\
                                    append(timeframe[:21])
                                csv_ready_scenario_per_datatype_dict["datatype"].append(datatype.split("/")[0])
                                csv_ready_scenario_per_datatype_dict["type_looking_for"]. \
                                    append(str(dict["looking_for"]).replace(" ", "\n"))
                                csv_ready_scenario_per_datatype_dict["total_occurrences"]. \
                                    append(dict["total_occurrences"])
                                csv_ready_scenario_per_datatype_dict["total_scenarios"]. \
                                    append(dict["total_scenarios"])
                                csv_ready_scenario_per_datatype_dict["total_queries"].\
                                    append(stat_info_scenarios_dict["total_queries"])



            # display the non-redundant scenario information per datatype and per timeframe in a heatmap
            for list_per_search in stat_info_scenarios_dict["found_scenarios"]["list_per_search"]:

                tmp_dict = {}
                tmp_dict["scenario_name"] = []
                tmp_dict["timeframe"] = []
                tmp_dict["scenario_percentage"] = []

                for i in range(len(csv_ready_scenario_per_datatype_dict["timeframe"])):
                    if list_per_search["looking_for"].replace(" ", "\n") == \
                            csv_ready_scenario_per_datatype_dict["type_looking_for"][i]:

                        tmp_dict["scenario_name"].append(csv_ready_scenario_per_datatype_dict["scenario_name"][i])
                        tmp_dict["timeframe"].append(csv_ready_scenario_per_datatype_dict["timeframe"][i])
                        tmp_dict["scenario_percentage"].append(\
                            csv_ready_scenario_per_datatype_dict["scenario_percentage"][i])


                print(datatype.split("/")[1])
                print(str(list_per_search["looking_for"]))
                print(tmp_dict)

                df = pd.DataFrame(tmp_dict)

                df = pd.pivot_table(data=df,
                                    index='scenario_name',
                                    values='scenario_percentage',
                                    columns='timeframe')

                mask = (df == 0)
                fig, ax = plt.subplots(figsize=(16, 10))
                tmp = sns.heatmap(df, ax=ax, annot=True, vmin = 0,
                                  vmax = 1, mask=mask, cmap="YlGnBu", linewidths=.5)
                tmp.figure.tight_layout()
                #tmp.figure.subplots_adjust(left=0.45, bottom=0.6)

                plt.gcf().autofmt_xdate()
                save_path = "data/statistical_information/query_research/non_redundant/" \
                                            + datatype.split("/")[0] + "/scenarios/" +  \
                                            datatype.split("/")[1] + "_" + \
                                             str(list_per_search["looking_for"]).\
                                            replace("'", "'").replace(",", ",").\
                                            replace("\n", " ").replace("[", "[").\
                                            replace("http://www.", "").\
                                            replace("/", "\\") + ".png"

                tmp.get_figure().savefig(save_path)

                plt.close()

            # plot the overll numbers of found scenarios per datatype and per timeframe
            #   for the total scenarios
            df = pd.DataFrame(csv_ready_scenario_per_datatype_dict)

            tmp = sns.catplot(x="timeframe", y="total_scenarios", kind="bar",
                              palette="tab10", dodge=True, hue="type_looking_for",
                              data=df)

            plt.gcf().autofmt_xdate()

            save_path = "data/statistical_information/query_research/non_redundant/"+\
                datatype.split("/")[0] + "/scenarios/" + datatype.split("/")[1] +"_total_scenarios.png"

            tmp.savefig(save_path)

            plt.close()


            # plot the overll numbers of found scenarios per datatype and per timeframe
            #   for the total occurrences
            df = pd.DataFrame(csv_ready_scenario_per_datatype_dict)

            tmp = sns.catplot(x="timeframe", y="total_occurrences", kind="bar",
                              palette="tab10", dodge=True, hue="type_looking_for",
                              data=df)

            plt.gcf().autofmt_xdate()

            save_path = "data/statistical_information/query_research/non_redundant/"+\
                datatype.split("/")[0] + "/scenarios/" + datatype.split("/")[1] +"_total_occurrences.png"

            tmp.savefig(save_path)

            plt.close()


            # plot the overll numbers of found scenarios per datatype and per timeframe
            #   for the total queries
            df = pd.DataFrame(csv_ready_scenario_per_datatype_dict)

            tmp = sns.catplot(x="timeframe", y="total_queries", kind="bar",
                              palette="tab10", dodge=True, hue="type_looking_for",
                              data=df)

            plt.gcf().autofmt_xdate()

            save_path = "data/statistical_information/query_research/non_redundant/"+\
                datatype.split("/")[0] + "/scenarios/" + datatype.split("/")[1] +"_total_queries.png"

            tmp.savefig(save_path)

            plt.close()




# plot only the NON-redundant data
def plot_timeframe_metadata_distribution(timeframes, metadata):

    if metadata not in ["reference_metadata", "rank_metadata", "qualifier_metadata"]:
        raise Exception

    csv_ready_scenario_dict = {}
    csv_ready_scenario_dict["timeframe"] = []
    csv_ready_scenario_dict["datatype"] = []
    csv_ready_scenario_dict["type_looking_for"] = []
    csv_ready_scenario_dict["scenario_name"] = []
    csv_ready_scenario_dict["scenario_count"] = []
    csv_ready_scenario_dict["scenario_percentage"] = []
    csv_ready_scenario_dict["total_occurrences"] = []
    csv_ready_scenario_dict["total_queries"] = []
    csv_ready_scenario_dict["total_scenarios"] = []


    for timeframe in timeframes:

        # get the path to the location information of the timeframe scenario data per
        #   datatype
        information_path = "data/" + timeframe[:21] + "/" + timeframe[22:] + \
                            "/statistical_information/non_redundant/" +\
                            metadata + "/" + metadata + ".json"

        with open(information_path, "r") as stat_info_scenarios_data:
            stat_info_scenarios_dict = json.load(stat_info_scenarios_data)

            for dict in stat_info_scenarios_dict["found_scenarios"]:

                if dict not in ["looking_for", "total_occurrences", "total_scenarios"]:

                    csv_ready_scenario_dict["scenario_name"].append(dict)

                    csv_ready_scenario_dict["scenario_count"].\
                        append(stat_info_scenarios_dict["found_scenarios"][dict])

                    if stat_info_scenarios_dict["found_scenarios"]["total_occurrences"]>0:
                        csv_ready_scenario_dict["scenario_percentage"].\
                            append(stat_info_scenarios_dict["found_scenarios"][dict]
                                   / stat_info_scenarios_dict["found_scenarios"]["total_scenarios"])
                    else:
                        csv_ready_scenario_dict["scenario_percentage"].\
                            append(0)

                    csv_ready_scenario_dict["timeframe"].\
                        append(timeframe[:21])
                    csv_ready_scenario_dict["datatype"].append(metadata)
                    csv_ready_scenario_dict["type_looking_for"]. \
                        append(str(stat_info_scenarios_dict["found_scenarios"]["looking_for"]).
                               replace(" ", "\n"))
                    csv_ready_scenario_dict["total_occurrences"]. \
                        append(stat_info_scenarios_dict["found_scenarios"]["total_occurrences"])
                    csv_ready_scenario_dict["total_scenarios"]. \
                        append(stat_info_scenarios_dict["found_scenarios"]["total_scenarios"])
                    csv_ready_scenario_dict["total_queries"].\
                        append(stat_info_scenarios_dict["total_queries"])


    # add a 'overall' timeframe to display the total scenario information
    path_to_overall = "data/statistical_information/query_research/non_redundant/" +\
                            metadata + "/" + metadata + ".json"
    with open(path_to_overall, "r") as overall_data:
        overall_dict = json.load(overall_data)

        for dict in overall_dict["found_scenarios"]:

            if dict not in ["looking_for", "total_occurrences", "total_scenarios"]:

                csv_ready_scenario_dict["scenario_name"].append(dict)

                csv_ready_scenario_dict["scenario_count"]. \
                    append(overall_dict["found_scenarios"][dict])

                if overall_dict["found_scenarios"]["total_occurrences"] > 0:
                    csv_ready_scenario_dict["scenario_percentage"]. \
                        append(overall_dict["found_scenarios"][dict]
                               / overall_dict["found_scenarios"]["total_scenarios"])
                else:
                    csv_ready_scenario_dict["scenario_percentage"]. \
                        append(0)

                csv_ready_scenario_dict["timeframe"]. \
                    append("total")
                csv_ready_scenario_dict["datatype"].append(metadata)
                csv_ready_scenario_dict["type_looking_for"]. \
                    append(str(overall_dict["found_scenarios"]["looking_for"]).
                           replace(" ", "\n"))
                csv_ready_scenario_dict["total_occurrences"]. \
                    append(overall_dict["found_scenarios"]["total_occurrences"])
                csv_ready_scenario_dict["total_scenarios"]. \
                    append(overall_dict["found_scenarios"]["total_scenarios"])
                csv_ready_scenario_dict["total_queries"]. \
                    append(overall_dict["total_queries"])







    tmp_dict = {}
    tmp_dict["scenario_name"] = []
    tmp_dict["timeframe"] = []
    tmp_dict["scenario_percentage"] = []

    for i in range(len(csv_ready_scenario_dict["timeframe"])):
        tmp_dict["scenario_name"].append(csv_ready_scenario_dict["scenario_name"][i])
        tmp_dict["timeframe"].append(csv_ready_scenario_dict["timeframe"][i])
        tmp_dict["scenario_percentage"].append(\
            csv_ready_scenario_dict["scenario_percentage"][i])

    df = pd.DataFrame(tmp_dict)

    df = pd.pivot_table(data=df,
                        index='scenario_name',
                        values='scenario_percentage',
                        columns='timeframe')

    mask = (df == 0)
    fig, ax = plt.subplots(figsize=(16, 10)) # 16 10
    tmp = sns.heatmap(df, ax=ax, annot=True, vmin = 0, vmax = 1, mask=mask, cmap="YlGnBu", linewidths=.5)
    tmp.figure.tight_layout()
    #tmp.figure.subplots_adjust(left=0.45, bottom=0.6)

    plt.gcf().autofmt_xdate()
    save_path = "data/statistical_information/query_research/non_redundant/" \
                                + metadata + "/scenarios/overall_scenarios.png"

    tmp.get_figure().savefig(save_path)

    plt.close()

    # plot the overll numbers of found scenarios per datatype and per timeframe
    #   for the total scenarios
    df = pd.DataFrame(csv_ready_scenario_dict)

    tmp = sns.catplot(x="timeframe", y="total_scenarios", kind="bar",
                      palette="tab10", dodge=True, hue="type_looking_for",
                      data=df)

    plt.gcf().autofmt_xdate()

    save_path = "data/statistical_information/query_research/non_redundant/"+\
        metadata + "/scenarios/total_scenarios.png"

    tmp.savefig(save_path)

    plt.close()


    # plot the overll numbers of found scenarios per datatype and per timeframe
    #   for the total occurrences
    df = pd.DataFrame(csv_ready_scenario_dict)

    tmp = sns.catplot(x="timeframe", y="total_occurrences", kind="bar",
                      palette="tab10", dodge=True, hue="type_looking_for",
                      data=df)

    plt.gcf().autofmt_xdate()

    save_path = "data/statistical_information/query_research/non_redundant/"+\
        metadata + "/scenarios/total_occurrences.png"

    tmp.savefig(save_path)

    plt.close()


    # plot the overll numbers of found scenarios per datatype and per timeframe
    #   for the total queries
    df = pd.DataFrame(csv_ready_scenario_dict)

    tmp = sns.catplot(x="timeframe", y="total_queries", kind="bar",
                      palette="tab10", dodge=True, hue="type_looking_for",
                      data=df)

    plt.gcf().autofmt_xdate()

    save_path = "data/statistical_information/query_research/non_redundant/"+\
        metadata + "/scenarios/total_queries.png"

    tmp.savefig(save_path)

    plt.close()


