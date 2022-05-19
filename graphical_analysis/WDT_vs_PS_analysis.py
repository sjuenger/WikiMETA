import json
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

def plot_WDT_usages_vs_PD_usages():

    # gather the data
    information_path = "data/WDT_vs_PS_usage.json"

    csv_ready_dict = {}
    csv_ready_dict["timeframe"] = []
    csv_ready_dict["value"] = []
    csv_ready_dict["type"] = []

    with open(information_path, "r") as information_data:
        information_dict = json.load(information_data)

        # add the Total Queries
        csv_ready_dict["timeframe"].append("total")
        csv_ready_dict["value"].append(information_dict["TOTAL queries"])
        csv_ready_dict["type"].append("Total Queries")

        # add the Total Usages
        csv_ready_dict["timeframe"].append("total")
        csv_ready_dict["value"].append(information_dict["TOTAL usages"])
        csv_ready_dict["type"].append("Total Usages")

        # add the wdt Usages
        csv_ready_dict["timeframe"].append("total")
        csv_ready_dict["value"].append(information_dict["WDT usages"])
        csv_ready_dict["type"].append("wdt: Usages")

        # add the ps Usages
        csv_ready_dict["timeframe"].append("total")
        csv_ready_dict["value"].append(information_dict["PS usages"])
        csv_ready_dict["type"].append("ps: Usages")

        for timeframe in information_dict["timeframe data"]:

            # add the Total Queries
            csv_ready_dict["timeframe"].append(timeframe)
            csv_ready_dict["value"].append(information_dict["timeframe data"][timeframe]["TOTAL queries"])
            csv_ready_dict["type"].append("Total Queries")

            # add the Total Usages
            csv_ready_dict["timeframe"].append(timeframe)
            csv_ready_dict["value"].append(information_dict["timeframe data"][timeframe]["TOTAL usages"])
            csv_ready_dict["type"].append("Total Usages")

            # add the wdt Usages
            csv_ready_dict["timeframe"].append(timeframe)
            csv_ready_dict["value"].append(information_dict["timeframe data"][timeframe]["WDT usages"])
            csv_ready_dict["type"].append("wdt: Usages")

            # add the ps Usages
            csv_ready_dict["timeframe"].append(timeframe)
            csv_ready_dict["value"].append(information_dict["timeframe data"][timeframe]["PS usages"])
            csv_ready_dict["type"].append("ps: Usages")


    # plot the data
    df = pd.DataFrame(csv_ready_dict)
    tmp = sns.catplot(x="timeframe", y="value", kind="bar",
                      palette="rocket", hue="type",
                      dodge=True, data=df, ci=None)

    plt.gcf().autofmt_xdate()

    tmp.savefig("data/WDT_usages_vs_PS_usages.pdf")

    plt.close()