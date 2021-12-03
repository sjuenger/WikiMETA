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
# look_for e.g. "<http://www.w3.org/ns/prov#wasDerivedFrom>"


def is_scenario_optional(json_object, look_for):
    where = json_object["where"]

    # find scenario 'filter'

    result = False

    # multiple bgp (basic graph patterns)
    for where_part in where:
        if where_part["type"] == "optional":
            if (look_for in where_part["patterns"]):
                result = True

    # if result:
    # print(result)
    # print("Scenario 1")
    # print(where)

    return result
