# this method is used to count the best / normal / deprecated ranks, used in the queries

import glob
import json

def count_ranks_in(location, mode, DATATYPES, redundant_mode):

    if mode not in ["rank_metadata"]:
        error_message = "Not supported metadata mode: ", mode
        raise Exception(error_message)

    if redundant_mode not in ["redundant", "non_redundant"]:
        error_message = "Not supported redundancy mode: ", redundant_mode
        raise Exception(error_message)

    result_dict = {}
    result_dict["ranks"] = {}
    result_dict["ranks"]["best_rank"] = 0
    result_dict["ranks"]["normal_rank"] = 0
    result_dict["ranks"]["deprecated_rank"] = 0
    result_dict["total_ranks"] = 0

    # get the path to the folder, where the json file about the gathered statistical information
    # .. is stored
    path_to_stat_information = "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" + \
                               redundant_mode + "/" + mode

    for data_type in DATATYPES:
        # TODO: check, if the property dictionary already exists
        # if
        # TODO: change to only the files, that do contain a property
        # if redundant_mode == "redundant" -> retrieve all .json files
        # if redundant_mode == "non_redundant" -> retrieve only non-marked files
        #
        # in any case, exclude the '...deletion_information.json' files --> [0-9] at the end
        if redundant_mode == "redundant":
            # Retrieve all files, ending with .json (also those, starting with a 'x')
            files_json = glob.glob("data/" + location[:21] + "/" +
                                   location[22:] + "/" + data_type + "/*[0-9].json")
        else:
            # Retrieve only the non-redundant files, ending with .json (not those, starting with a 'x')
            # .. only those, starting with a digit
            files_json = glob.glob("data/" + location[:21] + "/" +
                                   location[22:] + "/" + data_type + "/[0-9]*[0-9].json")


        for query_file in files_json:
            with open(query_file, "r") as query:
                query_json = json.load(query)

                # just iterate through SELECT queries
                # TODO: What about the DESCRIBE / ... queries?
                # Count them by hand?
                if query_json["queryType"] == 'SELECT':

                    where_part = query_json["where"]

                    best_ranks_no = str(where_part).count("http://wikiba.se/ontology#BestRank")
                    deprecated_ranks_no = str(where_part).count("http://wikiba.se/ontology#DeprecatedRank")
                    normal_ranks_no = str(where_part).count("http://wikiba.se/ontology#NormaltRank")

                    result_dict["ranks"]["best_rank"] += best_ranks_no
                    result_dict["ranks"]["normal_rank"] += normal_ranks_no
                    result_dict["ranks"]["deprecated_rank"] += deprecated_ranks_no

                    result_dict["total_ranks"] += best_ranks_no + normal_ranks_no + deprecated_ranks_no


    with open(path_to_stat_information + "/ranks_counted.json", "w") as result_data:
        json.dump(result_dict, result_data)

    return
