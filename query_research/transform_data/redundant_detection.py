import glob
import os
import Levenshtein as lev


# detection of redundant queries by levenshtein distance
# f.e. if a user executes a query multiples times / or corrects an small error
# -> this still counts as only one query (in theory, this has to be done with the other queries, too)

def delete_redundant_queries(location):
    # Retrieve all files, ending with .json
    files_sparql_both = glob.glob("data/" + location[:21] + "/" +
                                  location[22:] + "/both/*.sparql")
    files_sparql_only_derived = glob.glob("data/" + location[:21] + "/" +
                                          location[22:] + "/only_derived/*.sparql")
    files_sparql_only_reference = glob.glob("data/" + location[:21] + "/" +
                                            location[22:] + "/only_reference/*.sparql")

    i = 0
    for query_file in files_sparql_both:
        if os.path.isfile(query_file.title().lower()):
            with open(query_file, "rt") as sparql_data:
                query_one = sparql_data.read()

                for test_query_file in files_sparql_both:
                    if os.path.isfile(test_query_file.title().lower()):
                        with open(test_query_file, "rt") as sparql_test_data:
                            query_two = sparql_test_data.read()

                            if query_one.title() != query_two.title():
                                if lev.ratio(query_one.lower(), query_two.lower()) > 0.9:
                                    path_to_delete = test_query_file.title().lower()
                                    print("Deleting: ", path_to_delete)
                                    print("Because of: ", query_file.title().lower())
                                    print("\n")
                                    os.remove(path_to_delete)
                                    os.remove(path_to_delete[:len(path_to_delete)-7]+".json")

                        sparql_test_data.close()
            sparql_data.close()
