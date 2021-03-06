import json
import glob
import os
import shutil

"""{
# scenario 5:
# BIND( ...

# Property Path
# Union ...
# Having

# scenario X for DESCRIBE, CONSTRUCT, ...?

# Others in others
}"""
import query_research.bound_variables as bound_variables

import query_research.scenarios.scenario_prop_one_detection as scenario_prop_one_detection
import query_research.scenarios.scenario_prop_three_detection as scenario_prop_three_detection
import query_research.scenarios.scenario_prop_two_detection as scenario_prop_two_detection
import query_research.scenarios.scenario_prop_four_detection as scenario_prop_four_detection

import query_research.scenarios.scenario_obj_one_detection as scenario_obj_one_detection
import query_research.scenarios.scenario_obj_two_detection as scenario_obj_two_detection
import query_research.scenarios.scenario_obj_three_detection as scenario_obj_three_detection
import query_research.scenarios.scenario_obj_four_detection as scenario_obj_four_detection

import query_research.scenarios.scenario_sub_one_detection as scenario_sub_one_detection
import query_research.scenarios.scenario_sub_two_detection as scenario_sub_two_detection
import query_research.scenarios.scenario_sub_three_detection as scenario_sub_three_detection
import query_research.scenarios.scenario_sub_four_detection as scenario_sub_four_detection

import query_research.scenarios.scenario_filter_detection as scenario_filter_detection
import query_research.scenarios.scenario_optional_detection as scenario_optional_detection
import query_research.scenarios.scenario_union_detection as scenario_union_detection
import query_research.scenarios.scenario_prop_path_detection as scenario_prop_path_detection
import query_research.scenarios.scenario_bind_detection as scenario_bind_detection
import query_research.scenarios.scenario_blank_node_detection as scenario_blank_node_detection
import query_research.scenarios.scenario_minus_detection as scenario_minus_detection
import query_research.scenarios.scenario_subselect_detection as scenario_subselect_detection
import query_research.scenarios.scenario_literal_detection as scenario_literal_detection
import query_research.scenarios.scenario_values_detection as scenario_values_detection
import query_research.scenarios.scenario_service_detection as scenario_service_detection

def detect_scenarios(location, data_type, redundant_mode):

    if redundant_mode not in ["redundant", "non_redundant"]:
        error_message = "Not supported redundancy mode: ", redundant_mode
        raise Exception(error_message)

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

    # get the path to the folder, where all scenarios are saved
    path_to_scenarios = "data/" + location[:21] + "/" + location[22:] + "/" + \
                        data_type.split('/')[0] + "/scenarios/" + redundant_mode
    # get the path to the folder, where the json file about the gathered statistical information
    # .. is stored
    path_to_stat_information = "data/" + location[:21] + "/" + location[22:] + "/" + \
                        data_type.split('/')[0] + "/statistical_information/" + redundant_mode


    total_SELECT_queries = 0
    total_DESCRIBE_queries = 0
    total_CONSTRUCT_queries = 0
    total_ASK_queries = 0

    total_metadata_found_in_SELECT_SPARQL_expression = 0

    # a scenario fora non-recognized scenario

    # to check for the type of the SPARQL query (SELECT, DESCRIBE, ASK, CONSTRUCT)
    for query_file in files_json:
        if os.path.isfile(query_file.title().lower()):
            with open(query_file, "rt") as json_data:
                json_object = json.load(json_data)

                if json_object["queryType"] == "SELECT":
                    total_SELECT_queries += 1
                elif json_object["queryType"] == "DESCRIBE":
                    total_DESCRIBE_queries += 1
                elif json_object["queryType"] == "ASK":
                    total_ASK_queries += 1
                elif json_object["queryType"] == "CONSTRUCT":
                    total_CONSTRUCT_queries += 1

            json_data.close()

    # to check for the scenarios
    array_looking_for = get_mode(data_type)
    dict_overview_looking_for = {"list_per_search": []}

    for looking_for_list in array_looking_for:

        # create a scenario per "looking for" , e.g. "wasDerivedFrom"
        dict_looking_for = {
            "looking_for": str(looking_for_list),
            "total_occurrences": 0,
            "total_scenarios": 0,
            "prop_one": 0,
            "prop_two": 0,
            "prop_three": 0,
            "prop_four": 0,
            "obj_one": 0,
            "obj_two": 0,
            "obj_three": 0,
            "obj_four": 0,
            "sub_one": 0,
            "sub_two": 0,
            "sub_three": 0,
            "sub_four": 0,
            "filter": 0,
            "optional": 0,
            "union": 0,
            "prop_path": 0,
            "bind": 0,
            "blank_node": 0,
            "minus": 0,
            "subselect": 0,
            "literal": 0,
            "values": 0,
            "service": 0,
            "other": 0}
        # TODO: Add "total" occurrences of a "looking for"

        for query_file in files_json:

            if os.path.isfile(query_file.title().lower()):

                # a boolean, to tell if something from the looking for list has been found
                metadata_of_looking_for_list_found = False

                with open(query_file, "rt") as json_data:
                    json_object = json.load(json_data)
                    # only apply the scenarios to SELECT queries
                    if json_object["queryType"] == "SELECT":

                        # the path to the sparql text file (corresponding to the json object
                        # to later be able to copy the sparql text file to a specific directors (for debugging)
                        # data/2017-06-12_2017-07-09/Organic/Reference_Metadata/Derived_+_Reference_Property/182150 2017-07-07 19:06:30.json
                        # -->
                        # data/2017-06-12_2017-07-09/Organic/Reference_Metadata/Derived_+_Reference_Property/182150 2017-07-07 19:06:30.sparql
                        path_to_sparql_text_file = query_file[:-4]+"sparql"

                        # if the query file is from a marked query e.g.
                        # data/2017-06-12_2017-07-09/Organic/Reference_Metadata/Derived_+_Reference_Property/x 182150 2017-07-07 19:06:30.sparql
                        # --> delete the "x " from the path
                        path_to_sparql_text_file = path_to_sparql_text_file.replace("x ", "")

                        # in case, the query file was marked as redundant -> remove the "x "....
                        path_to_sparql_text_file.replace("x ", "")

                        # to later check, if something changed in the list
                        # -> to detect, if a scenario did apply
                        tmp_dict = dict_looking_for.copy()

                        # extract the BOUND variables in the query and hand them over to each statement
                        # --> so, that this step is not necessary in every step
                        found_bound_variables = bound_variables.find_bound_variables(json_object)

                        # variables for the currently found scenarios per looking for list
                        occurrences_scenario_prop_one = 0
                        occurrences_scenario_prop_three = 0
                        occurrences_scenario_prop_two = 0
                        occurrences_scenario_prop_four = 0
                        occurrences_scenario_obj_one = 0
                        occurrences_scenario_obj_two = 0
                        occurrences_scenario_obj_three = 0
                        occurrences_scenario_obj_four = 0
                        occurrences_scenario_sub_one = 0
                        occurrences_scenario_sub_two = 0
                        occurrences_scenario_sub_three = 0
                        occurrences_scenario_sub_four = 0
                        occurrences_scenario_bind = 0
                        occurrences_scenario_blank_node = 0
                        occurrences_scenario_filter = 0
                        occurrences_scenario_literal = 0
                        occurrences_scenario_minus = 0
                        occurrences_scenario_optional = 0
                        occurrences_scenario_prop_path = 0
                        occurrences_scenario_subselect = 0
                        occurrences_scenario_union = 0
                        occurrences_scenario_values = 0
                        occurrences_scenario_service = 0

                        # delete all the 'first-class' found GROUP
                        #SELECT(COUNT( ?var1  ) AS  ?var2  )
                        #WHERE
                        #{
                        #?var1 < http: // www.w3.org / ns / prov
                        ## wasDerivedFrom>  ?var3 .
                        #{
                        #?var3 < http: // www.wikidata.org / prop / reference / P248 > < http: // www.wikidata.org / entity / Q29583405 >.
                        #}
                        #}
                        #
                        # And insert them to the WHERE types in the query
                        # .. there might occur a double group, e.g. a group in a group
                        # .. but there wasn't a single case found in the data

                        delete_and_join_group(json_object)



                        for looking_for in looking_for_list:

                            total_metadata_found_in_SELECT_SPARQL_expression += str(json_object["variables"]).count(looking_for)
                            if str(json_object["variables"]).count(looking_for) > 0:
                                print(json_data.name)


                            # variable to count the found scenarios
                            scenario_count = 0

                            # scenario prop_one
                            tmp_occurrences = \
                                scenario_prop_one_detection.\
                                    scenario_prop_one_occurrences(json_object, looking_for, found_bound_variables)
                            occurrences_scenario_prop_one += tmp_occurrences
                            dict_looking_for["prop_one"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                # copy the corresponding sparql file (to the JSON file) to a specific folder for scenarios
                                # .. used for debugging and review of the results
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/prop_one")

                            # scenario prop_three
                            tmp_occurrences = \
                                scenario_prop_three_detection.\
                                    scenario_prop_three_occurrences(json_object, looking_for, found_bound_variables)
                            occurrences_scenario_prop_three += tmp_occurrences
                            dict_looking_for["prop_three"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/prop_three")

                            # scenario prop_two
                            tmp_occurrences = \
                                scenario_prop_two_detection.\
                                    scenario_prop_two_occurrences(json_object, looking_for, found_bound_variables)
                            occurrences_scenario_prop_two += tmp_occurrences
                            dict_looking_for["prop_two"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/prop_two")

                            # scenario prop_four
                            tmp_occurrences = \
                                scenario_prop_four_detection.\
                                    scenario_prop_four_occurrences(json_object, looking_for, found_bound_variables)
                            occurrences_scenario_prop_four += tmp_occurrences
                            dict_looking_for["prop_four"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/prop_four")

                            # scenario obj_one
                            tmp_occurrences = \
                                scenario_obj_one_detection.\
                                    scenario_obj_one_occurrences(json_object, looking_for, found_bound_variables)
                            occurrences_scenario_obj_one += tmp_occurrences
                            dict_looking_for["obj_one"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/obj_one")

                            # scenario obj_two
                            tmp_occurrences = \
                                scenario_obj_two_detection.\
                                    scenario_obj_two_occurrences(json_object, looking_for, found_bound_variables)
                            occurrences_scenario_obj_two += tmp_occurrences
                            dict_looking_for["obj_two"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/obj_two")

                            # scenario obj_three
                            tmp_occurrences = \
                                scenario_obj_three_detection.\
                                    scenario_obj_three_occurrences(json_object, looking_for, found_bound_variables)
                            occurrences_scenario_obj_three += tmp_occurrences
                            dict_looking_for["obj_three"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/obj_three")

                            # scenario obj_four
                            tmp_occurrences = \
                                scenario_obj_four_detection.\
                                    scenario_obj_four_occurrences(json_object, looking_for, found_bound_variables)
                            occurrences_scenario_obj_four += tmp_occurrences
                            dict_looking_for["obj_four"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/obj_four")

                            # scenario sub_one
                            tmp_occurrences = \
                                scenario_sub_one_detection.\
                                    scenario_sub_one_occurrences(json_object, looking_for, found_bound_variables)
                            occurrences_scenario_sub_one += tmp_occurrences
                            dict_looking_for["sub_one"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/sub_one")

                            # scenario sub_two
                            tmp_occurrences = \
                                scenario_sub_two_detection.\
                                    scenario_sub_two_occurrences(json_object, looking_for, found_bound_variables)
                            occurrences_scenario_sub_two += tmp_occurrences
                            dict_looking_for["sub_two"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/sub_two")

                            # scenario sub_three
                            tmp_occurrences = \
                                scenario_sub_three_detection.\
                                    scenario_sub_three_occurrences(json_object, looking_for, found_bound_variables)
                            occurrences_scenario_sub_three += tmp_occurrences
                            dict_looking_for["sub_three"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/sub_three")

                            # scenario sub_four
                            tmp_occurrences = \
                                scenario_sub_four_detection.\
                                    scenario_sub_four_occurrences(json_object, looking_for, found_bound_variables)
                            occurrences_scenario_sub_four += tmp_occurrences
                            dict_looking_for["sub_four"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/sub_four")

                            # scenario filter
                            tmp_occurrences = \
                                scenario_filter_detection.\
                                    scenario_filter_occurrences(json_object, looking_for,
                                                              path_to_scenarios, found_bound_variables, True, data_type)
                            occurrences_scenario_filter += tmp_occurrences
                            dict_looking_for["filter"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/filter")

                            # scenario optional
                            tmp_occurrences = \
                                scenario_optional_detection.\
                                    scenario_optional_occurrences(json_object, looking_for,
                                                              path_to_scenarios, found_bound_variables, True, data_type)
                            occurrences_scenario_optional += tmp_occurrences
                            dict_looking_for["optional"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/optional")

                            # scenario union
                            tmp_occurrences = \
                                scenario_union_detection.\
                                    scenario_union_occurrences(json_object, looking_for,
                                                              path_to_scenarios, found_bound_variables, True, data_type)
                            occurrences_scenario_union += tmp_occurrences
                            dict_looking_for["union"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/union")

                            # scenario property path
                            tmp_occurrences = \
                                scenario_prop_path_detection.\
                                    scenario_prop_path_occurrences(json_object, looking_for,
                                                               path_to_scenarios, found_bound_variables, True, data_type)
                            occurrences_scenario_prop_path += tmp_occurrences
                            dict_looking_for["prop_path"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/prop_path")

                            # find, if a scenario group is still in the code
                            group_where = json_object["where"]
                            # find scenarios 'group'
                            for group_where_part in group_where:
                                if group_where_part["type"] == "group":
                                    raise Exception


                            # scenario bind
                            # additionally add the path to the scenario -> for the statistical information
                            # about the scenarios the found bound variables are in
                            #
                            # and a boolean, that tells the script, to look for the scenarios, that the 'new' variables
                            #   may be used in
                            tmp_occurrences = \
                                scenario_bind_detection.\
                                    scenario_bind_occurrences(json_object, looking_for,
                                                              path_to_scenarios, found_bound_variables, True, data_type)
                            occurrences_scenario_bind += tmp_occurrences
                            dict_looking_for["bind"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/bind")

                            # scenario blank node
                            tmp_occurrences = \
                                scenario_blank_node_detection.\
                                    scenario_blank_node_occurrences(json_object, looking_for, found_bound_variables)
                            occurrences_scenario_blank_node += tmp_occurrences
                            dict_looking_for["blank_node"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/blank_node")

                            # scenario minus
                            tmp_occurrences = \
                                scenario_minus_detection.\
                                    scenario_minus_occurrences(json_object, looking_for,
                                                               path_to_scenarios, found_bound_variables, True, data_type)
                            occurrences_scenario_minus += tmp_occurrences
                            dict_looking_for["minus"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/minus")

                            # scenario subselect
                            tmp_occurrences = \
                                scenario_subselect_detection.\
                                    scenario_subselect_occurrences(json_object, looking_for,
                                                               path_to_scenarios, found_bound_variables, True, data_type)
                            occurrences_scenario_subselect += tmp_occurrences
                            dict_looking_for["subselect"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/subselect")

                            # scenario literal
                            tmp_occurrences = \
                                scenario_literal_detection.\
                                    scenario_literal_occurrences(json_object, looking_for, found_bound_variables)
                            occurrences_scenario_literal += tmp_occurrences
                            dict_looking_for["literal"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/literal")

                            # scenario values
                            tmp_occurrences = \
                                scenario_values_detection.\
                                    scenario_values_occurrences(json_object, looking_for, found_bound_variables)
                            occurrences_scenario_values += tmp_occurrences
                            dict_looking_for["values"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/values")

                            # scenario service
                            tmp_occurrences = \
                                scenario_service_detection.\
                                    scenario_service_occurrences(json_object, looking_for, found_bound_variables)
                            occurrences_scenario_service += tmp_occurrences
                            dict_looking_for["service"] += tmp_occurrences
                            if tmp_occurrences > 0:
                                shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/service")

                            # check, if any scenario did apply
                            if dict_looking_for != tmp_dict:
                                metadata_of_looking_for_list_found = True

                            # detect, how many times the item we are looking for in the current
                            # .. loop is detected in the json object
                            # -> there may be multiple occurrences per query
                            dict_looking_for["total_occurrences"] += str(json_object).count(looking_for)

                        # count the found scenarios
                        scenario_count += \
                            occurrences_scenario_prop_one + \
                            occurrences_scenario_prop_three + \
                            occurrences_scenario_prop_two + \
                            occurrences_scenario_prop_four + \
                            occurrences_scenario_obj_one + \
                            occurrences_scenario_obj_two + \
                            occurrences_scenario_obj_three + \
                            occurrences_scenario_obj_four + \
                            occurrences_scenario_sub_one + \
                            occurrences_scenario_sub_two + \
                            occurrences_scenario_sub_three + \
                            occurrences_scenario_sub_four + \
                            occurrences_scenario_bind + \
                            occurrences_scenario_blank_node + \
                            occurrences_scenario_filter + \
                            occurrences_scenario_literal + \
                            occurrences_scenario_minus + \
                            occurrences_scenario_optional + \
                            occurrences_scenario_prop_path + \
                            occurrences_scenario_subselect + \
                            occurrences_scenario_union + \
                            occurrences_scenario_values + \
                            occurrences_scenario_service

                        occurrences_scenario_other = 0
                        # check  if no scenario did apply
                        if not metadata_of_looking_for_list_found:

                            # save one 'other' scenario
                            occurrences_scenario_other = 1


                            dict_looking_for["other"] += occurrences_scenario_other
                            shutil.copy(path_to_sparql_text_file, path_to_scenarios + "/other")
                            # with the "other" -> also copy the .json file
                            # -> so, it is a bit easier to develop new filters
                            shutil.copy(query_file, path_to_scenarios + "/other")

                        # save the total found scenarios PLUS the OTHER scenario
                        scenario_count += occurrences_scenario_other
                        dict_looking_for["total_scenarios"] += scenario_count


                        tmp_found_metadata = 0
                        for looking_for in looking_for_list:
                            tmp_found_metadata += str(json_object).count(looking_for)


                        if (tmp_found_metadata  != scenario_count):
                            #if (occurrences_scenario_prop_path == 0):
                            if(not(occurrences_scenario_prop_one == 0 and
                                occurrences_scenario_prop_three == 0 and
                                occurrences_scenario_prop_two == 0 and
                                occurrences_scenario_prop_four == 0 and
                                occurrences_scenario_obj_one == 0 and
                                occurrences_scenario_obj_two == 0 and
                                occurrences_scenario_obj_three == 0 and
                                occurrences_scenario_obj_four == 0 and
                                occurrences_scenario_sub_one == 0 and
                                occurrences_scenario_sub_two == 0 and
                                occurrences_scenario_sub_three == 0 and
                                occurrences_scenario_sub_four == 0 and
                                occurrences_scenario_bind == 0 and
                                occurrences_scenario_blank_node != 0 and
                                #occurrences_scenario_filter == 0 and
                                occurrences_scenario_literal == 0 and
                                occurrences_scenario_minus == 0 and
                                #occurrences_scenario_optional == 0 and
                                occurrences_scenario_prop_path != 0 and
                                occurrences_scenario_subselect == 0 and
                                #occurrences_scenario_union == 0 and
                                occurrences_scenario_values == 0 and
                                occurrences_scenario_service == 0 and
                                occurrences_scenario_other == 0)
                            and
                                not(occurrences_scenario_prop_one == 0 and
                                    occurrences_scenario_prop_three == 0 and
                                    occurrences_scenario_prop_two == 0 and
                                    occurrences_scenario_prop_four == 0 and
                                    occurrences_scenario_obj_one == 0 and
                                    occurrences_scenario_obj_two == 0 and
                                    occurrences_scenario_obj_three == 0 and
                                    occurrences_scenario_obj_four == 0 and
                                    occurrences_scenario_sub_one == 0 and
                                    occurrences_scenario_sub_two == 0 and
                                    occurrences_scenario_sub_three == 0 and
                                    occurrences_scenario_sub_four == 0 and
                                     occurrences_scenario_bind == 0 and
                                     occurrences_scenario_blank_node == 0 and
                                     occurrences_scenario_filter == 0 and
                                     occurrences_scenario_literal == 0 and
                                     occurrences_scenario_minus == 0 and
                                     occurrences_scenario_optional == 0 and
                                     occurrences_scenario_prop_path == 0 and
                                     occurrences_scenario_subselect == 0 and
                                     occurrences_scenario_union == 0 and
                                     occurrences_scenario_values == 0 and
                                     occurrences_scenario_service == 0 and
                                     occurrences_scenario_other != 0)
                            and
                                not (occurrences_scenario_prop_one == 0 and
                                    occurrences_scenario_prop_three == 0 and
                                    occurrences_scenario_prop_two == 0 and
                                    occurrences_scenario_prop_four == 0 and
                                    occurrences_scenario_obj_one == 0 and
                                    occurrences_scenario_obj_two == 0 and
                                    occurrences_scenario_obj_three == 0 and
                                    occurrences_scenario_obj_four == 0 and
                                    occurrences_scenario_sub_one == 0 and
                                    occurrences_scenario_sub_two == 0 and
                                    occurrences_scenario_sub_three == 0 and
                                    occurrences_scenario_sub_four == 0 and
                                     occurrences_scenario_bind == 0 and
                                     occurrences_scenario_blank_node == 0 and
                                     occurrences_scenario_filter == 0 and
                                     occurrences_scenario_literal != 0 and
                                     occurrences_scenario_minus == 0 and
                                     occurrences_scenario_optional == 0 and
                                     occurrences_scenario_prop_path != 0 and
                                     occurrences_scenario_subselect == 0 and
                                     occurrences_scenario_union == 0 and
                                     occurrences_scenario_values == 0 and
                                     occurrences_scenario_service == 0 and
                                     occurrences_scenario_other == 0)
                            and
                                not (occurrences_scenario_prop_one == 0 and
                                    occurrences_scenario_prop_three == 0 and
                                    occurrences_scenario_prop_two == 0 and
                                    occurrences_scenario_prop_four == 0 and
                                    occurrences_scenario_obj_one == 0 and
                                    occurrences_scenario_obj_two == 0 and
                                    occurrences_scenario_obj_three == 0 and
                                    occurrences_scenario_obj_four == 0 and
                                    occurrences_scenario_sub_one == 0 and
                                    occurrences_scenario_sub_two == 0 and
                                    occurrences_scenario_sub_three == 0 and
                                    occurrences_scenario_sub_four == 0 and
                                     occurrences_scenario_bind == 0 and
                                     occurrences_scenario_blank_node != 0 and
                                     occurrences_scenario_filter == 0 and
                                     occurrences_scenario_literal != 0 and
                                     occurrences_scenario_minus == 0 and
                                     #occurrences_scenario_optional == 0 and
                                     occurrences_scenario_prop_path == 0 and
                                     occurrences_scenario_subselect == 0 and
                                     #occurrences_scenario_union == 0 and
                                     occurrences_scenario_values == 0 and
                                     occurrences_scenario_service == 0 and
                                     occurrences_scenario_other == 0)
                            ):

                                print("Detected a difference between the number of detected scenarios and found metadata in"
                                      " the query.")
                                print("prop_one: " , occurrences_scenario_prop_one , \
                                "prop_three: " , occurrences_scenario_prop_three , \
                                "prop_two: " , occurrences_scenario_prop_two , \
                                "prop_four: " , occurrences_scenario_prop_four , \
                                "obj_one: " , occurrences_scenario_obj_one , \
                                "obj_two: " , occurrences_scenario_obj_two , \
                                "obj_three: " , occurrences_scenario_obj_three , \
                                "obj_four: " , occurrences_scenario_obj_four , \
                                "sub_one: " , occurrences_scenario_sub_one , \
                                "sub_two: " , occurrences_scenario_sub_two , \
                                "sub_three: " , occurrences_scenario_sub_three , \
                                "sub_four: " , occurrences_scenario_sub_four , "\n", \
                                "bind: " , occurrences_scenario_bind , \
                                "blank: " , occurrences_scenario_blank_node , \
                                "filter: " , occurrences_scenario_filter , \
                                "literal: " , occurrences_scenario_literal, "\n" , \
                                "minus: " , occurrences_scenario_minus , \
                                "optional: " , occurrences_scenario_optional , \
                                "prop_path: " , occurrences_scenario_prop_path , \
                                "subselect: " , occurrences_scenario_subselect , \
                                "union: " , occurrences_scenario_union, \
                                "values: ", occurrences_scenario_values, \
                                "service: ", occurrences_scenario_service, \
                                "other: ", occurrences_scenario_other)
                                print(tmp_found_metadata)
                                print(json_data.name)
                                print("\n")

                    json_data.close()


        # attach the dictionary for looking for to the dictionary for the whole data type
        dict_overview_looking_for["list_per_search"].append(dict_looking_for)

    if total_metadata_found_in_SELECT_SPARQL_expression > 0:
        print("Found metadata signs inside a SPARQL SELECT expressions: ", total_metadata_found_in_SELECT_SPARQL_expression)

    scenario_dict = {
        "data_type": data_type,
        "total_queries": files_json.__len__(),
        "SELECT_queries": total_SELECT_queries,
        "DESCRIBE_queries": total_DESCRIBE_queries,
        "CONSTRUCT_queries": total_CONSTRUCT_queries,
        "ASK_queries": total_ASK_queries,
        "found_scenarios": dict_overview_looking_for
    }

    # save the scneario_dict to a folder
    with open(path_to_stat_information + "/" + data_type.split('/')[1] + ".json", "wt") as information_data:
        json.dump(scenario_dict, information_data)
    information_data.close()

    # test the bind variables

    return


def delete_and_join_group(json_object):
    # recursive fun
    group_was_found = False

    where = json_object["where"]
    for where_part in where:
        if where_part["type"] == "group":
            json_object["where"].remove(where_part)
            json_object["where"] = json_object["where"] + where_part["patterns"]
            group_was_found = True

    if group_was_found:
        # recursion start
        delete_and_join_group(json_object)
    else:
        # recursion stop
        return



def get_mode(data_type):
    # references
    #
    # the reference property can also be in the form of value or value-normalized
    if data_type == "reference_metadata/all_three":
        return [["http://www.wikidata.org/reference/"], ["http://www.wikidata.org/prop/reference/P",
                                                         "http://www.wikidata.org/prop/reference/value/P",
                                                         "http://www.wikidata.org/prop/reference/value-normalized/P"],
                                                        ["http://www.w3.org/ns/prov#wasDerivedFrom"]]
    elif data_type == "reference_metadata/derived_+_reference_node":
        return [["http://www.wikidata.org/reference/"], ["http://www.w3.org/ns/prov#wasDerivedFrom"]]
    elif data_type == "reference_metadata/derived_+_reference_property":
        return [["http://www.wikidata.org/prop/reference/P","http://www.wikidata.org/prop/reference/value/P",
                                                         "http://www.wikidata.org/prop/reference/value-normalized/P"],
                                                        ["http://www.w3.org/ns/prov#wasDerivedFrom"]]
    elif data_type == "reference_metadata/only_derived":
        return [["http://www.w3.org/ns/prov#wasDerivedFrom"]]
    elif data_type == "reference_metadata/only_reference_node":
        return [["http://www.wikidata.org/reference/"]]
    elif data_type == "reference_metadata/only_reference_property":
        return [["http://www.wikidata.org/prop/reference/P", "http://www.wikidata.org/prop/reference/value/P",
                                                         "http://www.wikidata.org/prop/reference/value-normalized/P"]]
    elif data_type == "reference_metadata/reference_node_+_reference_property":
        return [["http://www.wikidata.org/prop/reference/P","http://www.wikidata.org/prop/reference/value/P",
                                                         "http://www.wikidata.org/prop/reference/value-normalized/P"],
                ["http://www.wikidata.org/reference/"]]

    # ranks
    elif data_type == "rank_metadata/rank_property":
        return [["http://wikiba.se/ontology#rank"]]
    elif data_type == "rank_metadata/preferred_rank_+_rank_property":
        return [["http://wikiba.se/ontology#rank"], ["http://wikiba.se/ontology#PreferredRank"]]
    elif data_type == "rank_metadata/normal_rank_+_rank_property":
        return [["http://wikiba.se/ontology#rank"], ["http://wikiba.se/ontology#NormalRank"]]
    elif data_type == "rank_metadata/deprecated_rank_+_rank_property":
        return [["http://wikiba.se/ontology#rank"], ["http://wikiba.se/ontology#DeprecatedRank"]]
    elif data_type == "rank_metadata/preferred_+_normal_rank_+_rank_property":
        return [["http://wikiba.se/ontology#rank"], ["http://wikiba.se/ontology#PreferredRank"],
                ["http://wikiba.se/ontology#NormalRank"]]
    elif data_type == "rank_metadata/preferred_+_deprecated_rank_+_rank_property":
        return [["http://wikiba.se/ontology#rank"], ["http://wikiba.se/ontology#PreferredRank"],
                ["http://wikiba.se/ontology#DeprecatedRank"]]
    elif data_type == "rank_metadata/normal_+_deprecated_rank_+_rank_property":
        return [["http://wikiba.se/ontology#rank"], ["http://wikiba.se/ontology#NormalRank"],
                ["http://wikiba.se/ontology#DeprecatedRank"]]
    elif data_type == "rank_metadata/all_ranks_+_rank_property":
        return [["http://wikiba.se/ontology#rank"], ["http://wikiba.se/ontology#PreferredRank"],
                ["http://wikiba.se/ontology#NormalRank"], ["http://wikiba.se/ontology#DeprecatedRank"]]
    elif data_type == "rank_metadata/normal_rank":
        return [["http://wikiba.se/ontology#NormalRank"]]
    elif data_type == "rank_metadata/deprecated_rank":
        return [["http://wikiba.se/ontology#DeprecatedRank"]]
    elif data_type == "rank_metadata/preferred_rank":
        return [["http://wikiba.se/ontology#PreferredRank"]]
    elif data_type == "rank_metadata/preferred_+_normal_rank":
        return [["http://wikiba.se/ontology#PreferredRank"], ["http://wikiba.se/ontology#NormalRank"]]
    elif data_type == "rank_metadata/preferred_+_deprecated_rank":
        return [["http://wikiba.se/ontology#PreferredRank"], ["http://wikiba.se/ontology#DeprecatedRank"]]
    elif data_type == "rank_metadata/normal_+_deprecated_rank":
        return [["http://wikiba.se/ontology#NormalRank"], ["http://wikiba.se/ontology#DeprecatedRank"]]
    elif data_type == "rank_metadata/all_ranks":
        return [["http://wikiba.se/ontology#PreferredRank"], ["http://wikiba.se/ontology#NormalRank"],
                ["http://wikiba.se/ontology#DeprecatedRank"]]

    elif data_type == "rank_metadata/rank_property_+_best_rank_property":
        return [["http://wikiba.se/ontology#rank"], ["http://wikiba.se/ontology#BestRank"]]
    elif data_type == "rank_metadata/preferred_rank_+_rank_property_+_best_rank_property":
        return [["http://wikiba.se/ontology#rank"], ["http://wikiba.se/ontology#PreferredRank"],
                ["http://wikiba.se/ontology#BestRank"]]
    elif data_type == "rank_metadata/normal_rank_+_rank_property_+_best_rank_property":
        return [["http://wikiba.se/ontology#rank"], ["http://wikiba.se/ontology#NormalRank"],
                ["http://wikiba.se/ontology#BestRank"]]
    elif data_type == "rank_metadata/deprecated_rank_+_rank_property_+_best_rank_property":
        return [["http://wikiba.se/ontology#rank"], ["http://wikiba.se/ontology#DeprecatedRank"],
                ["http://wikiba.se/ontology#BestRank"]]
    elif data_type == "rank_metadata/preferred_+_normal_rank_+_rank_property_+_best_rank_property":
        return [["http://wikiba.se/ontology#rank"], ["http://wikiba.se/ontology#PreferredRank"],
                ["http://wikiba.se/ontology#NormalRank"], ["http://wikiba.se/ontology#BestRank"]]
    elif data_type == "rank_metadata/preferred_+_deprecated_rank_+_rank_property_+_best_rank_property":
        return [["http://wikiba.se/ontology#rank"], ["http://wikiba.se/ontology#PreferredRank"],
                ["http://wikiba.se/ontology#DeprecatedRank"], ["http://wikiba.se/ontology#BestRank"]]
    elif data_type == "rank_metadata/normal_+_deprecated_rank_+_rank_property_+_best_rank_property":
        return [["http://wikiba.se/ontology#rank"], ["http://wikiba.se/ontology#NormalRank"],
                ["http://wikiba.se/ontology#DeprecatedRank"], ["http://wikiba.se/ontology#BestRank"]]
    elif data_type == "rank_metadata/all_ranks_+_rank_property_+_best_rank_property":
        return [["http://wikiba.se/ontology#rank"], ["http://wikiba.se/ontology#PreferredRank"],
                ["http://wikiba.se/ontology#NormalRank"], ["http://wikiba.se/ontology#DeprecatedRank"],
                ["http://wikiba.se/ontology#BestRank"]]
    elif data_type == "rank_metadata/normal_rank_+_best_rank_property":
        return [["http://wikiba.se/ontology#NormalRank"], ["http://wikiba.se/ontology#BestRank"]]
    elif data_type == "rank_metadata/deprecated_rank_+_best_rank_property":
        return [["http://wikiba.se/ontology#DeprecatedRank"], ["http://wikiba.se/ontology#BestRank"]]
    elif data_type == "rank_metadata/preferred_rank_+_best_rank_property":
        return [["http://wikiba.se/ontology#PreferredRank"], ["http://wikiba.se/ontology#BestRank"]]
    elif data_type == "rank_metadata/preferred_+_normal_rank_+_best_rank_property":
        return [["http://wikiba.se/ontology#PreferredRank"], ["http://wikiba.se/ontology#NormalRank"],
                ["http://wikiba.se/ontology#BestRank"]]
    elif data_type == "rank_metadata/preferred_+_deprecated_rank_+_best_rank_property":
        return [["http://wikiba.se/ontology#PreferredRank"], ["http://wikiba.se/ontology#DeprecatedRank"],
                ["http://wikiba.se/ontology#BestRank"]]
    elif data_type == "rank_metadata/normal_+_deprecated_rank_+_best_rank_property":
        return [["http://wikiba.se/ontology#NormalRank"], ["http://wikiba.se/ontology#DeprecatedRank"],
                ["http://wikiba.se/ontology#BestRank"]]
    elif data_type == "rank_metadata/all_ranks_+_best_rank_property":
        return [["http://wikiba.se/ontology#PreferredRank"], ["http://wikiba.se/ontology#NormalRank"],
                ["http://wikiba.se/ontology#DeprecatedRank"], ["http://wikiba.se/ontology#BestRank"]]
    elif data_type == "rank_metadata/best_rank_property":
        return [["http://wikiba.se/ontology#BestRank"]]

    # qualifiers
    elif data_type == "qualifier_metadata/property_qualifier":
        return [["http://www.wikidata.org/prop/qualifier/P","http://www.wikidata.org/prop/qualifier/value/P",
                 "http://www.wikidata.org/prop/qualifier/value-normalized/P"]]

