# method to detect scenario optional
#
#
#
# constellation for "wasDerivedFrom"
#
# scenario filter:
# OPTIONAL( ?s prov:wasDerivedFrom ?o . ) .
#
#
#
# look_for e.g. "http://www.w3.org/ns/prov#wasDerivedFrom"

import query_research.scenarios.scenario_1_detection as scenario_one_detection
import query_research.scenarios.scenario_2_detection as scenario_two_detection
import query_research.scenarios.scenario_3_detection as scenario_three_detection
import query_research.scenarios.scenario_4_detection as scenario_four_detection

import query_research.scenarios.scenario_5_detection as scenario_five_detection
import query_research.scenarios.scenario_6_detection as scenario_six_detection
import query_research.scenarios.scenario_7_detection as scenario_seven_detection
import query_research.scenarios.scenario_8_detection as scenario_eight_detection

import query_research.scenarios.scenario_9_detection as scenario_nine_detection
import query_research.scenarios.scenario_10_detection as scenario_ten_detection
import query_research.scenarios.scenario_11_detection as scenario_eleven_detection
import query_research.scenarios.scenario_12_detection as scenario_twelve_detection

import query_research.scenarios.scenario_filter_detection as scenario_filter_detection
import query_research.scenarios.scenario_optional_detection as scenario_optional_detection
import query_research.scenarios.scenario_union_detection as scenario_union_detection
import query_research.scenarios.scenario_prop_path_detection as scenario_prop_path_detection
import query_research.scenarios.scenario_group_detection as scenario_group_detection
import query_research.scenarios.scenario_bind_detection as scenario_bind_detection
import query_research.scenarios.scenario_blank_node_detection as scenario_blank_node_detection
import query_research.scenarios.scenario_minus_detection as scenario_minus_detection
import query_research.scenarios.scenario_subselect_detection as scenario_subselect_detection
import query_research.scenarios.scenario_ref_value_detection as scenario_ref_value_detection
import query_research.scenarios.scenario_literal_detection as scenario_literal_detection
import query_research.scenarios.scenario_values_detection as scenario_values_detection
import query_research.scenarios.scenario_service_detection as scenario_service_detection

import json
import os

def scenario_optional_occurrences(json_object, look_for, location, bound_variables, look_for_additional_layer, data_type):
    # 'location' is the path to the current 'scenarios' folder
    # -> for the statistical information, in which scenarios the found
    #       metadata are on the 'additional layer', i.e., which are inside th minus
    where = json_object["where"]

    # find scenarios 'optional'

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:
        if "type" in where_part and where_part["type"] == "optional":
            if look_for not in str(where_part["patterns"]):
                if look_for in str(where_part):
                    raise Exception
            else:
                # there may be more than one
                result += str(where_part["patterns"]).count(look_for)

                # if a OPTIONAL scenario is detected -> look one step deeper, which scenario is used INSIDE the OPTIONAL
                #
                # also delete any GROUP, that might be used and join the content to the patterns of the OPTIONAL

                delete_and_join_all_GROUP_patterns_to_the_overall_OPTIONAL_patterns(where_part)

                # -> detect the scenario, the found metadata is in
                # but ONLY do that, if the 'look_for_aditional_layer boolean is set to true
                # (to prevent re-iteration)
                if look_for_additional_layer:

                    # dict structure for the counted scenarios
                    scenarios_dict = \
                        {
                            "one": 0,
                            "two": 0,
                            "three": 0,
                            "four": 0,
                            "five": 0,
                            "six": 0,
                            "seven": 0,
                            "eight": 0,
                            "nine": 0,
                            "ten": 0,
                            "eleven": 0,
                            "twelve": 0,
                            "filter": 0,
                            "optional": 0,
                            "union": 0,
                            "prop_path": 0,
                            "bind": 0,
                            "blank_node": 0,
                            "minus": 0,
                            "subselect": 0,
                            "ref_value": 0,
                            "literal": 0,
                            "values": 0,
                            "service": 0,
                            "not_found_in_patterns": 0}

                    # look, if there already exists a 'optional_scenarios_information'
                    if os.path.isfile(location + "/optional_statistical_information.json"):
                        with open(location + "/optional_statistical_information.json", "r") as json_data:
                            optional_statistical_information = json.load(json_data)
                            json_data.close()
                    else:

                        optional_statistical_information = \
                            {
                                "total_found_metadata": 0,
                                "metadata_found_in_scenarios": scenarios_dict,
                                "metadata_per_datatype_found_in_scenarios": {}}

                    # check for the datatypes
                    # or/and get the correct scenario dict for the current datatype
                    already_inserted = False
                    for test_dict_datatype in optional_statistical_information["metadata_per_datatype_found_in_scenarios"]:
                        if test_dict_datatype == data_type:
                            already_inserted = True

                            current_datatype_dict = optional_statistical_information[
                                "metadata_per_datatype_found_in_scenarios"][data_type]

                    if not already_inserted:
                        scenarios_dict_datatype = scenarios_dict.copy()
                        optional_statistical_information["metadata_per_datatype_found_in_scenarios"][data_type] = \
                            scenarios_dict_datatype

                        current_datatype_dict = scenarios_dict_datatype
                        
                    optional_statistical_information["total_found_metadata"] += \
                        str(where_part["patterns"]).count(look_for)

                    # detect the scenario on the 'additional' layer

                    tmp_dict = optional_statistical_information["metadata_found_in_scenarios"].copy()

                    # scenario one
                    tmp_occurrences = \
                        scenario_one_detection. \
                            scenario_one_occurrences({"where": where_part["patterns"]}, look_for,
                                                     bound_variables)
                    optional_statistical_information["metadata_found_in_scenarios"]["one"] += tmp_occurrences
                    current_datatype_dict["one"] += tmp_occurrences

                    # scenario two
                    tmp_occurrences = \
                        scenario_two_detection. \
                            scenario_two_occurrences({"where": where_part["patterns"]}, look_for,
                                                     bound_variables)
                    optional_statistical_information["metadata_found_in_scenarios"]["two"] += tmp_occurrences
                    current_datatype_dict["two"] += tmp_occurrences

                    # scenario three
                    tmp_occurrences = \
                        scenario_three_detection. \
                            scenario_three_occurrences({"where": where_part["patterns"]}, look_for,
                                                       bound_variables)
                    optional_statistical_information["metadata_found_in_scenarios"]["three"] += tmp_occurrences
                    current_datatype_dict["three"] += tmp_occurrences

                    # scenario four
                    tmp_occurrences = \
                        scenario_four_detection. \
                            scenario_four_occurrences({"where": where_part["patterns"]}, look_for,
                                                      bound_variables)
                    optional_statistical_information["metadata_found_in_scenarios"]["four"] += tmp_occurrences
                    current_datatype_dict["four"] += tmp_occurrences

                    # scenario five
                    tmp_occurrences = \
                        scenario_five_detection. \
                            scenario_five_occurrences({"where": where_part["patterns"]}, look_for,
                                                      bound_variables)
                    optional_statistical_information["metadata_found_in_scenarios"]["five"] += tmp_occurrences
                    current_datatype_dict["five"] += tmp_occurrences

                    # scenario six
                    tmp_occurrences = \
                        scenario_six_detection. \
                            scenario_six_occurrences({"where": where_part["patterns"]}, look_for,
                                                     bound_variables)
                    optional_statistical_information["metadata_found_in_scenarios"]["six"] += tmp_occurrences
                    current_datatype_dict["six"] += tmp_occurrences

                    # scenario seven
                    tmp_occurrences = \
                        scenario_seven_detection. \
                            scenario_seven_occurrences({"where": where_part["patterns"]}, look_for,
                                                       bound_variables)
                    optional_statistical_information["metadata_found_in_scenarios"]["seven"] += tmp_occurrences
                    current_datatype_dict["seven"] += tmp_occurrences

                    # scenario eight
                    tmp_occurrences = \
                        scenario_eight_detection. \
                            scenario_eight_occurrences({"where": where_part["patterns"]}, look_for,
                                                       bound_variables)
                    optional_statistical_information["metadata_found_in_scenarios"]["eight"] += tmp_occurrences
                    current_datatype_dict["eight"] += tmp_occurrences

                    # scenario nine
                    tmp_occurrences = \
                        scenario_nine_detection. \
                            scenario_nine_occurrences({"where": where_part["patterns"]}, look_for,
                                                      bound_variables)
                    optional_statistical_information["metadata_found_in_scenarios"]["nine"] += tmp_occurrences
                    current_datatype_dict["nine"] += tmp_occurrences

                    # scenario tne
                    tmp_occurrences = \
                        scenario_ten_detection. \
                            scenario_ten_occurrences({"where": where_part["patterns"]}, look_for,
                                                     bound_variables)
                    optional_statistical_information["metadata_found_in_scenarios"]["ten"] += tmp_occurrences
                    current_datatype_dict["ten"] += tmp_occurrences

                    # scenario eleven
                    tmp_occurrences = \
                        scenario_eleven_detection. \
                            scenario_eleven_occurrences({"where": where_part["patterns"]}, look_for,
                                                        bound_variables)
                    optional_statistical_information["metadata_found_in_scenarios"]["eleven"] += tmp_occurrences
                    current_datatype_dict["eleven"] += tmp_occurrences

                    # scenario twelve
                    tmp_occurrences = \
                        scenario_twelve_detection. \
                            scenario_twelve_occurrences({"where": where_part["patterns"]}, look_for,
                                                        bound_variables)
                    optional_statistical_information["metadata_found_in_scenarios"]["twelve"] += tmp_occurrences
                    current_datatype_dict["twelve"] += tmp_occurrences

                    # scenario bind
                    # if a variable is RE-USED in another BIND - but in this case, do not go deeper into the tree
                    #
                    # Do not look for another RE-USE of this new variable in a BIND.
                    tmp_occurrences = \
                        scenario_bind_detection. \
                            scenario_bind_occurrences({"where": where_part["patterns"]}, look_for,
                                                      location, bound_variables, False, data_type)
                    optional_statistical_information["metadata_found_in_scenarios"]["bind"] += tmp_occurrences
                    current_datatype_dict["bind"] += tmp_occurrences

                    # scenario blank_mode
                    tmp_occurrences = \
                        scenario_blank_node_detection. \
                            scenario_blank_node_occurrences({"where": where_part["patterns"]}, look_for,
                                                            bound_variables)
                    optional_statistical_information["metadata_found_in_scenarios"]["blank_node"] += tmp_occurrences
                    current_datatype_dict["blank_node"] += tmp_occurrences

                    # if RE-USED in another FILTER - but in this case, do not go deeper into the tree
                    #
                    # Do not look for another RE-USE in a FILTER.

                    # scenario filter
                    tmp_occurrences = \
                        scenario_filter_detection. \
                            scenario_filter_occurrences({"where": where_part["patterns"]}, look_for, location,
                                                        bound_variables, False, data_type)
                    optional_statistical_information["metadata_found_in_scenarios"]["filter"] += tmp_occurrences
                    current_datatype_dict["filter"] += tmp_occurrences

                    # scenario group
                    # check, if there are some group term types left
                    check_for_still_existing_group = \
                        scenario_group_detection. \
                            scenario_group_occurrences({"where": where_part["patterns"]}, look_for,
                                                       bound_variables)
                    if check_for_still_existing_group > 0:
                        raise Exception

                    # scenario literal
                    tmp_occurrences = \
                        scenario_literal_detection. \
                            scenario_literal_occurrences({"where": where_part["patterns"]}, look_for,
                                                         bound_variables)
                    optional_statistical_information["metadata_found_in_scenarios"]["literal"] += tmp_occurrences
                    current_datatype_dict["literal"] += tmp_occurrences

                    # if RE-USED in another MINUS - but in this case, do not go deeper into the tree
                    #
                    # Do not look for another RE-USE in a MINUS.
                    # scenario minus
                    tmp_occurrences = \
                        scenario_minus_detection. \
                            scenario_minus_occurrences({"where": where_part["patterns"]}, look_for, location,
                                                       bound_variables, False, data_type)
                    optional_statistical_information["metadata_found_in_scenarios"]["minus"] += tmp_occurrences
                    current_datatype_dict["minus"] += tmp_occurrences

                    # if RE-USED in another OPTIONAL - but in this case, do not go deeper into the tree
                    #
                    # Do not look for another RE-USE in a OPTIONAL.
                    # scenario optional
                    tmp_occurrences = \
                        scenario_optional_detection. \
                            scenario_optional_occurrences({"where": where_part["patterns"]}, look_for,
                                                          location,
                                                          bound_variables, False, data_type)
                    optional_statistical_information["metadata_found_in_scenarios"]["optional"] += tmp_occurrences
                    current_datatype_dict["optional"] += tmp_occurrences

                    # scenario prop_path
                    tmp_occurrences = \
                        scenario_prop_path_detection. \
                            scenario_prop_path_occurrences({"where": where_part["patterns"]}, look_for,
                                                           location,
                                                           bound_variables, False, data_type)
                    optional_statistical_information["metadata_found_in_scenarios"]["prop_path"] += tmp_occurrences
                    current_datatype_dict["prop_path"] += tmp_occurrences

                    # scenario service
                    tmp_occurrences = \
                        scenario_service_detection. \
                            scenario_service_occurrences({"where": where_part["patterns"]}, look_for,
                                                         bound_variables)
                    optional_statistical_information["metadata_found_in_scenarios"]["service"] += tmp_occurrences
                    current_datatype_dict["service"] += tmp_occurrences

                    # if RE-USED in another SUBSELECT - but in this case, do not go deeper into the tree
                    #
                    # Do not look for another RE-USE in a SUBSELECT.
                    # scenario subselect
                    tmp_occurrences = \
                        scenario_subselect_detection. \
                            scenario_subselect_occurrences({"where": where_part["patterns"]}, look_for,
                                                           location,
                                                           bound_variables, False, data_type)
                    optional_statistical_information["metadata_found_in_scenarios"]["subselect"] += tmp_occurrences
                    current_datatype_dict["subselect"] += tmp_occurrences

                    # if RE-USED in another UNION - but in this case, do not go deeper into the tree
                    #
                    # Do not look for another RE-USE in a UNION.
                    # scenario union
                    tmp_occurrences = \
                        scenario_union_detection. \
                            scenario_union_occurrences({"where": where_part["patterns"]}, look_for, location,
                                                       bound_variables, False, data_type)
                    optional_statistical_information["metadata_found_in_scenarios"]["union"] += tmp_occurrences
                    current_datatype_dict["union"] += tmp_occurrences

                    # scenario values
                    tmp_occurrences = \
                        scenario_values_detection. \
                            scenario_values_occurrences({"where": where_part["patterns"]}, look_for,
                                                        bound_variables)
                    optional_statistical_information["metadata_found_in_scenarios"]["values"] += tmp_occurrences
                    current_datatype_dict["values"] += tmp_occurrences

                    # if the variable could not be found in the patterns of the OPTIONAL
                    if optional_statistical_information["metadata_found_in_scenarios"] == tmp_dict:
                        optional_statistical_information["metadata_found_in_scenarios"]["not_found_in_patterns"] += \
                            str(where_part["patterns"]).count(look_for)
                        current_datatype_dict["not_found_in_patterns"] += \
                            str(where_part["patterns"]).count(look_for)

                    # save the json object
                    with open(location + "/optional_statistical_information.json", "w") as json_data:
                        json.dump(optional_statistical_information, json_data)
                        json_data.close()
                        # print(optional_statistical_information)


    return result


def delete_and_join_all_GROUP_patterns_to_the_overall_OPTIONAL_patterns(group_type):
    # recursive fun
    group_was_found = False

    patterns = group_type["patterns"]

    for pattern in patterns:
        if pattern["type"] == "group":
            group_type["patterns"].remove(pattern)
            group_type["patterns"] = group_type["patterns"] + pattern["patterns"]
            group_was_found = True

    if group_was_found:
        # recursion start
        delete_and_join_all_GROUP_patterns_to_the_overall_OPTIONAL_patterns(group_type)
    else:
        # recursion stop
        return