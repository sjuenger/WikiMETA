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


def scenario_filter_occurrences(json_object, look_for):
    where = json_object["where"]

    # find scenarios 'filter'

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:
        if where_part["type"] == "filter":
            if (look_for in str(where_part["expression"])):
                # there may be more than one
                result += str(where_part["expression"]).count(look_for)

    # if result:
    # print(result)
    # print("Scenario 1")
    # print(where)

    return result
