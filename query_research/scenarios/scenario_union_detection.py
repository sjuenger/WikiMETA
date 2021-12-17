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
#
#
# look_for e.g. "http://www.w3.org/ns/prov#wasDerivedFrom"


def scenario_union_occurrences(json_object, look_for):
    where = json_object["where"]

    # find scenarios 'union'

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:
        if where_part["type"] == "union":
            if (look_for in str(where_part["patterns"])):
                result += 1

    #if result:
    #    print(result)
    #    print("Scenario union")
    #    print(where)

    return result
