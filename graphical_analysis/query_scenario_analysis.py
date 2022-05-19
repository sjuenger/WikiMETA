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
            csv_ready_scenario_per_datatype_dict["type looking for"] = []
            csv_ready_scenario_per_datatype_dict["scenario name"] = []
            csv_ready_scenario_per_datatype_dict["scenario count"] = []
            csv_ready_scenario_per_datatype_dict["scenario percentage"] = []
            csv_ready_scenario_per_datatype_dict["total occurrences"] = []
            csv_ready_scenario_per_datatype_dict["total queries"] = []
            csv_ready_scenario_per_datatype_dict["total scenarios"] = []

            total_query_count_per_looking_for_per_scenario = {}
            total_query_count_per_looking_for = {}
            total_scenario_count_per_looking_for = {}
            total_occurrences_count_per_looking_for = {}


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

                        if str(dict["looking_for"]).replace(" ", "\n") in total_query_count_per_looking_for:
                            total_query_count_per_looking_for[str(dict["looking_for"]).replace(" ", "\n")]\
                                += stat_info_scenarios_dict["total_queries"]
                            total_occurrences_count_per_looking_for[str(dict["looking_for"]).replace(" ", "\n")]\
                                += dict["total_occurrences"]
                            total_scenario_count_per_looking_for[str(dict["looking_for"]).replace(" ", "\n")]\
                                += dict["total_scenarios"]
                        else:
                            total_query_count_per_looking_for[str(dict["looking_for"]).replace(" ", "\n")]\
                                = stat_info_scenarios_dict["total_queries"]
                            total_occurrences_count_per_looking_for[str(dict["looking_for"]).replace(" ", "\n")]\
                                = dict["total_occurrences"]
                            total_scenario_count_per_looking_for[str(dict["looking_for"]).replace(" ", "\n")]\
                                = dict["total_scenarios"]


                        for PID in dict:
                            if PID not in ["looking_for", "total_occurrences", "total_scenarios"]:

                                csv_ready_scenario_per_datatype_dict["scenario name"].append(PID)
                                csv_ready_scenario_per_datatype_dict["scenario count"].\
                                    append(dict[PID])

                                if str(dict["looking_for"]).replace(" ", "\n") not in total_query_count_per_looking_for_per_scenario:
                                    total_query_count_per_looking_for_per_scenario[
                                        str(dict["looking_for"]).replace(" ", "\n")] = {}

                                if PID not in total_query_count_per_looking_for_per_scenario[
                                        str(dict["looking_for"]).replace(" ", "\n")]:
                                    total_query_count_per_looking_for_per_scenario[
                                        str(dict["looking_for"]).replace(" ", "\n")][PID] = dict[PID]
                                else:
                                    total_query_count_per_looking_for_per_scenario[
                                        str(dict["looking_for"]).replace(" ", "\n")][PID] += dict[PID]

                                if dict["total_occurrences"] > 0:
                                    csv_ready_scenario_per_datatype_dict["scenario percentage"].\
                                        append(dict[PID] / dict["total_scenarios"])
                                else:
                                    csv_ready_scenario_per_datatype_dict["scenario percentage"].\
                                        append(0)

                                csv_ready_scenario_per_datatype_dict["timeframe"].\
                                    append(timeframe[:21].replace("_", "-\n"))
                                csv_ready_scenario_per_datatype_dict["datatype"].append(datatype.split("/")[0])
                                csv_ready_scenario_per_datatype_dict["type looking for"]. \
                                    append(str(dict["looking_for"]).replace(" ", "\n"))
                                csv_ready_scenario_per_datatype_dict["total occurrences"]. \
                                    append(dict["total_occurrences"])
                                csv_ready_scenario_per_datatype_dict["total scenarios"]. \
                                    append(dict["total_scenarios"])
                                csv_ready_scenario_per_datatype_dict["total queries"].\
                                    append(stat_info_scenarios_dict["total_queries"])




            # display the non-redundant scenario information per datatype and per timeframe in a heatmap
            for list_per_search in stat_info_scenarios_dict["found_scenarios"]["list_per_search"]:

                tmp_dict = {}
                tmp_dict["scenario name"] = []
                tmp_dict["timeframe"] = []
                tmp_dict["scenario percentage"] = []

                # add the total data
                for scenario in total_query_count_per_looking_for_per_scenario[
                        list_per_search["looking_for"].replace(" ", "\n")]:
                    tmp_dict["scenario name"].append(scenario)


                    tmp_dict["timeframe"].append("total")


                    if total_query_count_per_looking_for_per_scenario[
                            list_per_search["looking_for"].replace(" ", "\n")][scenario] > 0:
                        tmp_dict["scenario percentage"]. \
                            append(total_query_count_per_looking_for_per_scenario[
                            list_per_search["looking_for"].replace(" ", "\n")][scenario] /
                                   total_scenario_count_per_looking_for[list_per_search["looking_for"].replace(" ", "\n")])
                    else:
                        tmp_dict["scenario percentage"]. \
                            append(0)

                # add the timeframe data
                for i in range(len(csv_ready_scenario_per_datatype_dict["timeframe"])):
                    if list_per_search["looking_for"].replace(" ", "\n") == \
                            csv_ready_scenario_per_datatype_dict["type looking for"][i]:

                        tmp_dict["scenario name"].append(csv_ready_scenario_per_datatype_dict["scenario name"][i])
                        tmp_dict["timeframe"].append(csv_ready_scenario_per_datatype_dict["timeframe"][i])
                        tmp_dict["scenario percentage"].append(\
                            csv_ready_scenario_per_datatype_dict["scenario percentage"][i])


                print(datatype.split("/")[1])
                print(str(list_per_search["looking_for"]))
                print(tmp_dict)

                df = pd.DataFrame(tmp_dict)

                df = pd.pivot_table(data=df,
                                    index='scenario name',
                                    values='scenario percentage',
                                    columns='timeframe', sort=False)

                mask = (df == 0)
                fig, ax = plt.subplots(figsize=(12, 10))
                tmp = sns.heatmap(df, ax=ax, annot=True, vmin = 0,
                                  vmax = 1, mask=mask, cmap="Greens",
                                  linewidths=.5)
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
                                            replace("/", "\\") + ".pdf"

                tmp.get_figure().savefig(save_path)

                plt.close()


            for list_per_search in stat_info_scenarios_dict["found_scenarios"]["list_per_search"]:

                csv_ready_scenario_per_datatype_dict["timeframe"].append("total")

                csv_ready_scenario_per_datatype_dict["total occurrences"].append(
                    total_occurrences_count_per_looking_for[
                        list_per_search["looking_for"].replace(" ", "\n")]
                )
                csv_ready_scenario_per_datatype_dict["total scenarios"].append(
                    total_scenario_count_per_looking_for[
                        list_per_search["looking_for"].replace(" ", "\n")]
                )
                csv_ready_scenario_per_datatype_dict["total queries"].append(
                    total_query_count_per_looking_for[
                        list_per_search["looking_for"].replace(" ", "\n")]
                )

                csv_ready_scenario_per_datatype_dict["datatype"].append(None)
                csv_ready_scenario_per_datatype_dict["scenario percentage"].append(None)

                csv_ready_scenario_per_datatype_dict["type looking for"].append(
                    list_per_search["looking_for"].replace(" ", "\n"))

                csv_ready_scenario_per_datatype_dict["scenario name"].append(None)
                csv_ready_scenario_per_datatype_dict["scenario count"] .append(None)



            # plot the overll numbers of found scenarios per datatype and per timeframe
            #   for the total scenarios
            df = pd.DataFrame(csv_ready_scenario_per_datatype_dict)

            tmp = sns.catplot(x="timeframe", y="total scenarios", kind="bar",
                              palette="tab10", dodge=True, hue="type looking for",
                              data=df)

            plt.gcf().autofmt_xdate()

            save_path = "data/statistical_information/query_research/non_redundant/"+\
                datatype.split("/")[0] + "/scenarios/" + datatype.split("/")[1] +"_total_scenarios.pdf"

            tmp.savefig(save_path)

            plt.close()


            # plot the overll numbers of found scenarios per datatype and per timeframe
            #   for the total occurrences
            df = pd.DataFrame(csv_ready_scenario_per_datatype_dict)

            tmp = sns.catplot(x="timeframe", y="total occurrences", kind="bar",
                              palette="tab10", dodge=True, hue="type looking for",
                              data=df)

            plt.gcf().autofmt_xdate()

            save_path = "data/statistical_information/query_research/non_redundant/"+\
                datatype.split("/")[0] + "/scenarios/" + datatype.split("/")[1] +"_total_occurrences.pdf"

            tmp.savefig(save_path)

            plt.close()


            # plot the overll numbers of found scenarios per datatype and per timeframe
            #   for the total queries
            df = pd.DataFrame(csv_ready_scenario_per_datatype_dict)

            tmp = sns.catplot(x="timeframe", y="total queries", kind="bar",
                              palette="tab10", dodge=True, hue="type looking for",
                              data=df)

            plt.gcf().autofmt_xdate()

            save_path = "data/statistical_information/query_research/non_redundant/"+\
                datatype.split("/")[0] + "/scenarios/" + datatype.split("/")[1] +"_total_queries.pdf"

            tmp.savefig(save_path)

            plt.close()




# plot only the NON-redundant data
def plot_timeframe_metadata_distribution(timeframes, metadata):

    if metadata not in ["reference_metadata", "rank_metadata", "qualifier_metadata"]:
        raise Exception

    csv_ready_scenario_dict = {}
    csv_ready_scenario_dict["timeframe"] = []
    csv_ready_scenario_dict["datatype"] = []
    csv_ready_scenario_dict["type looking for"] = []
    csv_ready_scenario_dict["scenario name"] = []
    csv_ready_scenario_dict["scenario count"] = []
    csv_ready_scenario_dict["scenario percentage"] = []
    csv_ready_scenario_dict["total occurrences"] = []
    csv_ready_scenario_dict["total queries"] = []
    csv_ready_scenario_dict["total scenarios"] = []


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

                    csv_ready_scenario_dict["scenario name"].append(dict)

                    csv_ready_scenario_dict["scenario count"].\
                        append(stat_info_scenarios_dict["found_scenarios"][dict])

                    if stat_info_scenarios_dict["found_scenarios"]["total_occurrences"]>0:
                        csv_ready_scenario_dict["scenario percentage"].\
                            append(stat_info_scenarios_dict["found_scenarios"][dict]
                                   / stat_info_scenarios_dict["found_scenarios"]["total_scenarios"])
                    else:
                        csv_ready_scenario_dict["scenario percentage"].\
                            append(0)

                    csv_ready_scenario_dict["timeframe"].\
                        append(timeframe[:21].replace("_", "-\n"))
                    csv_ready_scenario_dict["datatype"].append(metadata)
                    csv_ready_scenario_dict["type looking for"]. \
                        append(str(stat_info_scenarios_dict["found_scenarios"]["looking_for"]).
                               replace(" ", "\n"))
                    csv_ready_scenario_dict["total occurrences"]. \
                        append(stat_info_scenarios_dict["found_scenarios"]["total_occurrences"])
                    csv_ready_scenario_dict["total scenarios"]. \
                        append(stat_info_scenarios_dict["found_scenarios"]["total_scenarios"])
                    csv_ready_scenario_dict["total queries"].\
                        append(stat_info_scenarios_dict["total_queries"])


    # add a 'overall' timeframe to display the total scenario information
    path_to_overall = "data/statistical_information/query_research/non_redundant/" +\
                            metadata + "/" + metadata + ".json"
    with open(path_to_overall, "r") as overall_data:
        overall_dict = json.load(overall_data)

        for dict in overall_dict["found_scenarios"]:

            if dict not in ["looking_for", "total_occurrences", "total_scenarios"]:

                csv_ready_scenario_dict["scenario name"].append(dict)

                csv_ready_scenario_dict["scenario count"]. \
                    append(overall_dict["found_scenarios"][dict])

                if overall_dict["found_scenarios"]["total_occurrences"] > 0:
                    csv_ready_scenario_dict["scenario percentage"]. \
                        append(overall_dict["found_scenarios"][dict]
                               / overall_dict["found_scenarios"]["total_scenarios"])
                else:
                    csv_ready_scenario_dict["scenario percentage"]. \
                        append(0)

                csv_ready_scenario_dict["timeframe"]. \
                    append("total")
                csv_ready_scenario_dict["datatype"].append(metadata)
                csv_ready_scenario_dict["type looking for"]. \
                    append(str(overall_dict["found_scenarios"]["looking_for"]).
                           replace(" ", "\n"))
                csv_ready_scenario_dict["total occurrences"]. \
                    append(overall_dict["found_scenarios"]["total_occurrences"])
                csv_ready_scenario_dict["total scenarios"]. \
                    append(overall_dict["found_scenarios"]["total_scenarios"])
                csv_ready_scenario_dict["total queries"]. \
                    append(overall_dict["total_queries"])


    tmp_dict = {}
    tmp_dict["scenario name"] = []
    tmp_dict["timeframe"] = []
    tmp_dict["scenario percentage"] = []

    for i in range(len(csv_ready_scenario_dict["timeframe"])):
        tmp_dict["scenario name"].append(csv_ready_scenario_dict["scenario name"][i])
        tmp_dict["timeframe"].append(csv_ready_scenario_dict["timeframe"][i])
        tmp_dict["scenario percentage"].append(\
            csv_ready_scenario_dict["scenario percentage"][i])

    df = pd.DataFrame(tmp_dict)

    df = pd.pivot_table(data=df,
                        index='scenario name',
                        values='scenario percentage',
                        columns='timeframe', sort=False)

    mask = (df == 0)
    fig, ax = plt.subplots(figsize=(12, 10)) # 16 10
    tmp = sns.heatmap(df, ax=ax, annot=True, vmin = 0, vmax = 1, mask=mask, cmap="YlGnBu",
                      linewidths=.5)
    tmp.figure.tight_layout()
    #tmp.figure.subplots_adjust(left=0.45, bottom=0.6)

    plt.gcf().autofmt_xdate()
    save_path = "data/statistical_information/query_research/non_redundant/" \
                                + metadata + "/scenarios/overall_scenarios.pdf"

    tmp.get_figure().savefig(save_path)

    plt.close()

    # plot the overll numbers of found scenarios per datatype and per timeframe
    #   for the total scenarios
    df = pd.DataFrame(csv_ready_scenario_dict)

    tmp = sns.catplot(x="timeframe", y="total scenarios", kind="bar",
                      palette="tab10", dodge=True, hue="type looking for",
                      data=df)

    plt.gcf().autofmt_xdate()

    save_path = "data/statistical_information/query_research/non_redundant/"+\
        metadata + "/scenarios/total_scenarios.pdf"

    tmp.savefig(save_path)

    plt.close()


    # plot the overll numbers of found scenarios per datatype and per timeframe
    #   for the total occurrences
    df = pd.DataFrame(csv_ready_scenario_dict)

    tmp = sns.catplot(x="timeframe", y="total occurrences", kind="bar",
                      palette="tab10", dodge=True, hue="type looking for",
                      data=df)

    plt.gcf().autofmt_xdate()

    save_path = "data/statistical_information/query_research/non_redundant/"+\
        metadata + "/scenarios/total_occurrences.pdf"

    tmp.savefig(save_path)

    plt.close()


    # plot the overll numbers of found scenarios per datatype and per timeframe
    #   for the total queries
    df = pd.DataFrame(csv_ready_scenario_dict)

    tmp = sns.catplot(x="timeframe", y="total queries", kind="bar",
                      palette="tab10", dodge=True, hue="type looking for",
                      data=df)

    plt.gcf().autofmt_xdate()

    save_path = "data/statistical_information/query_research/non_redundant/"+\
        metadata + "/scenarios/total_queries.pdf"

    tmp.savefig(save_path)

    plt.close()





# plot only the NON-redundant data
def plot_metadata_distribution_per_datatype_overall(timeframes, datatypes_list):

    for datatypes in datatypes_list:

        csv_ready_scenario_per_datatype_dict = {}
        csv_ready_scenario_per_datatype_dict["datatype"] = []
        csv_ready_scenario_per_datatype_dict["scenario_name"] = []
        csv_ready_scenario_per_datatype_dict["scenario_count"] = []
        csv_ready_scenario_per_datatype_dict["scenario_percentage"] = []

        for datatype in datatypes:

            tmp_data_scenario_dict = {}


            for timeframe in timeframes:

                # get the path to the location information of the timeframe scenario data per
                #   datatype
                information_path = "data/" + timeframe[:21] + "/" + timeframe[22:] + \
                                   "/" + datatype.split("/")[0] + \
                                   "/statistical_information/non_redundant/" + \
                                   datatype.split("/")[1] + ".json"

                # also, get the overall number of detected scenario per metadata tpye to calculate
                # the percentage of the datatypes on the overall numbers
                path_to_overall = "data/statistical_information/query_research/non_redundant/" + \
                                  datatype.split("/")[0] + "/" + datatype.split("/")[0] + ".json"


                with open(information_path, "r") as stat_info_scenarios_data:
                    stat_info_scenarios_dict = json.load(stat_info_scenarios_data)

                    with open(path_to_overall, "r") as overall_data:
                        overall_dict = json.load(overall_data)
                        overall_scenario_count = overall_dict["found_scenarios"]["total_scenarios"]

                        for dict in stat_info_scenarios_dict["found_scenarios"]["list_per_search"]:

                            for PID in dict:
                                if PID not in ["looking_for", "total_occurrences", "total_scenarios"]:


                                    if PID in tmp_data_scenario_dict:
                                        tmp_data_scenario_dict[PID] += dict[PID]
                                    else:
                                        tmp_data_scenario_dict[PID] = dict[PID]


            for scenario in tmp_data_scenario_dict:
                # ONLY wirte data to the graphic, if the datatype contains at leat one scenario
                if tmp_data_scenario_dict[scenario] > 0:
                    csv_ready_scenario_per_datatype_dict["scenario_name"].append(scenario)
                    csv_ready_scenario_per_datatype_dict["scenario_count"]. \
                        append(tmp_data_scenario_dict[scenario])
                    if tmp_data_scenario_dict[scenario] > 0:
                        csv_ready_scenario_per_datatype_dict["scenario_percentage"]. \
                            append(tmp_data_scenario_dict[scenario] / overall_scenario_count)
                    else:
                        csv_ready_scenario_per_datatype_dict["scenario_percentage"]. \
                            append(0)

                    csv_ready_scenario_per_datatype_dict["datatype"]. \
                        append(datatype.split("/")[1].replace("_+_", " +\n ").replace("_", " "))


        tmp_dict = {}
        tmp_dict["scenario name"] = []
        tmp_dict["datatype"] = []
        tmp_dict["scenario percentage"] = []

        for i in range(len(csv_ready_scenario_per_datatype_dict["datatype"])):


            tmp_dict["scenario name"].append(csv_ready_scenario_per_datatype_dict["scenario_name"][i])
            tmp_dict["datatype"].append(csv_ready_scenario_per_datatype_dict["datatype"][i])
            tmp_dict["scenario percentage"].append( \
                csv_ready_scenario_per_datatype_dict["scenario_percentage"][i])

        df = pd.DataFrame(tmp_dict)

        df = pd.pivot_table(data=df,
                            index='scenario name',
                            values='scenario percentage',
                            columns='datatype', sort=True)

        mask = (df == 0)
        fig, ax = plt.subplots(figsize=(12, 10))
        tmp = sns.heatmap(df, ax=ax, annot=True, vmin = 0,
                          vmax = 1, mask=mask, cmap="Purples",
                          linewidths=.5)
        tmp.figure.tight_layout()
        #tmp.figure.subplots_adjust(left=0.45, bottom=0.6)

        plt.gcf().autofmt_xdate()
        save_path = "data/statistical_information/query_research/non_redundant/" \
                    + datatype.split("/")[0] + "/scenarios/" + \
                    datatype.split("/")[0] + "_datatypes_overall.pdf"

        tmp.get_figure().savefig(save_path)

        plt.close()


