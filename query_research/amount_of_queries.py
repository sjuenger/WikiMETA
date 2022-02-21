import json
import gzip
import csv

def save_total_of_queries_amount_per_timeframe(locations, list_of_metadata):

    for location in locations:

        with gzip.open("data/" + location + ".tsv.gz", "rt") as raw_timeframe_data:

            csv_data = csv.reader(raw_timeframe_data, delimiter="\t")

            # count the overall queries
            data_count = 0
            for row in csv_data:
                data_count += 1

            data_count_dict = {}
            data_count_dict["counted_queries"] = data_count
            data_count_dict["counted_metadata_queries"] = {}
            data_count_dict["counted_metadata_occurences"] = {}

            # count the queries with metadata
            for metadata in list_of_metadata:

                if metadata not in ["qualifier_metadata", "reference_metadata", "rank_metadata"]:
                    raise Exception

                path_to_timeframe_metadata_information = "data/" + location[:21] + "/" + location[22:] +\
                    "/statistical_information/redundant/" + metadata + "/" + metadata + ".json"

                with open(path_to_timeframe_metadata_information, "r") as metadata_information:
                    metadata_information_dict = json.load(metadata_information)
                    data_count_dict["counted_metadata_queries"][metadata] = \
                        metadata_information_dict["total_queries"]
                    data_count_dict["counted_metadata_occurences"][metadata] = \
                        metadata_information_dict["found_scenarios"]["total_occurrences"]

            # save the counted queries
            count_save_path = "data/" + location[:21]

            with open(count_save_path + "/counted_queries.json", "w") as save_data:
                json.dump(data_count_dict, save_data)


def save_total_of_queries_amount_overall(locations, list_of_metadata):

    data_count_dict = {}
    data_count_dict["counted_queries"] = 0
    data_count_dict["counted_metadata_queries"] = {}
    data_count_dict["counted_metadata_occurences"] = {}

    for location in locations:

        # look up the queries per timeframe
        count_save_path = "data/" + location[:21]

        with open(count_save_path + "/counted_queries.json", "r") as save_data:
            save_dict = json.load(save_data)

            data_count_dict["counted_queries"] += save_dict["counted_queries"]

            # count the queries with metadata
            for metadata in list_of_metadata:

                if metadata not in ["qualifier_metadata", "reference_metadata", "rank_metadata"]:
                    raise Exception

                if metadata not in data_count_dict["counted_metadata_queries"]:

                    data_count_dict["counted_metadata_queries"][metadata] = \
                        save_dict["counted_metadata_queries"][metadata]
                    data_count_dict["counted_metadata_occurences"][metadata] = \
                        save_dict["counted_metadata_occurences"][metadata]
                else:

                    data_count_dict["counted_metadata_queries"][metadata] += \
                        save_dict["counted_metadata_queries"][metadata]
                    data_count_dict["counted_metadata_occurences"][metadata] += \
                        save_dict["counted_metadata_occurences"][metadata]


    # save the counted queries
    count_save_path = "data"


    with open(count_save_path + "/counted_queries.json", "w") as result_data:
        json.dump(data_count_dict, result_data)