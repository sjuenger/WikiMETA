import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# plot only the NON-redundant data
def plot_additional_layer_information_about_scenarios_per_timeframe_for_OPTIONAL_MINUS_SUBSELECT_UNION_FILTER(timeframes,
                                                                                                 metadata,
                                                                                                 scenario):

    if metadata not in ["reference_metadata", "rank_metadata", "qualifier_metadata"]:
        raise Exception
    if scenario not in ["optional", "minus", "subselect", "union", "filter"]:
        raise Exception

    csv_ready_scenario_dict = {}
    csv_ready_scenario_dict["timeframe"] = []
    csv_ready_scenario_dict["datatype"] = []
    csv_ready_scenario_dict["base scenario"] = []
    csv_ready_scenario_dict["scenario name"] = []
    csv_ready_scenario_dict["scenario count"] = []
    csv_ready_scenario_dict["scenario percentage"] = []
    csv_ready_scenario_dict["total scenarios"] = []


    for timeframe in timeframes:

        # get the path to the location information of the timeframe scenario data per
        #   datatype
        information_path = "data/" + timeframe[:21] + "/" + timeframe[22:] + \
                           "/" + metadata + \
                           "/scenarios/non_redundant/" + scenario + "_statistical_information.json"

        if os.path.exists(information_path):

            with open(information_path, "r") as stat_info_scenarios_data:
                stat_info_scenarios_dict = json.load(stat_info_scenarios_data)

                for ID in stat_info_scenarios_dict["metadata_found_in_scenarios"]:

                    # to exclude the datatypes, e.g. 'total' or 'only_derived
                    if ID != "datatype":

                        csv_ready_scenario_dict["scenario name"].append(ID)
                        csv_ready_scenario_dict["scenario count"]. \
                            append(stat_info_scenarios_dict["metadata_found_in_scenarios"][ID])

                        total_occurrences = stat_info_scenarios_dict["total_found_metadata"]
                        csv_ready_scenario_dict["total scenarios"].append(total_occurrences)

                        if total_occurrences > 0:
                            csv_ready_scenario_dict["scenario percentage"]. \
                                append(int(stat_info_scenarios_dict["metadata_found_in_scenarios"][ID]) /
                                        total_occurrences)
                        else:
                            csv_ready_scenario_dict["scenario percentage"]. \
                                append(0)

                        csv_ready_scenario_dict["timeframe"]. \
                            append(timeframe[:21].replace("_", " - "))
                        csv_ready_scenario_dict["datatype"].append(metadata)

                        csv_ready_scenario_dict["base scenario"].append(scenario)

    # insert the total data
    overall_information_path = "data/statistical_information/query_research/" + "non_redundant" + \
                                 "/" + metadata + "/scenarios/additional_layer/" \
                                                  + scenario +"_statistical_information.json"

    with open(overall_information_path, "r") as overall_data:
        overall_dict = json.load(overall_data)

        for ID in overall_dict["metadata_found_in_scenarios"]:

            csv_ready_scenario_dict["timeframe"].append("total")
            csv_ready_scenario_dict["scenario name"].append(ID)
            csv_ready_scenario_dict["scenario count"]. \
                append(overall_dict["metadata_found_in_scenarios"][ID])

            total_occurrences = overall_dict["total_found_metadata"]
            csv_ready_scenario_dict["total scenarios"].append(total_occurrences)

            if total_occurrences > 0:
                csv_ready_scenario_dict["scenario percentage"]. \
                    append(int(overall_dict["metadata_found_in_scenarios"][ID]) /
                           total_occurrences)
            else:
                csv_ready_scenario_dict["scenario percentage"]. \
                    append(0)

            csv_ready_scenario_dict["datatype"].append(metadata)

            csv_ready_scenario_dict["base scenario"].append(scenario)


    # plot the data in a heatmap
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
    fig, ax = plt.subplots(figsize=(8, 10)) # 16 10
    tmp = sns.heatmap(df, ax=ax, annot=True, vmin = 0, vmax = 1, mask=mask, cmap="YlOrRd",
                      linewidths=.5)
    tmp.figure.tight_layout()
    #tmp.figure.subplots_adjust(left=0.2, bottom=-0.2)

    plt.gcf().autofmt_xdate()
    save_path = "data/statistical_information/query_research/non_redundant/" \
                                + metadata + "/scenarios/additional_layer/" + scenario + ".png"

    tmp.get_figure().savefig(save_path)

    plt.close()


# plot only the NON-redundant data
def plot_additional_additional_layer_information_about_scenarios_per_timeframe_for_SUBSELECT_UNION(timeframes,
                                                                                                 metadata,
                                                                                                 scenario):

    if metadata not in ["reference_metadata", "rank_metadata", "qualifier_metadata"]:
        raise Exception
    if scenario not in ["subselect", "union"]:
        raise Exception

    csv_ready_scenario_dict = {}
    csv_ready_scenario_dict["timeframe"] = []
    csv_ready_scenario_dict["datatype"] = []
    csv_ready_scenario_dict["base scenario"] = []
    csv_ready_scenario_dict["scenario name"] = []
    csv_ready_scenario_dict["scenario count"] = []
    csv_ready_scenario_dict["scenario percentage"] = []
    csv_ready_scenario_dict["total scenarios"] = []


    for timeframe in timeframes:

        # get the path to the location information of the timeframe scenario data per
        #   datatype
        information_path = "data/" + timeframe[:21] + "/" + timeframe[22:] + \
                           "/" + metadata + \
                           "/scenarios/non_redundant/" + scenario + "_statistical_information.json"

        if os.path.exists(information_path):

            with open(information_path, "r") as stat_info_scenarios_data:
                stat_info_scenarios_dict = json.load(stat_info_scenarios_data)

                if scenario == "union":
                    tmpID = "scenarios_found_in_second_level_subselect"
                elif scenario == "subselect":
                    tmpID = "scenarios_found_in_second_level_union"

                for ID in stat_info_scenarios_dict[tmpID]:

                    # to exclude the datatypes, e.g. 'total' or 'only_derived
                    if ID != "datatype":

                        csv_ready_scenario_dict["scenario name"].append(ID)


                        if scenario == "union":
                            csv_ready_scenario_dict["scenario count"]. \
                                append(stat_info_scenarios_dict["scenarios_found_in_second_level_subselect"][ID])

                            total_occurrences = stat_info_scenarios_dict["metadata_found_in_scenarios"]["subselect"]

                            if total_occurrences > 0:
                                csv_ready_scenario_dict["scenario percentage"]. \
                                    append(
                                    int(stat_info_scenarios_dict["scenarios_found_in_second_level_subselect"][ID]) /
                                    total_occurrences)
                            else:
                                csv_ready_scenario_dict["scenario percentage"]. \
                                    append(0)

                            csv_ready_scenario_dict["total scenarios"].append(total_occurrences)




                        elif scenario == "subselect":
                            csv_ready_scenario_dict["scenario count"]. \
                                append(stat_info_scenarios_dict["scenarios_found_in_second_level_union"][ID])

                            total_occurrences = stat_info_scenarios_dict["metadata_found_in_scenarios"]["union"]

                            if total_occurrences > 0:
                                csv_ready_scenario_dict["scenario percentage"]. \
                                    append(
                                    int(stat_info_scenarios_dict["scenarios_found_in_second_level_union"][ID]) /
                                    total_occurrences)
                            else:
                                csv_ready_scenario_dict["scenario percentage"]. \
                                    append(0)

                            csv_ready_scenario_dict["total scenarios"].append(total_occurrences)

                        csv_ready_scenario_dict["timeframe"]. \
                            append(timeframe[:21].replace("_", " - "))
                        csv_ready_scenario_dict["datatype"].append(metadata)

                        csv_ready_scenario_dict["base scenario"].append(scenario)



        # insert the total data
        overall_information_path = "data/statistical_information/query_research/" + "non_redundant" + \
                                   "/" + metadata + "/scenarios/additional_layer/" \
                                   + scenario + "_statistical_information.json"

        with open(overall_information_path, "r") as overall_data:
            overall_dict = json.load(overall_data)

            if scenario == "union":
                tmpID = "scenarios_found_in_second_level_subselect"
            elif scenario == "subselect":
                tmpID = "scenarios_found_in_second_level_union"

            for ID in overall_dict[tmpID]:

                csv_ready_scenario_dict["scenario name"].append(ID)

                if scenario == "union":
                    csv_ready_scenario_dict["scenario count"]. \
                        append(overall_dict["scenarios_found_in_second_level_subselect"][ID])

                    total_occurrences = overall_dict["metadata_found_in_scenarios"]["subselect"]

                    if total_occurrences > 0:
                        csv_ready_scenario_dict["scenario percentage"]. \
                            append(
                            int(overall_dict["scenarios_found_in_second_level_subselect"][ID]) /
                            total_occurrences)
                    else:
                        csv_ready_scenario_dict["scenario percentage"]. \
                            append(0)




                elif scenario == "subselect":
                    csv_ready_scenario_dict["scenario count"]. \
                        append(overall_dict["scenarios_found_in_second_level_union"][ID])

                    total_occurrences = overall_dict["metadata_found_in_scenarios"]["union"]

                    if total_occurrences > 0:
                        csv_ready_scenario_dict["scenario percentage"]. \
                            append(
                            int(overall_dict["scenarios_found_in_second_level_union"][ID]) /
                            total_occurrences)
                    else:
                        csv_ready_scenario_dict["scenario percentage"]. \
                            append(0)

                csv_ready_scenario_dict["total scenarios"].append(total_occurrences)
                csv_ready_scenario_dict["timeframe"]. \
                    append("total")
                csv_ready_scenario_dict["datatype"].append(metadata)

                csv_ready_scenario_dict["base scenario"].append(scenario)


    # plot the data in a heatmap
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
    fig, ax = plt.subplots(figsize=(8, 10)) # 16 10
    tmp = sns.heatmap(df, ax=ax, annot=True, vmin = 0, vmax = 1, mask=mask, cmap="OrRd",
                      linewidths=.5)
    tmp.figure.tight_layout()
    #tmp.figure.subplots_adjust(left=0.45, bottom=0.6)

    plt.gcf().autofmt_xdate()

    if scenario == "union":
        tmpFileName = "_additional_subselect"
    elif scenario == "subselect":
        tmpFileName = "_additional_union"

    save_path = "data/statistical_information/query_research/non_redundant/" \
                                + metadata + "/scenarios/additional_layer/" + \
                                    scenario + tmpFileName + ".png"

    tmp.get_figure().savefig(save_path)

    plt.close()



# plot only the NON-redundant data
def plot_additional_layer_information_about_scenarios_per_datatype_for_OPTIONAL_MINUS_SUBSELECT_UNION_FILTER(timeframes,
                                                                                                 metadata,
                                                                                                 scenario):

    if metadata not in ["reference_metadata", "rank_metadata", "qualifier_metadata"]:
        raise Exception
    if scenario not in ["optional", "minus", "subselect", "union", "filter"]:
        raise Exception

    csv_ready_scenario_dict = {}
    csv_ready_scenario_dict["datatype"] = []
    csv_ready_scenario_dict["base scenario"] = []
    csv_ready_scenario_dict["scenario name"] = []
    csv_ready_scenario_dict["scenario count"] = []
    csv_ready_scenario_dict["scenario percentage"] = []
    csv_ready_scenario_dict["total scenarios"] = []


    # insert the total data
    overall_information_path = "data/statistical_information/query_research/" + "non_redundant" + \
                                 "/" + metadata + "/scenarios/additional_layer/" \
                                                  + scenario +"_statistical_information.json"

    with open(overall_information_path, "r") as overall_data:
        overall_dict = json.load(overall_data)

        for datatype in overall_dict["metadata_per_datatype_found_in_scenarios"]:

            for ID in overall_dict["metadata_per_datatype_found_in_scenarios"][datatype]:

                csv_ready_scenario_dict["scenario name"].append(ID)
                csv_ready_scenario_dict["scenario count"]. \
                    append(overall_dict["metadata_per_datatype_found_in_scenarios"][datatype][ID])

                total_occurrences = overall_dict["total_found_metadata"]
                csv_ready_scenario_dict["total scenarios"].append(total_occurrences)

                if total_occurrences > 0:
                    csv_ready_scenario_dict["scenario percentage"]. \
                        append(int(overall_dict["metadata_per_datatype_found_in_scenarios"][datatype][ID]) /
                               total_occurrences)
                else:
                    csv_ready_scenario_dict["scenario percentage"]. \
                        append(0)

                csv_ready_scenario_dict["datatype"].append(datatype.split("/")[1].
                                                           replace("_+_", " +\n").
                                                           replace("e_", "e\n"))
                csv_ready_scenario_dict["base scenario"].append(scenario)


    # plot the data in a heatmap
    tmp_dict = {}
    tmp_dict["scenario name"] = []
    tmp_dict["datatype"] = []
    tmp_dict["scenario percentage"] = []

    for i in range(len(csv_ready_scenario_dict["datatype"])):
        tmp_dict["scenario name"].append(csv_ready_scenario_dict["scenario name"][i])
        tmp_dict["datatype"].append(csv_ready_scenario_dict["datatype"][i])
        tmp_dict["scenario percentage"].append(\
            csv_ready_scenario_dict["scenario percentage"][i])

    df = pd.DataFrame(tmp_dict)

    df = pd.pivot_table(data=df,
                        index='scenario name',
                        values='scenario percentage',
                        columns='datatype', sort=False)

    mask = (df == 0)
    fig, ax = plt.subplots(figsize=(8, 10)) # 16 10
    tmp = sns.heatmap(df, ax=ax, annot=True, vmin = 0, vmax = 1, mask=mask, cmap="BuPu",
                      linewidths=.5)
    tmp.figure.tight_layout()
    #tmp.figure.subplots_adjust(left=0.2, bottom=-0.2)

    plt.gcf().autofmt_xdate()
    save_path = "data/statistical_information/query_research/non_redundant/" \
                                + metadata + "/scenarios/additional_layer/" + scenario + "_per_datatype.png"

    tmp.get_figure().savefig(save_path)

    plt.close()



# plot only the NON-redundant data
def plot_additional_additional_layer_information_about_scenarios_per_datatype_for_SUBSELECT_UNION(timeframes,
                                                                                                 metadata,
                                                                                                 scenario):

    if metadata not in ["reference_metadata", "rank_metadata", "qualifier_metadata"]:
        raise Exception
    if scenario not in ["subselect", "union"]:
        raise Exception

    csv_ready_scenario_dict = {}
    csv_ready_scenario_dict["datatype"] = []
    csv_ready_scenario_dict["base scenario"] = []
    csv_ready_scenario_dict["scenario name"] = []
    csv_ready_scenario_dict["scenario count"] = []
    csv_ready_scenario_dict["scenario percentage"] = []
    csv_ready_scenario_dict["total scenarios"] = []


    # insert the total data
    overall_information_path = "data/statistical_information/query_research/" + "non_redundant" + \
                               "/" + metadata + "/scenarios/additional_layer/" \
                               + scenario + "_statistical_information.json"

    with open(overall_information_path, "r") as overall_data:
        overall_dict = json.load(overall_data)

        if scenario == "union":
            tmpID = "scenarios_per_datatype_found_in_second_level_subselect"
        elif scenario == "subselect":
            tmpID = "scenarios_per_datatype_found_in_second_level_union"

        for datatype in overall_dict[tmpID]:
            for ID in overall_dict[tmpID][datatype]:

                csv_ready_scenario_dict["scenario name"].append(ID)

                if scenario == "union":
                    csv_ready_scenario_dict["scenario count"]. \
                        append(overall_dict["scenarios_per_datatype_found_in_second_level_subselect"]\
                                                   [datatype][ID])

                    total_occurrences = overall_dict["metadata_found_in_scenarios"]["subselect"]

                    if total_occurrences > 0:
                        csv_ready_scenario_dict["scenario percentage"]. \
                            append(
                            int(overall_dict["scenarios_per_datatype_found_in_second_level_subselect"]\
                                [datatype][ID]) / total_occurrences)
                    else:
                        csv_ready_scenario_dict["scenario percentage"]. \
                            append(0)

                    csv_ready_scenario_dict["total scenarios"].append(total_occurrences)




                elif scenario == "subselect":
                    csv_ready_scenario_dict["scenario count"]. \
                        append(overall_dict["scenarios_per_datatype_found_in_second_level_union"]\
                                                   [datatype][ID])

                    total_occurrences = overall_dict["metadata_found_in_scenarios"]["union"]

                    if total_occurrences > 0:
                        csv_ready_scenario_dict["scenario percentage"]. \
                            append(
                            int(overall_dict["scenarios_per_datatype_found_in_second_level_union"]\
                                [datatype][ID]) / total_occurrences)
                    else:
                        csv_ready_scenario_dict["scenario percentage"]. \
                            append(0)

                    csv_ready_scenario_dict["total scenarios"].append(total_occurrences)

                csv_ready_scenario_dict["datatype"].append(datatype.split("/")[1].
                                                           replace("_+_", " +\n").
                                                           replace("e_", "e\n"))

                csv_ready_scenario_dict["base scenario"].append(scenario)


    # plot the data in a heatmap
    tmp_dict = {}
    tmp_dict["scenario name"] = []
    tmp_dict["datatype"] = []
    tmp_dict["scenario percentage"] = []

    for i in range(len(csv_ready_scenario_dict["datatype"])):
        tmp_dict["scenario name"].append(csv_ready_scenario_dict["scenario name"][i])
        tmp_dict["datatype"].append(csv_ready_scenario_dict["datatype"][i])
        tmp_dict["scenario percentage"].append(\
            csv_ready_scenario_dict["scenario percentage"][i])

    df = pd.DataFrame(tmp_dict)

    df = pd.pivot_table(data=df,
                        index='scenario name',
                        values='scenario percentage',
                        columns='datatype', sort=False)

    mask = (df == 0)
    fig, ax = plt.subplots(figsize=(8, 10)) # 16 10
    tmp = sns.heatmap(df, ax=ax, annot=True, vmin = 0, vmax = 1, mask=mask, cmap="PuBu",
                      linewidths=.5)
    tmp.figure.tight_layout()
    #tmp.figure.subplots_adjust(left=0.45, bottom=0.6)

    plt.gcf().autofmt_xdate()

    if scenario == "union":
        tmpFileName = "_additional_subselect"
    elif scenario == "subselect":
        tmpFileName = "_additional_union"

    save_path = "data/statistical_information/query_research/non_redundant/" \
                                + metadata + "/scenarios/additional_layer/" + \
                                    scenario + tmpFileName + "_per_datatype.png"

    tmp.get_figure().savefig(save_path)

    plt.close()






# plot only the NON-redundant data
def plot_additional_layer_information_about_scenarios(timeframes, metadata):
    return


def intTryParse(value):
    try:
        return int(value), True
    except ValueError:
        return value, False


