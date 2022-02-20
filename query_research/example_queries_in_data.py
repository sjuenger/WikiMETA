import json
import glob
import re

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
                                    timeframe[22:] + "/" + datatype + "/x*[0-9].json")
        else:
            # Retrieve all files, ending with .json (also those, starting with a 'x')
            files_json = glob.glob("data/" + timeframe[:21] + "/" +
                                   timeframe[22:] + "/" + datatype + "/*[0-9].json")

        # check for example queries in the data

        # create a list of all the Wikidata SPARQL Queries (345  queries)
        # do not include the failed queries -> 206_failed.sparql or 205.sparql

        example_queries = []
        example_json_files = glob.glob("data/" + example_location + "/*[0-9].json")
        for example_file in example_json_files:
            with open(example_file) as example_query_data:
                example_query_dict = json.load(example_query_data)
                example_queries.append(example_query_dict)

        for file in files_json:
            with open(file, "r") as query_data:
                query_dict = json.load(query_data)
                redundant_example_queries_count["total_queries"] += 1

                # only look at the SELECT queries, because the Wikidata Example Queries are also
                # .. only SELECT queries

                if query_dict["queryType"] == "SELECT":

                    # check for all the example queries
                    for example_query_dict in example_queries:

                        if "where" in example_query_dict:

                            query_dict_str = re.sub(r"\"value\": \"var\d+\"", "\"value\": \"var\"",
                                                    json.dumps(query_dict))
                            example_query_dict_str = re.sub(r"\"value\": \"var\d+\"", "\"value\": \"var\"",
                                                    json.dumps(example_query_dict))

                            query_dict_var = json.loads(query_dict_str)
                            example_query_dict_var = json.loads(example_query_dict_str)

                            query_dict_where = query_dict_var["where"]
                            example_query_dict_where = example_query_dict_var["where"]

                            if query_dict_where == example_query_dict_where:
                                print(query_dict_where)
                                print(timeframe)
                                print(metadata)
                                print(datatype)
                                print("\n")
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


def summarize_scenario_data_from_metadata_per_datatype_and_overall(timeframes, datatypes, only_marked):

    result_dict = {}
    result_dict["datatypes"] = []
    result_dict["total_queries"] = 0
    result_dict["example_queries"] = 0


    for datatype in datatypes:

        datatype_dict = {}
        datatype_dict["name"] = datatype.split("/")[-2]
        datatype_dict["total_queries"] = 0
        datatype_dict["example_queries"] = 0

        for timeframe in timeframes:

            # path to the data about the datatypes from each metadata
            information_path = "data/statistical_information/redundant_detection/" + \
                               timeframe[:21] + "/" + datatype.split("/")[-2] + "/" + \
                               datatype.split("/")[-1]

            if only_marked:
                tmp_str = "_found_example_queries_in_marked_queries.json"
            else:
                tmp_str = "_found_example_queries_in_all_queries.json"

            with open(information_path + tmp_str) as information_data:
                information_dict = json.load(information_data)

                datatype_dict["total_queries"] += information_dict["total_queries"]
                datatype_dict["example_queries"] += information_dict["example_queries"]

                result_dict["total_queries"] += information_dict["total_queries"]
                result_dict["example_queries"] += information_dict["example_queries"]


        result_dict["datatypes"].append(datatype_dict)

    # path to save the information per metadata and per datatype
    result_path_datatype = "data/statistical_information/redundant_detection/" +\
                            datatype.split("/")[-2] + "/" + "found_example_queries.json"
    with open(result_path_datatype, "w") as result_data:
        json.dump(result_dict, result_data)




