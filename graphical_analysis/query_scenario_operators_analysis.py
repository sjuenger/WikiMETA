import json
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# plot only the NON-redundant data
def plot_additional_operator_information_about_scenarios_per_timeframe_for_FILTER_PROPPATH(timeframes,
                                                                                                 metadata,
                                                                                                 scenario):
    if metadata not in ["reference_metadata", "rank_metadata", "qualifier_metadata"]:
        raise Exception
    if scenario not in ["filter", "prop_path"]:
        raise Exception

    csv_ready_scenario_dict = {}
    csv_ready_scenario_dict["timeframe"] = []
    csv_ready_scenario_dict["datatype"] = []
    csv_ready_scenario_dict["base_scenario"] = []
    csv_ready_scenario_dict["operator_name"] = []
    csv_ready_scenario_dict["operator_count"] = []
    csv_ready_scenario_dict["operator_percentage"] = []
    csv_ready_scenario_dict["total_operators"] = []


    for timeframe in timeframes:

        # get the path to the location information of the timeframe scenario data per
        #   datatype
        information_path = "data/" + timeframe[:21] + "/" + timeframe[22:] + \
                           "/" + metadata + \
                           "/scenarios/non_redundant/" + scenario + "_statistical_information.json"

        if os.path.exists(information_path):

            with open(information_path, "r") as stat_info_scenarios_data:
                stat_info_scenarios_dict = json.load(stat_info_scenarios_data)

                for operator in stat_info_scenarios_dict["found_operators_overall"]:

                    csv_ready_scenario_dict["operator_name"].append(operator)


                    csv_ready_scenario_dict["operator_count"]. \
                        append(stat_info_scenarios_dict["found_operators_overall"][operator])

                    total_occurrences = stat_info_scenarios_dict["total_found_operators"]

                    if total_occurrences > 0:
                        csv_ready_scenario_dict["operator_percentage"]. \
                            append(
                            int(stat_info_scenarios_dict["found_operators_overall"][operator]) /
                            total_occurrences)
                    else:
                        csv_ready_scenario_dict["operator_percentage"]. \
                            append(0)


                    csv_ready_scenario_dict["total_operators"].append(total_occurrences)
                    csv_ready_scenario_dict["timeframe"]. \
                        append(timeframe[:21].replace("_", "-\n"))
                    csv_ready_scenario_dict["datatype"].append(metadata)

                    csv_ready_scenario_dict["base_scenario"].append(scenario)


    # plot the data in a heatmap
    tmp_dict = {}
    tmp_dict["operator_name"] = []
    tmp_dict["timeframe"] = []
    tmp_dict["operator_percentage"] = []

    for i in range(len(csv_ready_scenario_dict["timeframe"])):
        tmp_dict["operator_name"].append(csv_ready_scenario_dict["operator_name"][i])
        tmp_dict["timeframe"].append(csv_ready_scenario_dict["timeframe"][i])
        tmp_dict["operator_percentage"].append(\
            csv_ready_scenario_dict["operator_percentage"][i])

    df = pd.DataFrame(tmp_dict)

    df = pd.pivot_table(data=df,
                        index='operator_name',
                        values='operator_percentage',
                        columns='timeframe', sort=False)

    mask = (df == 0)

    if scenario == "filter":
        fig, ax = plt.subplots(figsize=(8, 6)) # 16 10
    elif scenario == "prop_path":
        fig, ax = plt.subplots(figsize=(8, 5))

    tmp = sns.heatmap(df, ax=ax, annot=True, vmin = 0, vmax = 1, mask=mask, cmap="YlGnBu",
                      linewidths=.5)
    tmp.figure.tight_layout()
    tmp.figure.subplots_adjust(left=0.15, bottom=0.3)
    # set the yticks "upright" with 0, as opposed to sideways with 90
    plt.yticks(rotation=0)

    plt.gcf().autofmt_xdate()



    save_path = "data/statistical_information/query_research/non_redundant/" \
                                + metadata + "/scenarios/additional_layer/" + \
                                    scenario + "_operators.png"

    tmp.get_figure().savefig(save_path)

    plt.close()
