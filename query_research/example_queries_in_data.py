import json
import glob

def count_example_queries_in_queries(example_location, timeframe, metadata, datatypes, only_marked):

    redundant_example_queries_count = {}
    redundant_example_queries_count["total_queries"] = 0
    redundant_example_queries_count["example_queries"] = 0

    if metadata not in ["qualifier_metadata", "reference_metadata", "rank_metadata"]:
        error_message = "Not supported mode."
        raise Exception(error_message)

    # get one datatype out of the datatypes
    for datatype in datatypes:

        # all queries -> retrieve all .json files
        # in marked queries -> retrieve only marked files
        #
        # exclude the '...deletion_information.json' files --> [0-9] at the end

        if only_marked:
            # Retrieve only the definitely redundant files, ending with .json and starting with a 'x'
            files_json = glob.glob("data/" + timeframe[:21] + "/" +
                                    timeframe[22:] + "/" + metadata + "/"
                                    + datatype + "/x*[0-9].json")
        else:
            # Retrieve all files, ending with .json (also those, starting with a 'x')
            files_json = glob.glob("data/" + timeframe[:21] + "/" +
                                   timeframe[22:] + "/" + metadata + "/"
                                   + datatype + "/*[0-9].json")

        # check for example queries in the data

        # do not include the failed queries -> 206_failed.sparql or 205.sparql
        example_json_files = glob.glob("data/" + example_location + "/*[0-9].json")

        for file in files_json:

            with open(file, "r") as query_data:

                query_dict = json.load(query_data)

                redundant_example_queries_count["total_queries"] += 1

                for example_file in example_json_files:

                    with open(example_file, "r") as example_query_data:

                            example_query_dict = json.load(example_query_data)

                            if query_dict == example_query_dict:

                                redundant_example_queries_count["example_queries"] += 1

        information_path = "data/statistical_information/redundant_detection/" + \
            timeframe[:21] + "/" + datatype.split("/")[-2] + "/" + \
                  datatype.split("/")[-1]

        if only_marked:
            tmp_str = "_found_example_queries_in_marked_queries.json"
        else:
            tmp_str = "_found_example_queries_in_all_queries.json"

        with open(information_path + tmp_str, "w") as result_data:
            json.dump(redundant_example_queries_count, result_data)

