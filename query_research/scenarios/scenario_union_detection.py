# method to detect scenario union
#
#
#
# constellation for "wasDerivedFrom"
#
# scenario filter:
# { ?s prov:wasDerivedFrom ?o . }
# UNION
# { ?s2 prov:wasDerivedFrom ?o2 . }
#
# ---> will in the additional layer be two scenario ones
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

def scenario_union_occurrences(json_object, look_for, location, bound_variables, look_for_additional_layer):
    # 'location' is the path to the current 'scenarios' folder
    # -> for the statistical information, in which scenarios the found
    #       metadata are on the 'additional layer'

    where = json_object["where"]

    # find scenarios 'union'

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:
        if where_part["type"] == "union":
            if (look_for not in str(where_part["patterns"])):
                if look_for in str(where_part):
                    raise Exception
            else:
                # there may be more than one
                result += str(where_part["patterns"]).count(look_for)

                # if a UNION scenario is detected -> look one step deeper, which scenario is used INSIDE the UNION
                #
                # also delete any GROUP, that might be used and join the content to the patterns of the UNION

                delete_and_join_all_GROUP_patterns_to_the_overall_UNION_patterns(where_part)

                # -> detect the scenario, the found metadata is in
                # but ONLY do that, if the 'look_for_aditional_layer boolean is set to true
                # (to prevent re-iteration)
                if look_for_additional_layer:

                    # look, if there already exists a 'union_scenarios_information'
                    if os.path.isfile(location + "/union_statistical_information.json"):
                        with open(location + "/union_statistical_information.json", "r") as json_data:
                            union_statistical_information = json.load(json_data)
                            json_data.close()
                    else:
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

                        union_statistical_information = \
                            {
                                "total_found_metadata": 0,
                                "metadata_found_in_scenarios": scenarios_dict}


                    union_statistical_information["total_found_metadata"] += \
                        str(where_part["patterns"]).count(look_for)
                    # detect the scenario on the 'additional' layer

                    tmp_dict = union_statistical_information["metadata_found_in_scenarios"].copy()

                    # scenario one
                    union_statistical_information["metadata_found_in_scenarios"]["one"] += \
                        scenario_one_detection. \
                            scenario_one_occurrences({"where": where_part["patterns"]}, look_for, bound_variables)
                    # scenario two
                    union_statistical_information["metadata_found_in_scenarios"]["two"] += \
                        scenario_two_detection. \
                            scenario_two_occurrences({"where": where_part["patterns"]}, look_for, bound_variables)
                    # scenario three
                    union_statistical_information["metadata_found_in_scenarios"]["three"] += \
                        scenario_three_detection. \
                            scenario_three_occurrences({"where": where_part["patterns"]}, look_for, bound_variables)
                    # scenario four
                    union_statistical_information["metadata_found_in_scenarios"]["four"] += \
                        scenario_four_detection. \
                            scenario_four_occurrences({"where": where_part["patterns"]}, look_for, bound_variables)
                    # scenario five
                    union_statistical_information["metadata_found_in_scenarios"]["five"] += \
                        scenario_five_detection. \
                            scenario_five_occurrences({"where": where_part["patterns"]}, look_for, bound_variables)
                    # scenario six
                    union_statistical_information["metadata_found_in_scenarios"]["six"] += \
                        scenario_six_detection. \
                            scenario_six_occurrences({"where": where_part["patterns"]}, look_for, bound_variables)
                    # scenario seven
                    union_statistical_information["metadata_found_in_scenarios"]["seven"] += \
                        scenario_seven_detection. \
                            scenario_seven_occurrences({"where": where_part["patterns"]}, look_for, bound_variables)
                    # scenario eight
                    union_statistical_information["metadata_found_in_scenarios"]["eight"] += \
                        scenario_eight_detection. \
                            scenario_eight_occurrences({"where": where_part["patterns"]}, look_for, bound_variables)
                    # scenario nine
                    union_statistical_information["metadata_found_in_scenarios"]["nine"] += \
                        scenario_nine_detection. \
                            scenario_nine_occurrences({"where": where_part["patterns"]}, look_for, bound_variables)
                    # scenario tne
                    union_statistical_information["metadata_found_in_scenarios"]["ten"] += \
                        scenario_ten_detection. \
                            scenario_ten_occurrences({"where": where_part["patterns"]}, look_for, bound_variables)
                    # scenario eleven
                    union_statistical_information["metadata_found_in_scenarios"]["eleven"] += \
                        scenario_eleven_detection. \
                            scenario_eleven_occurrences({"where": where_part["patterns"]}, look_for, bound_variables)
                    # scenario twelve
                    union_statistical_information["metadata_found_in_scenarios"]["twelve"] += \
                        scenario_twelve_detection. \
                            scenario_twelve_occurrences({"where":where_part["patterns"]}, look_for, bound_variables)

                    # scenario bind
                    # if a variable is RE-USED in another BIND - but in this case, do not go deeper into the tree
                    #
                    # Do not look for another RE-USE of this new variable in a BIND.
                    union_statistical_information["metadata_found_in_scenarios"]["bind"] += \
                        scenario_bind_detection. \
                            scenario_bind_occurrences({"where": where_part["patterns"]}, look_for,
                                                      location, bound_variables, False)

                    # scenario blank_mode
                    union_statistical_information["metadata_found_in_scenarios"]["blank_node"] += \
                        scenario_blank_node_detection. \
                            scenario_blank_node_occurrences({"where": where_part["patterns"]}, look_for, bound_variables)
                    # scenario filter
                    union_statistical_information["metadata_found_in_scenarios"]["filter"] += \
                        scenario_filter_detection. \
                            scenario_filter_occurrences({"where": where_part["patterns"]}, look_for, bound_variables)

                    # scenario group
                    # check, if there are some group term types left
                    check_for_still_existing_group = \
                        scenario_group_detection. \
                            scenario_group_occurrences({"where": where_part["patterns"]}, look_for, bound_variables)
                    if check_for_still_existing_group > 0:
                        raise Exception

                    # scenario literal
                    union_statistical_information["metadata_found_in_scenarios"]["literal"] += \
                        scenario_literal_detection. \
                            scenario_literal_occurrences({"where": where_part["patterns"]}, look_for, bound_variables)


                    # if RE-USED in another MINUS - but in this case, do not go deeper into the tree
                    #
                    # Do not look for another RE-USE in a MINUS.
                    # scenario minus
                    union_statistical_information["metadata_found_in_scenarios"]["union"] += \
                        scenario_minus_detection. \
                            scenario_minus_occurrences({"where": where_part["patterns"]}, look_for, location,
                                                       bound_variables, False)


                    # scenario optional
                    union_statistical_information["metadata_found_in_scenarios"]["optional"] += \
                        scenario_optional_detection. \
                            scenario_optional_occurrences({"where": where_part["patterns"]}, look_for, bound_variables)
                    # scenario prop_path
                    union_statistical_information["metadata_found_in_scenarios"]["prop_path"] += \
                        scenario_prop_path_detection. \
                            scenario_prop_path_occurrences({"where": where_part["patterns"]}, look_for, bound_variables)
                    # scenario service
                    union_statistical_information["metadata_found_in_scenarios"]["service"] += \
                        scenario_service_detection. \
                            scenario_service_occurrences({"where": where_part["patterns"]}, look_for, bound_variables)
                    # scenario subselect
                    union_statistical_information["metadata_found_in_scenarios"]["subselect"] += \
                        scenario_subselect_detection. \
                            scenario_subselect_occurrences({"where": where_part["patterns"]}, look_for, bound_variables)

                    # if RE-USED in another UNION - but in this case, do not go deeper into the tree
                    #
                    # Do not look for another RE-USE in a UNION.
                    # scenario union
                    union_statistical_information["metadata_found_in_scenarios"]["union"] += \
                        scenario_union_detection. \
                            scenario_union_occurrences({"where": where_part["patterns"]}, look_for, location,
                                                       bound_variables, False)


                    # scenario values
                    union_statistical_information["metadata_found_in_scenarios"]["values"] += \
                        scenario_values_detection. \
                            scenario_values_occurrences({"where": where_part["patterns"]}, look_for, bound_variables)

                    # if the variable could not be found in the patterns of the UNION
                    if union_statistical_information["metadata_found_in_scenarios"] == tmp_dict:
                        union_statistical_information["metadata_found_in_scenarios"]["not_found_in_patterns"] += 1

                    # save the json object
                    with open(location + "/union_statistical_information.json", "w") as json_data:
                        json.dump(union_statistical_information, json_data)
                        json_data.close()
                        # print(union_statistical_information)

    return result

def delete_and_join_all_GROUP_patterns_to_the_overall_UNION_patterns(group_type):
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
        delete_and_join_all_GROUP_patterns_to_the_overall_UNION_patterns(group_type)
    else:
        # recursion stop
        return