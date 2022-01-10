import glob
import json
import os
from datetime import datetime, timedelta


# detection of redundant queries
# f.e. if a user executes a query multiples times
# -> this still counts as only one query (in theory, this has to be done with the other queries, too)

def delete_redundant_queries(timeframe, location):
    # Retrieve all files, ending with .json
    files_sparql = glob.glob("data/" + timeframe[:21] + "/" +
                                  timeframe[22:] + "/" + location + "/*.sparql")

    i = 0
    for query_file in sorted(files_sparql):

        with open(query_file, "rt") as sparql_data:
            query_one = sparql_data.read()

            # ignore files, which were marked as deleted beforehand
            path_of_sparql_data = sparql_data.name.split("/")
            title_of_sparql_data = str(path_of_sparql_data[len(path_of_sparql_data)-1])

            if not title_of_sparql_data.startswith("x"):

                for test_query_file in sorted(files_sparql):

                    # look only at the files, which are max. 25hours apart

                    # data/.../146 2017-06-12 02:13:12.json -> datetime( 2017-06-12 02:13:12 )
                    query_one_datetime = datetime.strptime(str(" ".join(query_file.split(" ")[1:]).split(".")[0]),
                                                           "%Y-%m-%d %H:%M:%S")
                    query_two_datetime = datetime.strptime(
                        str(" ".join(test_query_file.split(" ")[1:]).split(".")[0]),
                        "%Y-%m-%d %H:%M:%S")

                    # if the second, test file, is older than 25 hours, compared to the first one
                    # -> end the loop
                    if query_two_datetime - timedelta(hours=25) <= query_one_datetime:
                        break

                    # open the files again to compare a 'test' file with the first one
                    # -> to see, if the 'test' file is equal to the first one
                    with open(test_query_file, "rt") as sparql_test_data:
                        query_two = sparql_test_data.read()

                        # mark the second query, if it was created after the first one
                        # .. and their contents are the same
                        # .. and th second query was created/prompted not longer than 25hours after the first one
                        # ----(secured, through the above 'if', which in this case, breaks the loop)
                        if query_one_datetime < query_two_datetime and query_one == query_two:

                            # add a 'x' to the name of the file, which is to be deleted
                            new_file_name = test_query_file.title().split("/")
                            new_file_name[len(new_file_name)-1] = "x " + new_file_name[len(new_file_name)-1]

                            new_file_name = "/".join(new_file_name).lower()

                            print("Marked as deleted: ", test_query_file.title().lower())
                            print("Because of: ", query_file.title().lower())
                            print("New name: ", new_file_name)
                            print("\n")

                            # replace the test query file name with its new, marked name
                            #os.rename(test_query_file, new_file_name)

                            # save the information, about the renaming (for debugging)
                            renamed_dict = {
                                "Marked as deleted: ": test_query_file.title().lower(),
                                "Marked as deleted Query Text: ": query_two,
                                "Because of: ": query_file.title().lower(),
                                "Because of Query Text: ": query_one,
                                "New name: ": new_file_name
                            }
                            with open(test_query_file.replace(".sparql", "_deletion_information.json"), "w") as renamed_data:
                                json.dump(renamed_dict, renamed_data)

                            renamed_data.close()

                    sparql_test_data.close()
        sparql_data.close()
