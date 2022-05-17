# method to detect scenario bind
#
#
#
# constellation for "wasDerivedFrom"
#
# scenario bind:
# BIND(EXISTS
# {
# ?var4 < http: // www.w3.org / ns / prov
# wasDerivedFrom>  ?var5 .
# }
# AS  ?var3 ).
#
#
#
# look_for e.g. "http://www.w3.org/ns/prov#wasDerivedFrom"

import query_research.scenario_detection_unit as scenario_detection_unit
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
import query_research.scenarios.scenario_blank_node_detection as scenario_blank_node_detection
import query_research.scenarios.scenario_minus_detection as scenario_minus_detection
import query_research.scenarios.scenario_subselect_detection as scenario_subselect_detection
import query_research.scenarios.scenario_literal_detection as scenario_literal_detection
import query_research.scenarios.scenario_values_detection as scenario_values_detection
import query_research.scenarios.scenario_service_detection as scenario_service_detection

import os
import json


def scenario_bind_occurrences(json_object, look_for, location, bound_variables, look_for_additional_layer, data_type):
    # 'location' is the path to the current 'scenarios' folder
    # -> for the statistical information, in which scenario the found
    # bound "looking for ITEM" is used afterwards

    where = json_object["where"]
    # find scenarios 'filter'

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:
        if "type" in where_part and where_part["type"] == "bind":
            # if the bind operation is not just an assignment to a variable
            # {'type': 'bind', 'variable': {'termType': 'Variable', 'value': 'var3'}, 'expression': {'type': 'operation', 'operator': 'exists', 'args': [{'type': 'bgp', 'triples': [{'subject': {'termType': 'Variable', 'value': 'var4'}, 'predicate': {'termType': 'NamedNode', 'value': 'http://www.w3.org/ns/prov#wasDerivedFrom'}, 'object': {'termType': 'Variable', 'value': 'var5'}}]}]}}
            # TODO: Which type of BIND? Exist, If, ...
            if "args" in where_part["expression"]:
                if look_for in str(where_part["expression"]["args"]):
                    if "operator" in where_part["expression"]:
                        # print("args " + where_part["expression"]["operator"])
                        pass
                    else:
                        #print("here")
                        #print(where_part)
                        pass
                    # there may be more than one
                    result += str(where_part["expression"]["args"]).count(look_for)

            # if the bind operation is just an assignment to a variable
            # {'type': 'bind', 'variable': {'termType': 'Variable', 'value': 'var4'}, 'expression': {'termType': 'NamedNode', 'value': 'http://www.wikidata.org/prop/qualifier/P582'}}
            elif "termType" in where_part["expression"]:
                #print("termType")

                if look_for in str(where_part["expression"]["value"]):

                    # there may be more than one
                    result += str(where_part["expression"]["value"]).count(look_for)
                    #print(result)

                    # if that happens -> detect the scenario, the resulting variable is in!
                    # but ONLY do that, if the 'look_for_aditional_layer boolean is set to true
                    # (to prevent re-iteration)
                    if look_for_additional_layer:

                        # look, if there already exists a 'bind_scenarios_information'
                        if os.path.isfile(location + "/bind_statistical_information.json"):
                            with open(location + "/bind_statistical_information.json", "r") as json_data:
                                bind_statistical_information = json.load(json_data)
                                json_data.close()
                        else:
                            scenarios_dict = \
                                {
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
                                    "not_found_in_query": 0}

                            bind_statistical_information = \
                                {
                                    "total_found_bound_variables_to_metadata": 0,
                                    "variables_found_in_scenarios": scenarios_dict}


                        #variable to look for
                        variable_look_for = str(where_part["variable"]["value"])
                        #print(variable_look_for)
                        #print(json_object)

                        bind_statistical_information["total_found_bound_variables_to_metadata"] += \
                            str(where_part["expression"]["value"]).count(look_for)
                        #
                        # detect the scenario the found, bound variable might be in (it can also be not found in any other
                        # .. expression)

                        tmp_dict = bind_statistical_information["variables_found_in_scenarios"].copy()

                        # scenario prop_one
                        bind_statistical_information["variables_found_in_scenarios"]["prop_one"] += \
                            scenario_prop_one_detection.\
                                scenario_prop_one_occurrences(json_object, variable_look_for, bound_variables)
                        # scenario prop_three
                        bind_statistical_information["variables_found_in_scenarios"]["prop_three"] += \
                            scenario_prop_three_detection.\
                                scenario_prop_three_occurrences(json_object, variable_look_for, bound_variables)
                        # scenario prop_two
                        bind_statistical_information["variables_found_in_scenarios"]["prop_two"] += \
                            scenario_prop_two_detection.\
                                scenario_prop_two_occurrences(json_object, variable_look_for, bound_variables)
                        # scenario prop_four
                        bind_statistical_information["variables_found_in_scenarios"]["prop_four"] += \
                            scenario_prop_four_detection.\
                                scenario_prop_four_occurrences(json_object, variable_look_for, bound_variables)
                        # scenario obj_one
                        bind_statistical_information["variables_found_in_scenarios"]["obj_one"] += \
                            scenario_obj_one_detection.\
                                scenario_obj_one_occurrences(json_object, variable_look_for, bound_variables)
                        # scenario obj_two
                        bind_statistical_information["variables_found_in_scenarios"]["obj_two"] += \
                            scenario_obj_two_detection.\
                                scenario_obj_two_occurrences(json_object, variable_look_for, bound_variables)
                        # scenario obj_three
                        bind_statistical_information["variables_found_in_scenarios"]["obj_three"] += \
                            scenario_obj_three_detection.\
                                scenario_obj_three_occurrences(json_object, variable_look_for, bound_variables)
                        # scenario obj_four
                        bind_statistical_information["variables_found_in_scenarios"]["obj_four"] += \
                            scenario_obj_four_detection.\
                                scenario_obj_four_occurrences(json_object, variable_look_for, bound_variables)
                        # scenario sub_one
                        bind_statistical_information["variables_found_in_scenarios"]["sub_one"] += \
                            scenario_sub_one_detection.\
                                scenario_sub_one_occurrences(json_object, variable_look_for, bound_variables)
                        # scenario sub_two
                        bind_statistical_information["variables_found_in_scenarios"]["sub_two"] += \
                            scenario_sub_two_detection.\
                                scenario_sub_two_occurrences(json_object, variable_look_for, bound_variables)
                        # scenario sub_three
                        bind_statistical_information["variables_found_in_scenarios"]["sub_three"] += \
                            scenario_sub_three_detection.\
                                scenario_sub_three_occurrences(json_object, variable_look_for, bound_variables)
                        # scenario sub_four
                        bind_statistical_information["variables_found_in_scenarios"]["sub_four"] += \
                            scenario_sub_four_detection.\
                                scenario_sub_four_occurrences(json_object, variable_look_for, bound_variables)


                        # scenario bind
                        # if a variable is RE-USED in another BIND - but in this case, do not go deeper into the tree
                        #
                        # Do not look for another RE-USE of this new variable in a BIND.
                        bind_statistical_information["variables_found_in_scenarios"]["bind"] += \
                            scenario_bind_occurrences(json_object, variable_look_for,
                                                          location, bound_variables, False, data_type)


                        # scenario blank_mode
                        bind_statistical_information["variables_found_in_scenarios"]["blank_node"] += \
                            scenario_blank_node_detection.\
                                scenario_blank_node_occurrences(json_object, variable_look_for, bound_variables)


                        # if RE-USED in another FILTER - but in this case, do not go deeper into the tree
                        #
                        # Do not look for another RE-USE in a FILTER.
                        # scenario filter
                        bind_statistical_information["variables_found_in_scenarios"]["filter"] += \
                            scenario_filter_detection. \
                                scenario_filter_occurrences(json_object, look_for, location,
                                                            bound_variables, False, data_type)

                        # scenario group
                        # check, if there are some group term types left
                        check_for_still_existing_group = \
                            scenario_group_detection.\
                                scenario_group_occurrences(json_object, variable_look_for, bound_variables)
                        if check_for_still_existing_group > 0:
                            raise Exception
                        # scenario literal
                        bind_statistical_information["variables_found_in_scenarios"]["literal"] += \
                            scenario_literal_detection.\
                                scenario_literal_occurrences(json_object, variable_look_for, bound_variables)


                        # if RE-USED in another MINUS - but in this case, do not go deeper into the tree
                        #
                        # Do not look for another RE-USE in a MINUS.
                        # scenario minus
                        bind_statistical_information["variables_found_in_scenarios"]["minus"] += \
                            scenario_minus_detection. \
                                scenario_minus_occurrences(json_object, look_for, location,
                                                           bound_variables, False, data_type)


                        # if RE-USED in another OPTIONAL - but in this case, do not go deeper into the tree
                        #
                        # Do not look for another RE-USE in a OPTIONAL.
                        # scenario optional
                        bind_statistical_information["variables_found_in_scenarios"]["optional"] += \
                            scenario_optional_detection. \
                                scenario_optional_occurrences(json_object, look_for, location,
                                                              bound_variables, False, data_type)

                        # scenario prop_path
                        bind_statistical_information["variables_found_in_scenarios"]["prop_path"] += \
                            scenario_prop_path_detection.\
                                scenario_prop_path_occurrences(json_object, look_for,
                                                            location,
                                                            bound_variables, False, data_type)

                        # scenario service
                        bind_statistical_information["variables_found_in_scenarios"]["service"] += \
                            scenario_service_detection.\
                                scenario_service_occurrences(json_object, variable_look_for, bound_variables)


                        # if RE-USED in another SUBSELECT - but in this case, do not go deeper into the tree
                        #
                        # Do not look for another RE-USE in a SUBSELECT.
                        # scenario subselect
                        bind_statistical_information["variables_found_in_scenarios"]["subselect"] += \
                            scenario_subselect_detection. \
                                scenario_subselect_occurrences(json_object, look_for,
                                                            location,
                                                            bound_variables, False, data_type)




                        # if RE-USED in another UNION - but in this case, do not go deeper into the tree
                        #
                        # Do not look for another RE-USE in a UNION.
                        # scenario union
                        bind_statistical_information["variables_found_in_scenarios"]["union"] += \
                            scenario_union_detection. \
                                scenario_union_occurrences(json_object, look_for, location,
                                                           bound_variables, False, data_type)


                        # scenario values
                        bind_statistical_information["variables_found_in_scenarios"]["values"] += \
                            scenario_values_detection.\
                                scenario_values_occurrences(json_object, variable_look_for, bound_variables)

                        # if the variable could not be found in the where part of the query
                        if bind_statistical_information["variables_found_in_scenarios"] == tmp_dict:
                            if str(where_part).count(variable_look_for) > 1:
                                raise Exception
                            bind_statistical_information["variables_found_in_scenarios"]["not_found_in_query"] += 1

                        # save the json object
                        with open(location + "/bind_statistical_information.json", "w") as json_data:
                            json.dump(bind_statistical_information, json_data)
                            json_data.close()
                            #print(bind_statistical_information)

            # for e.g. :
            # BIND(MIN( ?var15Label  ) AS  ?var7 ).
            # BIND(CONCAT("[[", ?var16, "]]" )  AS  ?var2 ).
            # --> constructions, that do not correspond to the above constellations
            elif look_for in str(where_part["expression"]):
                # there may be more than one
                result += str(where_part["expression"]).count(look_for)

            else:
                if look_for in str(where_part):
                    raise Exception

            # TODO: Check the other scenarios like this one!
            # TODO: What if a BIND Operation is in a sub-select?

    return result
