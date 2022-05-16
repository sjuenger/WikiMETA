# method to detect scenario filter
#
#
#
# constellation for "wasDerivedFrom"
#
# scenario filter:
# FILTER( STR(?s) = prov:wasDerivedFrom ) .
#
#
#
# look_for e.g. "http://www.w3.org/ns/prov#wasDerivedFrom"

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
import query_research.scenarios.scenario_group_detection as scenario_group_detection
import query_research.scenarios.scenario_bind_detection as scenario_bind_detection
import query_research.scenarios.scenario_blank_node_detection as scenario_blank_node_detection
import query_research.scenarios.scenario_minus_detection as scenario_minus_detection
import query_research.scenarios.scenario_subselect_detection as scenario_subselect_detection
import query_research.scenarios.scenario_literal_detection as scenario_literal_detection
import query_research.scenarios.scenario_values_detection as scenario_values_detection
import query_research.scenarios.scenario_service_detection as scenario_service_detection

import json
import os

def scenario_filter_occurrences(json_object, look_for, location, bound_variables, look_for_additional_layer, data_type):
    # 'location' is the path to the current 'scenarios' folder
    # -> for the statistical information, in which scenarios the found
    #       metadata are on the 'additional layer'

    where = json_object["where"]

    # find scenarios 'filter'

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:
        if "type" in where_part and where_part["type"] == "filter":
            if (look_for not in str(where_part["expression"])):
                if look_for in str(where_part):
                    raise Exception
            else:
                # there may be more than one
                result += str(where_part["expression"]).count(look_for)


                # if a FILTER scenario is detected -> look one step deeper, which scenario is used INSIDE the FILTER
                #
                # also delete any GROUP, that might be used and join the content to the patterns of the UNION

                delete_and_join_all_GROUP_patterns_to_the_overall_FILTER_patterns(where_part)

                # -> detect the scenario, the found metadata is in
                # but ONLY do that, if the 'look_for_aditional_layer boolean is set to true
                # (to prevent re-iteration)
                if look_for_additional_layer:

                    # dict structure for the counted scenarios
                    scenarios_dict = \
                        {
                            "prop_one": 0,
                            "prop_three": 0,
                            "prop_two": 0,
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
                            "not_found_in_patterns": 0}

                    # look, if there already exists a 'filter_scenarios_information'
                    if os.path.isfile(location + "/filter_statistical_information.json"):
                        with open(location + "/filter_statistical_information.json", "r") as json_data:
                            filter_statistical_information = json.load(json_data)
                            json_data.close()
                    else:

                        filter_statistical_information = \
                            {
                                "total_found_metadata": 0,
                                "metadata_found_in_scenarios": scenarios_dict,
                                "metadata_per_datatype_found_in_scenarios": {},
                                "total_found_operators": 0,
                                "found_operators_overall": {},
                                "found_operators_per_datatype": {}}

                    # check for the datatypes
                    # or/and get the correct scenario dict for the current datatype
                    already_inserted = False
                    for test_dict_datatype in filter_statistical_information["metadata_per_datatype_found_in_scenarios"]:
                        if test_dict_datatype == data_type:
                            already_inserted = True
                            
                            current_datatype_dict = filter_statistical_information[
                                "metadata_per_datatype_found_in_scenarios"][data_type]
                    
                    if not already_inserted:
                        scenarios_dict_datatype = scenarios_dict.copy()
                        filter_statistical_information["metadata_per_datatype_found_in_scenarios"][data_type] =\
                            scenarios_dict_datatype
                        
                        current_datatype_dict = scenarios_dict_datatype
                    
                    
                    filter_statistical_information["total_found_metadata"] += \
                        str(where_part["expression"]["args"]).count(look_for)
                    # detect the scenario on the 'additional' layer

                    tmp_dict = filter_statistical_information["metadata_found_in_scenarios"].copy()

                    # scenario prop_one
                    tmp_occurrences = \
                        scenario_prop_one_detection. \
                            scenario_prop_one_occurrences({"where": where_part["expression"]["args"]}, look_for, bound_variables)
                    filter_statistical_information["metadata_found_in_scenarios"]["prop_one"] += tmp_occurrences
                    current_datatype_dict["prop_one"] += tmp_occurrences

                    # scenario prop_three
                    tmp_occurrences = \
                        scenario_prop_three_detection. \
                            scenario_prop_three_occurrences({"where": where_part["expression"]["args"]}, look_for, bound_variables)
                    filter_statistical_information["metadata_found_in_scenarios"]["prop_three"] += tmp_occurrences
                    current_datatype_dict["prop_three"] += tmp_occurrences

                    # scenario prop_two
                    tmp_occurrences = \
                        scenario_prop_two_detection. \
                            scenario_prop_two_occurrences({"where": where_part["expression"]["args"]}, look_for, bound_variables)
                    filter_statistical_information["metadata_found_in_scenarios"]["prop_two"] += tmp_occurrences
                    current_datatype_dict["prop_two"] += tmp_occurrences

                    # scenario prop_four
                    tmp_occurrences = \
                        scenario_prop_four_detection. \
                            scenario_prop_four_occurrences({"where": where_part["expression"]["args"]}, look_for, bound_variables)
                    filter_statistical_information["metadata_found_in_scenarios"]["prop_four"] += tmp_occurrences
                    current_datatype_dict["prop_four"] += tmp_occurrences

                    # scenario obj_one
                    tmp_occurrences = \
                        scenario_obj_one_detection. \
                            scenario_obj_one_occurrences({"where": where_part["expression"]["args"]}, look_for, bound_variables)
                    filter_statistical_information["metadata_found_in_scenarios"]["obj_one"] += tmp_occurrences
                    current_datatype_dict["obj_one"] += tmp_occurrences

                    # scenario obj_two
                    tmp_occurrences = \
                        scenario_obj_two_detection. \
                            scenario_obj_two_occurrences({"where": where_part["expression"]["args"]}, look_for, bound_variables)
                    filter_statistical_information["metadata_found_in_scenarios"]["obj_two"] += tmp_occurrences
                    current_datatype_dict["obj_two"] += tmp_occurrences


                    # scenario obj_three
                    tmp_occurrences = \
                        scenario_obj_three_detection. \
                            scenario_obj_three_occurrences({"where": where_part["expression"]["args"]}, look_for, bound_variables)
                    filter_statistical_information["metadata_found_in_scenarios"]["obj_three"] += tmp_occurrences
                    current_datatype_dict["obj_three"] += tmp_occurrences


                    # scenario obj_four
                    tmp_occurrences = \
                        scenario_obj_four_detection. \
                            scenario_obj_four_occurrences({"where": where_part["expression"]["args"]}, look_for, bound_variables)
                    filter_statistical_information["metadata_found_in_scenarios"]["obj_four"] += tmp_occurrences
                    current_datatype_dict["obj_four"] += tmp_occurrences


                    # scenario sub_one
                    tmp_occurrences = \
                        scenario_sub_one_detection. \
                            scenario_sub_one_occurrences({"where": where_part["expression"]["args"]}, look_for, bound_variables)
                    filter_statistical_information["metadata_found_in_scenarios"]["sub_one"] += tmp_occurrences
                    current_datatype_dict["sub_one"] += tmp_occurrences


                    # scenario sub_two
                    tmp_occurrences = \
                        scenario_sub_two_detection. \
                            scenario_sub_two_occurrences({"where": where_part["expression"]["args"]}, look_for, bound_variables)
                    filter_statistical_information["metadata_found_in_scenarios"]["sub_two"] += tmp_occurrences
                    current_datatype_dict["sub_two"] += tmp_occurrences


                    # scenario sub_three
                    tmp_occurrences = \
                        scenario_sub_three_detection. \
                            scenario_sub_three_occurrences({"where": where_part["expression"]["args"]}, look_for, bound_variables)
                    filter_statistical_information["metadata_found_in_scenarios"]["sub_three"] += tmp_occurrences
                    current_datatype_dict["sub_three"] += tmp_occurrences


                    # scenario sub_four
                    tmp_occurrences = \
                        scenario_sub_four_detection. \
                            scenario_sub_four_occurrences({"where": where_part["expression"]["args"]}, look_for, bound_variables)
                    filter_statistical_information["metadata_found_in_scenarios"]["sub_four"] += tmp_occurrences
                    current_datatype_dict["sub_four"] += tmp_occurrences


                    # scenario bind
                    # if a variable is RE-USED in another BIND - but in this case, do not go deeper into the tree
                    #
                    # Do not look for another RE-USE of this new variable in a BIND.
                    tmp_occurrences = \
                        scenario_bind_detection. \
                            scenario_bind_occurrences({"where": where_part["expression"]["args"]}, look_for,
                                                      location, bound_variables, False, data_type)
                    filter_statistical_information["metadata_found_in_scenarios"]["bind"] += tmp_occurrences
                    current_datatype_dict["bind"] += tmp_occurrences



                    # scenario blank_mode
                    tmp_occurrences = \
                        scenario_blank_node_detection. \
                            scenario_blank_node_occurrences({"where": where_part["expression"]["args"]}, look_for,
                                                            bound_variables)
                    filter_statistical_information["metadata_found_in_scenarios"]["blank_node"] += tmp_occurrences
                    current_datatype_dict["blank_node"] += tmp_occurrences


                    # if RE-USED in another FILTER - but in this case, do not go deeper into the tree
                    #
                    # Do not look for another RE-USE in a FILTER.


                    # scenario filter
                    tmp_occurrences = \
                        scenario_filter_detection. \
                            scenario_filter_occurrences({"where": where_part["expression"]["args"]}, look_for, location,
                                                       bound_variables, False, data_type)
                    filter_statistical_information["metadata_found_in_scenarios"]["filter"] += tmp_occurrences
                    current_datatype_dict["filter"] += tmp_occurrences



                    # scenario group
                    # check, if there are some group term types left
                    check_for_still_existing_group = \
                        scenario_group_detection. \
                            scenario_group_occurrences({"where": where_part["expression"]["args"]}, look_for, bound_variables)
                    if check_for_still_existing_group > 0:
                        raise Exception



                    # scenario literal
                    tmp_occurrences = \
                        scenario_literal_detection. \
                            scenario_literal_occurrences({"where": where_part["expression"]["args"]}, look_for, bound_variables)
                    filter_statistical_information["metadata_found_in_scenarios"]["literal"] += tmp_occurrences
                    current_datatype_dict["literal"] += tmp_occurrences



                    # if RE-USED in another MINUS - but in this case, do not go deeper into the tree
                    #
                    # Do not look for another RE-USE in a MINUS.
                    # scenario minus
                    tmp_occurrences = \
                        scenario_minus_detection. \
                            scenario_minus_occurrences({"where": where_part["expression"]["args"]}, look_for, location,
                                                       bound_variables, False, data_type)
                    filter_statistical_information["metadata_found_in_scenarios"]["minus"] += tmp_occurrences
                    current_datatype_dict["minus"] += tmp_occurrences



                    # if RE-USED in another OPTIONAL - but in this case, do not go deeper into the tree
                    #
                    # Do not look for another RE-USE in a OPTIONAL.
                    # scenario optional
                    tmp_occurrences = \
                        scenario_optional_detection. \
                            scenario_optional_occurrences({"where": where_part["expression"]["args"]}, look_for, location,
                                                        bound_variables, False, data_type)
                    filter_statistical_information["metadata_found_in_scenarios"]["optional"] += tmp_occurrences
                    current_datatype_dict["optional"] += tmp_occurrences



                    # scenario prop_path
                    tmp_occurrences = \
                        scenario_prop_path_detection. \
                            scenario_prop_path_occurrences({"where": where_part["expression"]["args"]}, look_for, location,
                                                       bound_variables, False, data_type)
                    filter_statistical_information["metadata_found_in_scenarios"]["prop_path"] += tmp_occurrences
                    current_datatype_dict["prop_path"] += tmp_occurrences



                    # scenario service
                    tmp_occurrences = \
                        scenario_service_detection. \
                            scenario_service_occurrences({"where": where_part["expression"]["args"]}, look_for, bound_variables)
                    filter_statistical_information["metadata_found_in_scenarios"]["service"] += tmp_occurrences
                    current_datatype_dict["service"] += tmp_occurrences



                    # if RE-USED in another SUBSELECT - but in this case, do not go deeper into the tree
                    #
                    # Do not look for another RE-USE in a SUBSELECT.
                    # scenario subselect
                    tmp_occurrences = \
                        scenario_subselect_detection. \
                            scenario_subselect_occurrences({"where": where_part["expression"]["args"]}, look_for,
                                                           location,
                                                           bound_variables, False, data_type)
                    filter_statistical_information["metadata_found_in_scenarios"]["subselect"] += tmp_occurrences
                    current_datatype_dict["subselect"] += tmp_occurrences



                    # if RE-USED in another UNION - but in this case, do not go deeper into the tree
                    #
                    # Do not look for another RE-USE in a UNION.
                    # scenario union
                    tmp_occurrences = \
                        scenario_union_detection. \
                            scenario_union_occurrences({"where": where_part["expression"]["args"]}, look_for, location,
                                                       bound_variables, False, data_type)
                    filter_statistical_information["metadata_found_in_scenarios"]["union"] += tmp_occurrences
                    current_datatype_dict["union"] += tmp_occurrences



                    # scenario values
                    tmp_occurrences = \
                        scenario_values_detection. \
                            scenario_values_occurrences({"where": where_part["expression"]["args"]}, look_for, bound_variables)
                    filter_statistical_information["metadata_found_in_scenarios"]["values"] += tmp_occurrences
                    current_datatype_dict["values"] += tmp_occurrences



                    # if the variable could not be found in the patterns of the FILTER
                    if filter_statistical_information["metadata_found_in_scenarios"] == tmp_dict:
                        # could be more than one
                        filter_statistical_information["metadata_found_in_scenarios"]["not_found_in_patterns"] += \
                            str({"where": where_part["expression"]["args"]}).count(look_for)
                        current_datatype_dict["not_found_in_patterns"] += \
                            str(where_part["expression"]["args"]).count(look_for)




                    # also -> detect the operator of the FILTER!
                    #
                    # e.g. EXISTS / NON-EXISTS

                    if where_part["expression"]["operator"] in filter_statistical_information["found_operators_overall"]:
                        filter_statistical_information["found_operators_overall"][where_part["expression"]["operator"]] += 1

                    else:
                        filter_statistical_information["found_operators_overall"][where_part["expression"]["operator"]] = 1

                    filter_statistical_information["total_found_operators"] += 1

                    if data_type in filter_statistical_information["found_operators_per_datatype"]:
                        if where_part["expression"]["operator"] in \
                                filter_statistical_information["found_operators_per_datatype"][data_type]:
                            filter_statistical_information["found_operators_per_datatype"][data_type]\
                                [where_part["expression"]["operator"]] += 1
                        else:
                            filter_statistical_information["found_operators_per_datatype"][data_type]\
                                [where_part["expression"]["operator"]] = 1
                    else:
                        filter_statistical_information["found_operators_per_datatype"][data_type] = {}
                        filter_statistical_information["found_operators_per_datatype"][data_type]\
                            [where_part["expression"]["operator"]] = 1



                    # save the json object
                    with open(location + "/filter_statistical_information.json", "w") as json_data:
                        json.dump(filter_statistical_information, json_data)
                        json_data.close()
                        # print(filter_statistical_information)


    return result


def delete_and_join_all_GROUP_patterns_to_the_overall_FILTER_patterns(group_type):
    # recursive fun
    group_was_found = False

    patterns = group_type["expression"]["args"]

    for pattern in patterns:
        # there can also be just a "termType", e.g. on "=" filters
        if "type" in pattern:
            if pattern["type"] == "group":
                group_type["expression"]["args"].remove(pattern)
                group_type["expression"]["args"] = \
                    group_type["expression"]["args"] + pattern["patterns"]
                group_was_found = True

    if group_was_found:
        # recursion start
        delete_and_join_all_GROUP_patterns_to_the_overall_FILTER_patterns(group_type)
    else:
        # recursion stop
        return