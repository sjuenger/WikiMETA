# method to detect scenario subselect
#
#
#
# constellation for "wasDerivedFrom"
#
# scenario subselect:
# SELECT ?var1 ( COUNT ( ?var1  ) AS  ?var2  )
# WHERE {
#  SELECT DISTINCT ?var3  ?var1
#  WHERE  {
#    ?var3  <http://www.wikidata.org/prop/direct/P279>  <http://www.wikidata.org/entity/Q7187> ;
#  <http://www.wikidata.org/prop/direct/P703>  <http://www.wikidata.org/entity/Q5> ;
#  ?var1  ?var4 .
#  FILTER (   ( !( REGEX (  STR (  ?var1  ) , "string1" ) ) )
# ) .
#  FILTER (   (  REGEX (  STR (  ?var1  ) , "string2" )  )
# ) .
#  FILTER (   (  NOT EXISTS   {
#     ?var3  ?var1  ?var4 .
#     ?var4  <http://www.w3.org/ns/prov#wasDerivedFrom>  ?var5 .
#   }
#  )
# ) .
#  }
# }
# GROUP BY  ?var1
# ORDER BY  DESC( ?var2 )
#
#
#
# look_for e.g. "http://www.w3.org/ns/prov#wasDerivedFrom"

# PLUS, look for occurrences in the SELECT part of the subquery.

# PLUS, detect the scenario, the found metadata in the sub select is in

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

def scenario_subselect_occurrences(json_object, look_for, location, bound_variables, look_for_additional_layer, data_type):
    # 'location' is the path to the current 'scenarios' folder
    # -> for the statistical information, in which scenarios the found
    #       metadata are on the 'additional layer'

    where = json_object["where"]

    # find scenarios 'subselect'

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:
        if "queryType" in where_part:
            if where_part["queryType"] == "SELECT":
                if look_for not in str(where_part["where"])\
                        and look_for not in str(where_part["variables"]):

                    if look_for in str(where_part):
                        raise Exception
                else:
                    # there may be more than one
                    result += str(where_part["where"]).count(look_for)
                    # also, look in the SELECT part
                    result += str(where_part["variables"]).count(look_for)

                    # if a SUBSELECT scenario is detected -> look one step deeper, 
                    #   which scenario is used INSIDE the SUBSELECT
                    #
                    # also delete any GROUP, that might be used and join the content to the patterns of the SUBSELECT

                    delete_and_join_all_GROUP_patterns_to_the_overall_SUBSELECT_patterns(where_part)

                    # -> detect the scenario, the found metadata is in
                    # but ONLY do that, if the 'look_for_aditional_layer boolean is set to true
                    # (to prevent re-iteration)
                    if look_for_additional_layer:

                        # dict structure for the counted scenarios
                        scenarios_dict = \
                            {
                                "used_in_SELECT": 0,
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

                        # look, if there already exists a 'subselect_scenarios_information'
                        if os.path.isfile(location + "/subselect_statistical_information.json"):
                            with open(location + "/subselect_statistical_information.json", "r") as json_data:
                                subselect_statistical_information = json.load(json_data)
                                json_data.close()
                        else:

                            subselect_statistical_information = \
                                {
                                    "total_found_metadata": 0,
                                    "metadata_found_in_scenarios": scenarios_dict,
                                    "scenarios_found_in_second_level_union": scenarios_dict.copy(),
                                    "metadata_per_datatype_found_in_scenarios": {},
                                    "scenarios_per_datatype_found_in_second_level_union": {}
                                }

                        # check for the datatypes
                        # or/and get the correct scenario dict for the current datatype
                        already_inserted = False
                        for test_dict_datatype in subselect_statistical_information["metadata_per_datatype_found_in_scenarios"]:
                            if test_dict_datatype == data_type:
                                already_inserted = True

                                current_datatype_dict = subselect_statistical_information[
                                    "metadata_per_datatype_found_in_scenarios"][data_type]

                                # look for the current datatype dict for the operators
                                for test_dict_datatype in subselect_statistical_information[
                                    "scenarios_per_datatype_found_in_second_level_union"]:
                                    if test_dict_datatype == data_type:
                                        current_datatype_dict_subselect_layer = subselect_statistical_information[
                                                "scenarios_per_datatype_found_in_second_level_union"][data_type]

                        if not already_inserted:
                            scenarios_dict_datatype = scenarios_dict.copy()

                            subselect_statistical_information["metadata_per_datatype_found_in_scenarios"][data_type] = \
                                scenarios_dict_datatype
                            scenarios_dict_datatype_operator = scenarios_dict_datatype.copy()
                            subselect_statistical_information[
                                "scenarios_per_datatype_found_in_second_level_union"][data_type] = \
                                    scenarios_dict_datatype_operator

                            current_datatype_dict = scenarios_dict_datatype
                            current_datatype_dict_subselect_layer = scenarios_dict_datatype_operator
                            


                        subselect_statistical_information["total_found_metadata"] += \
                            str(where_part["where"]).count(look_for)
                        # detect the scenario on the 'additional' layer

                        tmp_dict = subselect_statistical_information["metadata_found_in_scenarios"].copy()

                        # scenario USED IN SELECT
                        subselect_statistical_information["metadata_found_in_scenarios"]["used_in_SELECT"] += \
                            str(where_part["variables"]).count(look_for)
                        current_datatype_dict["used_in_SELECT"] += str(where_part["variables"]).count(look_for)

                        # scenario prop_one
                        tmp_occurrences = \
                            scenario_prop_one_detection. \
                                scenario_prop_one_occurrences(where_part, look_for,
                                                         bound_variables)
                        subselect_statistical_information["metadata_found_in_scenarios"]["prop_one"] += tmp_occurrences
                        current_datatype_dict["prop_one"] += tmp_occurrences

                        # scenario prop_three
                        tmp_occurrences = \
                            scenario_prop_three_detection. \
                                scenario_prop_three_occurrences(where_part, look_for,
                                                         bound_variables)
                        subselect_statistical_information["metadata_found_in_scenarios"]["prop_three"] += tmp_occurrences
                        current_datatype_dict["prop_three"] += tmp_occurrences

                        # scenario prop_two
                        tmp_occurrences = \
                            scenario_prop_two_detection. \
                                scenario_prop_two_occurrences(where_part, look_for,
                                                           bound_variables)
                        subselect_statistical_information["metadata_found_in_scenarios"]["prop_two"] += tmp_occurrences
                        current_datatype_dict["prop_two"] += tmp_occurrences

                        # scenario prop_four
                        tmp_occurrences = \
                            scenario_prop_four_detection. \
                                scenario_prop_four_occurrences(where_part, look_for,
                                                          bound_variables)
                        subselect_statistical_information["metadata_found_in_scenarios"]["prop_four"] += tmp_occurrences
                        current_datatype_dict["prop_four"] += tmp_occurrences

                        # scenario obj_one
                        tmp_occurrences = \
                            scenario_obj_one_detection. \
                                scenario_obj_one_occurrences(where_part, look_for,
                                                          bound_variables)
                        subselect_statistical_information["metadata_found_in_scenarios"]["obj_one"] += tmp_occurrences
                        current_datatype_dict["obj_one"] += tmp_occurrences

                        # scenario obj_two
                        tmp_occurrences = \
                            scenario_obj_two_detection. \
                                scenario_obj_two_occurrences(where_part, look_for,
                                                         bound_variables)
                        subselect_statistical_information["metadata_found_in_scenarios"]["obj_two"] += tmp_occurrences
                        current_datatype_dict["obj_two"] += tmp_occurrences

                        # scenario obj_three
                        tmp_occurrences = \
                            scenario_obj_three_detection. \
                                scenario_obj_three_occurrences(where_part, look_for,
                                                           bound_variables)
                        subselect_statistical_information["metadata_found_in_scenarios"]["obj_three"] += tmp_occurrences
                        current_datatype_dict["obj_three"] += tmp_occurrences

                        # scenario obj_four
                        tmp_occurrences = \
                            scenario_obj_four_detection. \
                                scenario_obj_four_occurrences(where_part, look_for,
                                                           bound_variables)
                        subselect_statistical_information["metadata_found_in_scenarios"]["obj_four"] += tmp_occurrences
                        current_datatype_dict["obj_four"] += tmp_occurrences

                        # scenario sub_one
                        tmp_occurrences = \
                            scenario_sub_one_detection. \
                                scenario_sub_one_occurrences(where_part, look_for,
                                                          bound_variables)
                        subselect_statistical_information["metadata_found_in_scenarios"]["sub_one"] += tmp_occurrences
                        current_datatype_dict["sub_one"] += tmp_occurrences

                        # scenario sub_two
                        tmp_occurrences = \
                            scenario_sub_two_detection. \
                                scenario_sub_two_occurrences(where_part, look_for,
                                                         bound_variables)
                        subselect_statistical_information["metadata_found_in_scenarios"]["sub_two"] += tmp_occurrences
                        current_datatype_dict["sub_two"] += tmp_occurrences

                        # scenario sub_three
                        tmp_occurrences = \
                            scenario_sub_three_detection. \
                                scenario_sub_three_occurrences(where_part, look_for,
                                                            bound_variables)
                        subselect_statistical_information["metadata_found_in_scenarios"]["sub_three"] += tmp_occurrences
                        current_datatype_dict["sub_three"] += tmp_occurrences

                        # scenario sub_four
                        tmp_occurrences = \
                            scenario_sub_four_detection. \
                                scenario_sub_four_occurrences(where_part, look_for,
                                                            bound_variables)
                        subselect_statistical_information["metadata_found_in_scenarios"]["sub_four"] += tmp_occurrences
                        current_datatype_dict["sub_four"] += tmp_occurrences

                        # scenario bind
                        # if a variable is RE-USED in another BIND - but in this case, do not go deeper into the tree
                        #
                        # Do not look for another RE-USE of this new variable in a BIND.
                        tmp_occurrences = \
                            scenario_bind_detection. \
                                scenario_bind_occurrences(where_part, look_for,
                                                          location, bound_variables, False, data_type)
                        subselect_statistical_information["metadata_found_in_scenarios"]["bind"] += tmp_occurrences
                        current_datatype_dict["bind"] += tmp_occurrences

                        # scenario blank_mode
                        tmp_occurrences = \
                            scenario_blank_node_detection. \
                                scenario_blank_node_occurrences(where_part, look_for,
                                                                bound_variables)
                        subselect_statistical_information["metadata_found_in_scenarios"]["blank_node"] += tmp_occurrences
                        current_datatype_dict["blank_node"] += tmp_occurrences

                        # if RE-USED in another FILTER - but in this case, do not go deeper into the tree
                        #
                        # Do not look for another RE-USE in a FILTER.

                        # scenario filter
                        tmp_occurrences = \
                            scenario_filter_detection. \
                                scenario_filter_occurrences(where_part, look_for,
                                                            location,
                                                            bound_variables, False, data_type)
                        subselect_statistical_information["metadata_found_in_scenarios"]["filter"] += tmp_occurrences
                        current_datatype_dict["filter"] += tmp_occurrences

                        # scenario group
                        # check, if there are some group term types left
                        check_for_still_existing_group = \
                            scenario_group_detection. \
                                scenario_group_occurrences(where_part, look_for,
                                                           bound_variables)
                        if check_for_still_existing_group > 0:
                            raise Exception

                        # scenario literal
                        tmp_occurrences = \
                            scenario_literal_detection. \
                                scenario_literal_occurrences(where_part, look_for,
                                                             bound_variables)
                        subselect_statistical_information["metadata_found_in_scenarios"]["literal"] += tmp_occurrences
                        current_datatype_dict["literal"] += tmp_occurrences

                        # if RE-USED in another MINUS - but in this case, do not go deeper into the tree
                        #
                        # Do not look for another RE-USE in a MINUS.
                        # scenario minus
                        tmp_occurrences = \
                            scenario_minus_detection. \
                                scenario_minus_occurrences(where_part, look_for,
                                                           location,
                                                           bound_variables, False, data_type)
                        subselect_statistical_information["metadata_found_in_scenarios"]["minus"] += tmp_occurrences
                        current_datatype_dict["minus"] += tmp_occurrences

                        # if RE-USED in another OPTIONAL - but in this case, do not go deeper into the tree
                        #
                        # Do not look for another RE-USE in a OPTIONAL.
                        # scenario optional
                        tmp_occurrences = \
                            scenario_optional_detection. \
                                scenario_optional_occurrences(where_part, look_for,
                                                              location,
                                                              bound_variables, False, data_type)
                        subselect_statistical_information["metadata_found_in_scenarios"]["optional"] += tmp_occurrences
                        current_datatype_dict["optional"] += tmp_occurrences

                        # scenario prop_path
                        tmp_occurrences = \
                            scenario_prop_path_detection. \
                                scenario_prop_path_occurrences(where_part, look_for,
                                                               location,
                                                               bound_variables, False, data_type)
                        subselect_statistical_information["metadata_found_in_scenarios"]["prop_path"] += tmp_occurrences
                        current_datatype_dict["prop_path"] += tmp_occurrences

                        # scenario service
                        tmp_occurrences = \
                            scenario_service_detection. \
                                scenario_service_occurrences(where_part, look_for,
                                                             bound_variables)
                        subselect_statistical_information["metadata_found_in_scenarios"]["service"] += tmp_occurrences
                        current_datatype_dict["service"] += tmp_occurrences

                        # if RE-USED in another SUBSELECT - but in this case, do not go deeper into the tree
                        #
                        # Do not look for another RE-USE in a SUBSELECT.
                        # scenario subselect
                        tmp_occurrences = \
                            scenario_subselect_detection. \
                                scenario_subselect_occurrences(where_part, look_for,
                                                               location,
                                                               bound_variables, False, data_type)
                        subselect_statistical_information["metadata_found_in_scenarios"]["subselect"] += tmp_occurrences
                        current_datatype_dict["subselect"] += tmp_occurrences

                        # if RE-USED in another UNION - but in this case, do not go deeper into the tree
                        #
                        # Do not look for another RE-USE in a UNION.
                        # scenario union
                        tmp_occurrences_union = \
                            scenario_union_detection. \
                                scenario_union_occurrences(where_part, look_for,
                                                           location,
                                                           bound_variables, False, data_type)
                        subselect_statistical_information["metadata_found_in_scenarios"]["union"] += tmp_occurrences_union
                        current_datatype_dict["union"] += tmp_occurrences_union

                        # scenario values
                        tmp_occurrences = \
                            scenario_values_detection. \
                                scenario_values_occurrences(where_part, look_for,
                                                            bound_variables)
                        subselect_statistical_information["metadata_found_in_scenarios"]["values"] += tmp_occurrences
                        current_datatype_dict["values"] += tmp_occurrences

                        # if the variable could not be found in the patterns of the SUBSELECT
                        if subselect_statistical_information["metadata_found_in_scenarios"] == tmp_dict:
                            subselect_statistical_information["metadata_found_in_scenarios"]["not_found_in_patterns"] += \
                            str(where_part).count(look_for)
                            current_datatype_dict["not_found_in_patterns"] += \
                            str(where_part).count(look_for)

                        # -----------------------------------------------------------------------------------------------------------------------
                        #
                        # because the results of this little analysis often show, that ~80% of the found scenarios
                        #   are UNIONs -> detect here also the third layer of scenarios
                        #
                        # -----------------------------------------------------------------------------------------------------------------------

                        # detect the scenario of yet another 'additional' layer to the additional layer,
                        #   but only for the UNION scenarios, e.g. where a UNION was find -> and only
                        #   for the UNION parts in this queries
                        if tmp_occurrences_union > 0:

                            # for every pattern in patterns
                            # multiple bgp (basic graph patterns)
                            for pattern in where_part["where"]:
                                if "type" in pattern:
                                    if pattern["type"] == "union":
                                        if look_for not in str(pattern["patterns"]):

                                            if look_for in str(pattern):
                                                raise Exception
                                        else:

                                            tmp_dict = subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"].copy()
                                            # scenario prop_one
                                            tmp_occurrences = \
                                                scenario_prop_one_detection. \
                                                    scenario_prop_one_occurrences({"where": pattern["patterns"]},
                                                                             look_for, bound_variables)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "prop_one"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["prop_one"] += tmp_occurrences

                                            # scenario prop_three
                                            tmp_occurrences = \
                                                scenario_prop_three_detection. \
                                                    scenario_prop_three_occurrences({"where": pattern["patterns"]},
                                                                             look_for, bound_variables)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "prop_three"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["prop_three"] += tmp_occurrences

                                            # scenario prop_two
                                            tmp_occurrences = \
                                                scenario_prop_two_detection. \
                                                    scenario_prop_two_occurrences({"where": pattern["patterns"]},
                                                                               look_for, bound_variables)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "prop_two"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["prop_two"] += tmp_occurrences

                                            # scenario prop_four
                                            tmp_occurrences = \
                                                scenario_prop_four_detection. \
                                                    scenario_prop_four_occurrences({"where": pattern["patterns"]},
                                                                              look_for, bound_variables)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "prop_four"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["prop_four"] += tmp_occurrences

                                            # scenario obj_one
                                            tmp_occurrences = \
                                                scenario_obj_one_detection. \
                                                    scenario_obj_one_occurrences({"where": pattern["patterns"]},
                                                                              look_for, bound_variables)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "obj_one"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["obj_one"] += tmp_occurrences

                                            # scenario obj_two
                                            tmp_occurrences = \
                                                scenario_obj_two_detection. \
                                                    scenario_obj_two_occurrences({"where": pattern["patterns"]},
                                                                             look_for, bound_variables)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "obj_two"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["obj_two"] += tmp_occurrences

                                            # scenario obj_three
                                            tmp_occurrences = \
                                                scenario_obj_three_detection. \
                                                    scenario_obj_three_occurrences({"where": pattern["patterns"]},
                                                                               look_for, bound_variables)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "obj_three"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["obj_three"] += tmp_occurrences

                                            # scenario obj_four
                                            tmp_occurrences = \
                                                scenario_obj_four_detection. \
                                                    scenario_obj_four_occurrences({"where": pattern["patterns"]},
                                                                               look_for, bound_variables)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "obj_four"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["obj_four"] += tmp_occurrences

                                            # scenario sub_one
                                            tmp_occurrences = \
                                                scenario_sub_one_detection. \
                                                    scenario_sub_one_occurrences({"where": pattern["patterns"]},
                                                                              look_for, bound_variables)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "sub_one"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["sub_one"] += tmp_occurrences

                                            # scenario sub_two
                                            tmp_occurrences = \
                                                scenario_sub_two_detection. \
                                                    scenario_sub_two_occurrences({"where": pattern["patterns"]},
                                                                             look_for, bound_variables)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "sub_two"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["sub_two"] += tmp_occurrences

                                            # scenario sub_three
                                            tmp_occurrences = \
                                                scenario_sub_three_detection. \
                                                    scenario_sub_three_occurrences({"where": pattern["patterns"]},
                                                                                look_for, bound_variables)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "sub_three"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["sub_three"] += tmp_occurrences

                                            # scenario sub_four
                                            tmp_occurrences = \
                                                scenario_sub_four_detection. \
                                                    scenario_sub_four_occurrences({"where": pattern["patterns"]},
                                                                                look_for, bound_variables)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "sub_four"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["sub_four"] += tmp_occurrences

                                            # scenario bind
                                            # if a variable is RE-USED in another BIND - but in this case, do not go deeper into the tree
                                            #
                                            # Do not look for another RE-USE of this new variable in a BIND.
                                            tmp_occurrences = \
                                                scenario_bind_detection. \
                                                    scenario_bind_occurrences({"where": pattern["patterns"]},
                                                                              look_for,
                                                                              location, bound_variables, False,
                                                                              data_type)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "bind"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["bind"] += tmp_occurrences

                                            # scenario blank_mode
                                            tmp_occurrences = \
                                                scenario_blank_node_detection. \
                                                    scenario_blank_node_occurrences(
                                                    {"where": pattern["patterns"]}, look_for,
                                                    bound_variables)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "blank_node"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["blank_node"] += tmp_occurrences

                                            # if RE-USED in another FILTER - but in this case, do not go deeper into the tree
                                            #
                                            # Do not look for another RE-USE in a FILTER.

                                            # scenario filter
                                            tmp_occurrences = \
                                                scenario_filter_detection. \
                                                    scenario_filter_occurrences({"where": pattern["patterns"]},
                                                                                look_for, location,
                                                                                bound_variables, False, data_type)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "filter"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["filter"] += tmp_occurrences

                                            # scenario group
                                            # check, if there are some group term types left
                                            check_for_still_existing_group = \
                                                scenario_group_detection. \
                                                    scenario_group_occurrences({"where": pattern["patterns"]},
                                                                               look_for, bound_variables)
                                            if check_for_still_existing_group > 0:
                                                raise Exception

                                            # scenario literal
                                            tmp_occurrences = \
                                                scenario_literal_detection. \
                                                    scenario_literal_occurrences(
                                                    {"where": pattern["patterns"]}, look_for, bound_variables)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "literal"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["literal"] += tmp_occurrences

                                            # if RE-USED in another MINUS - but in this case, do not go deeper into the tree
                                            #
                                            # Do not look for another RE-USE in a MINUS.
                                            # scenario minus
                                            tmp_occurrences = \
                                                scenario_minus_detection. \
                                                    scenario_minus_occurrences({"where": pattern["patterns"]},
                                                                               look_for, location,
                                                                               bound_variables, False, data_type)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "minus"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["minus"] += tmp_occurrences

                                            # if RE-USED in another OPTIONAL - but in this case, do not go deeper into the tree
                                            #
                                            # Do not look for another RE-USE in a OPTIONAL.
                                            # scenario optional
                                            tmp_occurrences = \
                                                scenario_optional_detection. \
                                                    scenario_optional_occurrences(
                                                    {"where": pattern["patterns"]}, look_for, location,
                                                    bound_variables, False, data_type)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "optional"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["optional"] += tmp_occurrences

                                            # scenario prop_path
                                            tmp_occurrences = \
                                                scenario_prop_path_detection. \
                                                    scenario_prop_path_occurrences(
                                                    {"where": pattern["patterns"]}, look_for, location,
                                                    bound_variables, False, data_type)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "prop_path"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["prop_path"] += tmp_occurrences

                                            # scenario service
                                            tmp_occurrences = \
                                                scenario_service_detection. \
                                                    scenario_service_occurrences(
                                                    {"where": pattern["patterns"]}, look_for, bound_variables)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "service"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["service"] += tmp_occurrences

                                            # if RE-USED in another SUBSELECT - but in this case, do not go deeper into the tree
                                            #
                                            # Do not look for another RE-USE in a SUBSELECT.
                                            # scenario subselect
                                            tmp_occurrences = \
                                                scenario_subselect_detection. \
                                                    scenario_subselect_occurrences(
                                                    {"where": pattern["patterns"]}, look_for,
                                                    location,
                                                    bound_variables, False, data_type)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "subselect"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["subselect"] += tmp_occurrences

                                            # if RE-USED in another UNION - but in this case, do not go deeper into the tree
                                            #
                                            # Do not look for another RE-USE in a UNION.
                                            # scenario union
                                            tmp_occurrences = \
                                                scenario_union_detection. \
                                                    scenario_union_occurrences({"where": pattern["patterns"]},
                                                                               look_for, location,
                                                                               bound_variables, False, data_type)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "union"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["union"] += tmp_occurrences

                                            # scenario values
                                            tmp_occurrences = \
                                                scenario_values_detection. \
                                                    scenario_values_occurrences({"where": pattern["patterns"]},
                                                                                look_for, bound_variables)
                                            subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"][
                                                "values"] += tmp_occurrences
                                            current_datatype_dict_subselect_layer["values"] += tmp_occurrences

                                            # if the variable could not be found in the patterns of the UNION
                                            if subselect_statistical_information[
                                                "scenarios_found_in_second_level_union"] == tmp_dict:
                                                subselect_statistical_information[
                                                    "scenarios_found_in_second_level_union"][
                                                    "not_found_in_patterns"] += \
                                                        str(pattern["patterns"]).count(look_for)
                                                current_datatype_dict_subselect_layer["not_found_in_patterns"] += \
                                                     str(pattern["patterns"]).count(look_for)

                        # save the json object
                        with open(location + "/subselect_statistical_information.json", "w") as json_data:
                            json.dump(subselect_statistical_information, json_data)
                            json_data.close()
                            # print(subselect_statistical_information)

    return result


def delete_and_join_all_GROUP_patterns_to_the_overall_SUBSELECT_patterns(subselect):
    # recursive fun
    group_was_found = False

    where_list = subselect["where"]

    for pattern in where_list:
        if pattern["type"] == "group":
            subselect["where"].remove(pattern)
            subselect["where"] = \
                subselect["where"] + pattern["patterns"]
            group_was_found = True

    if group_was_found:
        # recursion start
        delete_and_join_all_GROUP_patterns_to_the_overall_SUBSELECT_patterns(subselect)
    else:
        # recursion stop
        return