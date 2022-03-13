import os
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# plot only the NON-redundant data
def plot_additional_layer_information_about_scenarios_per_timeframe_for_OPTIONAL_MINUS_SUBSELECT_UNION(timeframes,
                                                                                                 metadata,
                                                                                                 scenario):

    csv_ready_scenario_dict = {}
    csv_ready_scenario_dict["timeframe"] = []
    csv_ready_scenario_dict["datatype"] = []
    csv_ready_scenario_dict["base_scenario"] = []
    csv_ready_scenario_dict["scenario_name"] = []
    csv_ready_scenario_dict["scenario_count"] = []
    csv_ready_scenario_dict["scenario_percentage"] = []
    csv_ready_scenario_dict["total_scenarios"] = []


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

                        csv_ready_scenario_dict["scenario_name"].append(ID)
                        csv_ready_scenario_dict["scenario_count"]. \
                            append(stat_info_scenarios_dict["metadata_found_in_scenarios"][ID])

                        total_occurrences = stat_info_scenarios_dict["total_found_metadata"]
                        csv_ready_scenario_dict["total_scenarios"].append(total_occurrences)

                        if total_occurrences > 0:
                            csv_ready_scenario_dict["scenario_percentage"]. \
                                append(int(stat_info_scenarios_dict["metadata_found_in_scenarios"][ID]) /
                                        total_occurrences)
                        else:
                            csv_ready_scenario_dict["scenario_percentage"]. \
                                append(0)

                        csv_ready_scenario_dict["timeframe"]. \
                            append(timeframe[:21])
                        csv_ready_scenario_dict["datatype"].append(metadata)

                        csv_ready_scenario_dict["base_scenario"].append(scenario)


    # plot the data in a heatmap
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
                        columns='timeframe', sort=False)

    mask = (df == 0)
    fig, ax = plt.subplots(figsize=(12, 10)) # 16 10
    tmp = sns.heatmap(df, ax=ax, annot=True, vmin = 0, vmax = 1, mask=mask, cmap="YlGnBu",
                      linewidths=.5)
    tmp.figure.tight_layout()
    #tmp.figure.subplots_adjust(left=0.45, bottom=0.6)

    plt.gcf().autofmt_xdate()
    save_path = "data/statistical_information/query_research/non_redundant/" \
                                + metadata + "/scenarios/additional_layer/" + scenario + ".png"

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


