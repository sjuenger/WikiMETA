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

import os
import json


def scenario_bind_occurrences(json_object, look_for, location, _):
    # 'location' is the path to the current 'scenarios' folder
    # -> for the statistical information, in which scenario the found
    # bound "looking for ITEM" is used afterwards

    where = json_object["where"]
    # find scenarios 'filter'

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:
        if where_part["type"] == "bind":
            # if the bind operation is not just an assignment to a variable
            # {'type': 'bind', 'variable': {'termType': 'Variable', 'value': 'var3'}, 'expression': {'type': 'operation', 'operator': 'exists', 'args': [{'type': 'bgp', 'triples': [{'subject': {'termType': 'Variable', 'value': 'var4'}, 'predicate': {'termType': 'NamedNode', 'value': 'http://www.w3.org/ns/prov#wasDerivedFrom'}, 'object': {'termType': 'Variable', 'value': 'var5'}}]}]}}
            # TODO: Which type of BIND? Exist, If, ...
            if "args" in where_part["expression"]:
                if look_for in str(where_part["expression"]["args"]):
                    if "operator" in where_part["expression"]:
                        print("args " + where_part["expression"]["operator"])
                    else:
                        print("here")
                        print(where_part)
                    # there may be more than one
                    result += str(where_part["expression"]["args"]).count(look_for)

            # if the bind operation is just an assignment to a variable
            # {'type': 'bind', 'variable': {'termType': 'Variable', 'value': 'var4'}, 'expression': {'termType': 'NamedNode', 'value': 'http://www.wikidata.org/prop/qualifier/P582'}}
            elif "termType" in where_part["expression"]:
                print("termType")

                if look_for in str(where_part["expression"]["value"]):

                    # there may be more than one
                    result += str(where_part["expression"]["value"]).count(look_for)

                    # TODO: if that happens -> detect the scenario, the resulting variable is in!

                    # look, if there already exists a 'bind_scenarios_information'
                    if os.path.isfile(location + "/bind_statistical_information.json"):
                        with open(location + "/bind_statistical_information.json", "r") as json_data:
                            bind_statistical_information = json.load(json_data)
                            json_data.close()
                    else:
                        bind_statistical_information = \
                            {
                                "total_occurrences": 0,
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
                                "group": 0,
                                "bind": 0,
                                "blank_node": 0,
                                "minus": 0,
                                "subselect": 0,
                                "ref_value": 0,
                                "literal": 0,
                                "values": 0,
                                "service": 0,
                                "other": 0}

                    #variable to look for
                    variable_look_for = str(where_part["variable"]["value"])
                    print(variable_look_for)
                    print(json_object)

                    bind_statistical_information["total_occurrences"] += 1
                    # scenario one
                    bind_statistical_information["one"] += \
                        scenario_one_detection.scenario_one_occurrences(json_object, variable_look_for)
                    # scenario two
                    bind_statistical_information["two"] += \
                        scenario_two_detection.scenario_two_occurrences(json_object, variable_look_for)
                    # scenario three
                    bind_statistical_information["three"] += \
                        scenario_three_detection.scenario_three_occurrences(json_object, variable_look_for)
                    # scenario four
                    bind_statistical_information["four"] += \
                        scenario_four_detection.scenario_four_occurrences(json_object, variable_look_for)
                    # scenario five
                    bind_statistical_information["five"] += \
                        scenario_five_detection.scenario_five_occurrences(json_object, variable_look_for)
                    # scenario six
                    bind_statistical_information["six"] += \
                        scenario_six_detection.scenario_six_occurrences(json_object, variable_look_for)
                    # scenario seven
                    bind_statistical_information["seven"] += \
                        scenario_seven_detection.scenario_seven_occurrences(json_object, variable_look_for)
                    # scenario eight
                    bind_statistical_information["eight"] += \
                        scenario_eight_detection.scenario_eight_occurrences(json_object, variable_look_for)
                    # scenario nine
                    bind_statistical_information["nine"] += \
                        scenario_nine_detection.scenario_nine_occurrences(json_object, variable_look_for)
                    # scenario tne
                    bind_statistical_information["ten"] += \
                        scenario_ten_detection.scenario_ten_occurrences(json_object, variable_look_for)
                    # scenario eleven
                    bind_statistical_information["eleven"] += \
                        scenario_eleven_detection.scenario_eleven_occurrences(json_object, variable_look_for)
                    # scenario twelve
                    bind_statistical_information["twelve"] += \
                        scenario_twelve_detection.scenario_twelve_occurrences(json_object, variable_look_for)
                    # scenario bind
                    # -> no covering of this case. A variable cannot be assigned to another variable
                    # TODO: check this statement
                    # scenario blank_mode
                    bind_statistical_information["blank_node"] += \
                        scenario_blank_node_detection.scenario_blank_node_occurrences(json_object, variable_look_for)
                    # scenario filter
                    bind_statistical_information["filter"] += \
                        scenario_filter_detection.scenario_filter_occurrences(json_object, variable_look_for)
                    # scenario group
                    bind_statistical_information["group"] += \
                        scenario_group_detection.scenario_group_occurrences(json_object, variable_look_for)
                    # scenario literal
                    bind_statistical_information["literal"] += \
                        scenario_literal_detection.scenario_literal_occurrences(json_object, variable_look_for)
                    # scenario minus
                    bind_statistical_information["minus"] += \
                        scenario_minus_detection.scenario_minus_occurrences(json_object, variable_look_for)
                    # scenario optional
                    bind_statistical_information["optional"] += \
                        scenario_optional_detection.scenario_optional_occurrences(json_object, variable_look_for)
                    # scenario prop_path
                    bind_statistical_information["prop_path"] += \
                        scenario_prop_path_detection.scenario_prop_path_occurrences(json_object, variable_look_for)
                    # scenario ref_value
                    bind_statistical_information["ref_value"] += \
                        scenario_ref_value_detection.scenario_ref_value_occurrences(json_object, variable_look_for)
                    # scenario service
                    bind_statistical_information["service"] += \
                        scenario_service_detection.scenario_service_occurrences(json_object, variable_look_for)
                    # scenario subselect
                    bind_statistical_information["subselect"] += \
                        scenario_subselect_detection.scenario_subselect_occurrences(json_object, variable_look_for)
                    # scenario union
                    bind_statistical_information["union"] += \
                        scenario_union_detection.scenario_union_occurrences(json_object, variable_look_for)
                    # scenario values
                    bind_statistical_information["values"] += \
                        scenario_values_detection.scenario_values_occurrences(json_object, variable_look_for)


                    # save the json object
                    with open(location + "/bind_statistical_information.json", "w") as json_data:
                        json.dump(bind_statistical_information, json_data)
                        json_data.close()

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

    return result
