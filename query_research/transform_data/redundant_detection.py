import glob
import json
import os
import os.path
from datetime import datetime, timedelta


# detection of redundant queries
# f.e. if a user executes a query multiples times
# -> this still counts as only one query (in theory, this has to be done with the other queries, too)
#
# deleted queries will be marked with an 'x'... in front of their filename

def delete_redundant_queries(timeframe, location):
    # Retrieve all files, ending with .json
    files_json = glob.glob("data/" + timeframe[:21] + "/" +
                           timeframe[22:] + "/" + location + "/*.json")

    debug_information = {}

    query_count = 0
    queries_marked = 0

    sorted_query_files = sorted(files_json, key = get_query_file_number)

    # sort the files in a numeric order (to be sure, they are also sorted by time)
    for query_file in sorted_query_files:

        # do not use the deletion_information_json
        # if it is -> jump to the next file
        if "_deletion_information" not in query_file:

            # for Debugging -> if the script is run on an already marked dataset
            #if "x" in query_file:
            #    raise Exception


            # in case the query was marked before -> add an 'x' to the file name, so the program can still find it
            if not os.path.isfile(query_file):
                # data/2017-06-12_2017-07-09/organic/reference_metadata/derived_+_reference_property/x 104501 2017-06-26
                # 19:17:56.json -> if 'x' ?
                #
                # data/2017-06-12_2017-07-09/organic/reference_metadata/derived_+_reference_property/104501 2017-06-26 19:17:56.json
                # ->
                # data/2017-06-12_2017-07-09/organic/reference_metadata/derived_+_reference_property/x 104501 2017-06-26 19:17:56.json
                tmp_string_1 = "/x " + query_file.split("/")[-1]
                tmp_string_2 = query_file.split("/")
                tmp_string_2.pop()
                query_file = "/".join(tmp_string_2) + tmp_string_1
                print("Already marked query one: " + query_file)

            query_count += 1

            with open(query_file, "rt") as json_data:
                query_one = json.load(json_data)

                # only look at the SELECT queries

                if query_one["queryType"] == "SELECT":

                    # do not ignore files, which were marked as deleted beforehand
                    # because a chain of queries, e.g. 1 -> 2 -> 3 -> 4
                    # could be transformed to 1 -> x2 -> 3 -> x4
                    # e.g. when all queries are 24h apart
                    # instead, we want 1 -> x2 -> x3 -> x4


                    for test_query_file in sorted_query_files:

                        # in case, also this query was already marked in the dataset -> skip it. No need to mark it again
                        #
                        #  and
                        # do not compare the query with itself and also not of the "...._deletion_information"
                        # and
                        # if the query in the "sorted_query_files" was marked before, it can not be found in the path
                        # .. in this case, also ignore it. It is already marked
                        if ("_deletion_information" not in test_query_file) and test_query_file != query_file\
                                and (not test_query_file.split("/")[-1].startswith("x")\
                                and os.path.isfile(test_query_file)):

                            # look only at the files, which are max. 25hours apart

                            # to also include the marked as redundant files
                            if query_file.split("/")[-1].startswith("x"):
                                # data/.../x 146 2017-06-12 02:13:12.json -> datetime( 2017-06-12 02:13:12 )
                                query_one_datetime = datetime.strptime(str(" ".join(query_file.split(" ")[2:]).split(".")[0]),
                                                                    "%Y-%m-%d %H:%M:%S")

                            else:
                                # data/.../146 2017-06-12 02:13:12.json -> datetime( 2017-06-12 02:13:12 )
                                query_one_datetime = datetime.strptime(str(" ".join(query_file.split(" ")[1:]).split(".")[0]),
                                                                    "%Y-%m-%d %H:%M:%S")
                            if test_query_file.split("/")[-1].startswith("x"):
                                query_two_datetime = datetime.strptime(
                                    str(" ".join(test_query_file.split(" ")[2:]).split(".")[0]), "%Y-%m-%d %H:%M:%S")

                            else:
                                query_two_datetime = datetime.strptime(
                                    str(" ".join(test_query_file.split(" ")[1:]).split(".")[0]), "%Y-%m-%d %H:%M:%S")


                            # check, if the second query was prompted BEFORE the first query
                            # because the pure timeframes could be the same -> us the numbers for a complete comparison
                            if get_query_file_number(query_file) < get_query_file_number(test_query_file):
                                # if the second, test file, is older than 25 hours, compared to the first one
                                #
                                # -> end the loop and jump to the next query in the outer foreach loop of queries
                                # .. because every following 'test_query' would also be min. 25hours younger, compared to
                                # .. .. the outer query
                                if ((query_two_datetime - timedelta(hours=25)) <= query_one_datetime):


                                    # open the files to compare the 'test' file with the first one
                                    # -> to see, if the 'test' file is equal to the first one
                                    with open(test_query_file, "rt") as json_test_data:
                                        query_two = json.load(json_test_data)

                                        # again, only look at the SELECT queries
                                        if query_two["queryType"] == "SELECT":


                                            # mark the second query, if it was created after the first one
                                            # .. and their contents are the same
                                            # .. and the second query was created/prompted not longer than 25hours after the first one
                                            # ----(secured, through the above 'if', which in this case, breaks the loop)
                                            #
                                            # from the sparql object all expressions are separated, which do not change the semantic
                                            # .. of the query. e.g. the SELECT, LIMIT, OFFSET
                                            # .. -> we are only looking for the pure "WHERE" part of the query
                                            query_one_comparable = query_one["where"]
                                            query_two_compareable = query_two["where"]

                                            if compare_dictionary_structure(query_one_comparable, query_two_compareable):
                                                # add a 'x' to the name of the file, which is identified to be redundant to the first one
                                                new_file_name = test_query_file.title().split("/")
                                                new_file_name[len(new_file_name) - 1] = "x " + new_file_name[len(new_file_name) - 1]

                                                new_file_name = "/".join(new_file_name).lower()



                                                # replace the test query file name with its new, marked name
                                                # .. but not, if the file about to be renamed was already marked with an 'x'

                                                os.rename(test_query_file, new_file_name)
                                                print("Marked as redundant: ", test_query_file.title().lower())
                                                print("Because of: ", query_file.title().lower())
                                                print("New name: ", new_file_name)
                                                print("\n")

                                                queries_marked += 1


                                                # save the information, about the renaming (for debugging)
                                                renamed_dict = {
                                                    "Marked as deleted: ": test_query_file.title().lower(),
                                                    "Marked as deleted Query Text: ": query_two,
                                                    "Because of: ": query_file.title().lower(),
                                                    "Because of Query Text: ": query_one,
                                                    "New name: ": new_file_name
                                                }

                                                with open(test_query_file.replace(".json", "_deletion_information.json"),
                                                          "w") as renamed_data:
                                                    json.dump(renamed_dict, renamed_data)

                                                renamed_data.close()

                                    json_test_data.close()

                                else:
                                    break

                json_data.close()

    # print/save information from the redundant-detection
    print("Total queries: ", query_count)
    print("Queries marked: ", queries_marked)

    renamed_dict = {}
    renamed_dict["Total queries: "] = query_count
    renamed_dict["Queries marked: "] = queries_marked

    with open("data/statistical_information/redundant_detection/" + timeframe[:21] + "/" + location.split("/")[-2] + "/" +
              location.split("/")[-1] + "_renaming_information.json", "w") as renamed_data:
        json.dump(renamed_dict, renamed_data)


def compare_dictionary_structure(dict1, dict2):
    result = False
    if dict1 == dict2:
        result = True
    return result

def get_query_file_number(query):
    # data/.../146 2017-06-12 02:13:12.json -> 146
    #  remove the 'x', if a marked file should be compared
    #
    # e.g., if the script is run on an already marked dataset
    return int(query.replace("x ", "").split("/")[-1].split(" ")[0])

