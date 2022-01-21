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


def scenario_optional_occurrences(json_object, look_for, _):
    where = json_object["where"]

    # find scenarios 'optional'

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:
        if where_part["type"] == "optional":
            if (look_for in str(where_part["patterns"])):
                # there may be more than one
                result += str(where_part["patterns"]).count(look_for)
            else:
                if look_for in str(where_part):
                    raise Exception

    return result
