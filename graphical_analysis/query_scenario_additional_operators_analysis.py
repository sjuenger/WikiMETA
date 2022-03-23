import os
import json
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# plot only the NON-redundant data
def plot_additional_second_level_operator_information_about_scenarios_per_timeframe_for_OPTIONAL(timeframes,
                                                                                                 metadata,
                                                                                                 scenario):
    if metadata not in ["reference_metadata", "rank_metadata", "qualifier_metadata"]:
        raise Exception
    if scenario not in ["optional"]:
        raise Exception

    csv_ready_scenario_dict = {}
    csv_ready_scenario_dict["timeframe"] = []
    csv_ready_scenario_dict["datatype"] = []
    csv_ready_scenario_dict["base scenario"] = []
    csv_ready_scenario_dict["operator name"] = []
    csv_ready_scenario_dict["operator count"] = []
    csv_ready_scenario_dict["operator percentage"] = []
    csv_ready_scenario_dict["total operators"] = []

    for timeframe in timeframes:

        # get the path to the location information of the timeframe scenario data per
        #   datatype
        information_path = "data/" + timeframe[:21] + "/" + timeframe[22:] + \
                           "/" + metadata + \
                           "/scenarios/non_redundant/" + scenario + "_statistical_information.json"

        if os.path.exists(information_path):

            with open(information_path, "r") as stat_info_scenarios_data:
                stat_info_scenarios_dict = json.load(stat_info_scenarios_data)

                for operator in stat_info_scenarios_dict["in_found_prop_path_found_operators_overall"]:

                    csv_ready_scenario_dict["operator name"].append(operator)


                    csv_ready_scenario_dict["operator count"]. \
                        append(stat_info_scenarios_dict["in_found_prop_path_found_operators_overall"][operator])

                    total_occurrences = stat_info_scenarios_dict["in_found_prop_path_total_found_operators"]

                    if total_occurrences > 0:
                        csv_ready_scenario_dict["operator percentage"]. \
                            append(
                            int(stat_info_scenarios_dict["in_found_prop_path_found_operators_overall"][operator]) /
                            total_occurrences)
                    else:
                        csv_ready_scenario_dict["operator percentage"]. \
                            append(0)


                    csv_ready_scenario_dict["total operators"].append(total_occurrences)
                    csv_ready_scenario_dict["timeframe"]. \
                        append(timeframe[:21].replace("_", "-\n"))
                    csv_ready_scenario_dict["datatype"].append(metadata)

                    csv_ready_scenario_dict["base scenario"].append(scenario)


    # insert the total data
    overall_information_path = "data/statistical_information/query_research/" + "non_redundant" + \
                                 "/" + metadata + "/scenarios/additional_layer/" \
                                                  + scenario +"_statistical_information.json"

    with open(overall_information_path, "r") as overall_data:
        overall_dict = json.load(overall_data)

        for operator in overall_dict["in_found_prop_path_found_operators_overall"]:

            csv_ready_scenario_dict["operator name"].append(operator)

            csv_ready_scenario_dict["operator count"]. \
                append(overall_dict["in_found_prop_path_found_operators_overall"][operator])

            total_occurrences = overall_dict["in_found_prop_path_total_found_operators"]

            if total_occurrences > 0:
                csv_ready_scenario_dict["operator percentage"]. \
                    append(
                    int(overall_dict["in_found_prop_path_found_operators_overall"][operator]) /
                    total_occurrences)
            else:
                csv_ready_scenario_dict["operator percentage"]. \
                    append(0)

            csv_ready_scenario_dict["total operators"].append(total_occurrences)
            csv_ready_scenario_dict["timeframe"]. \
                append("total")
            csv_ready_scenario_dict["datatype"].append(metadata)

            csv_ready_scenario_dict["base scenario"].append(scenario)



    # plot the data in a heatmap
    tmp_dict = {}
    tmp_dict["operator name"] = []
    tmp_dict["timeframe"] = []
    tmp_dict["operator percentage"] = []

    for i in range(len(csv_ready_scenario_dict["timeframe"])):
        tmp_dict["operator name"].append(csv_ready_scenario_dict["operator name"][i])
        tmp_dict["timeframe"].append(csv_ready_scenario_dict["timeframe"][i])
        tmp_dict["operator percentage"].append(\
            csv_ready_scenario_dict["operator percentage"][i])

    df = pd.DataFrame(tmp_dict)

    df = pd.pivot_table(data=df,
                        index='operator name',
                        values='operator percentage',
                        columns='timeframe', sort=True)

    mask = (df == 0)

    fig, ax = plt.subplots(figsize=(9, 5)) # 16 10

    tmp = sns.heatmap(df, ax=ax, annot=True, vmin = 0, vmax = 1, mask=mask, cmap="Reds",
                      linewidths=.5)
    tmp.figure.tight_layout()
    tmp.figure.subplots_adjust(left=0.15, bottom=0.3)
    # set the yticks "upright" with 0, as opposed to sideways with 90
    plt.yticks(rotation=0)

    plt.gcf().autofmt_xdate()



    save_path = "data/statistical_information/query_research/non_redundant/" \
                                + metadata + "/scenarios/additional_layer/" + \
                                    scenario + "_prop_path_operators.png"

    tmp.get_figure().savefig(save_path)

    plt.close()


# plot only the NON-redundant data
def plot_additional_second_level_operator_information_about_scenarios_per_datatype_for_OPTIONAL(timeframes,
                                                                                                 metadata,
                                                                                                 scenario):
    if metadata not in ["reference_metadata", "rank_metadata", "qualifier_metadata"]:
        raise Exception
    if scenario not in ["optional"]:
        raise Exception

    csv_ready_scenario_dict = {}
    csv_ready_scenario_dict["datatype"] = []
    csv_ready_scenario_dict["base scenario"] = []
    csv_ready_scenario_dict["operator name"] = []
    csv_ready_scenario_dict["operator count"] = []
    csv_ready_scenario_dict["operator percentage"] = []
    csv_ready_scenario_dict["total operators"] = []


    # insert the total data
    overall_information_path = "data/statistical_information/query_research/" + "non_redundant" + \
                                 "/" + metadata + "/scenarios/additional_layer/" \
                                                  + scenario +"_statistical_information.json"

    with open(overall_information_path, "r") as overall_data:
        overall_dict = json.load(overall_data)

        for datatype in overall_dict["in_found_prop_path_found_operators_per_datatype"]:
            for operator in overall_dict["in_found_prop_path_found_operators_per_datatype"][datatype]:
                csv_ready_scenario_dict["operator name"].append(operator)

                csv_ready_scenario_dict["operator count"]. \
                    append(overall_dict["in_found_prop_path_found_operators_per_datatype"][datatype][operator])

                total_occurrences = overall_dict["in_found_prop_path_total_found_operators"]

                if total_occurrences > 0:
                    csv_ready_scenario_dict["operator percentage"]. \
                        append(
                        int(overall_dict["in_found_prop_path_found_operators_per_datatype"][datatype][operator]) /
                        total_occurrences)
                else:
                    csv_ready_scenario_dict["operator percentage"]. \
                        append(0)

                csv_ready_scenario_dict["total operators"].append(total_occurrences)

                # e.g. reference_metadata/only_derived -> only_derived
                csv_ready_scenario_dict["datatype"].append(datatype.split("/")[1].
                                                           replace("_+_", " +\n").
                                                           replace("e_", "e\n"))

                csv_ready_scenario_dict["base scenario"].append(scenario)



    # plot the data in a heatmap
    tmp_dict = {}
    tmp_dict["operator name"] = []
    tmp_dict["datatype"] = []
    tmp_dict["operator percentage"] = []

    for i in range(len(csv_ready_scenario_dict["datatype"])):
        tmp_dict["operator name"].append(csv_ready_scenario_dict["operator name"][i])
        tmp_dict["datatype"].append(csv_ready_scenario_dict["datatype"][i])
        tmp_dict["operator percentage"].append(\
            csv_ready_scenario_dict["operator percentage"][i])

    df = pd.DataFrame(tmp_dict)

    df = pd.pivot_table(data=df,
                        index='operator name',
                        values='operator percentage',
                        columns='datatype', sort=True)

    mask = (df == 0)
    fig, ax = plt.subplots(figsize=(6, 5))

    tmp = sns.heatmap(df, ax=ax, annot=True, vmin = 0, vmax = 1, mask=mask, cmap="Greys",
                      linewidths=.5)
    tmp.figure.subplots_adjust()
    tmp.figure.tight_layout()
    tmp.figure.subplots_adjust(left=0.15, bottom=0)
    # set the yticks "upright" with 0, as opposed to sideways with 90
    plt.yticks(rotation=0)

    plt.gcf().autofmt_xdate()



    save_path = "data/statistical_information/query_research/non_redundant/" \
                                + metadata + "/scenarios/additional_layer/" + \
                                    scenario + "_prop_path_operators_per_datatype.png"

    tmp.get_figure().savefig(save_path)

    plt.close()

