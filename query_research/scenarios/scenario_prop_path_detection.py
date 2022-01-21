# method to detect scenario property path
#
#
#
# constellation for "wasDerivedFrom"
#
# scenario filter:
# ?s prov:wasDerivedFrom / ?p ?o .
#
#
#
# look_for e.g. "http://www.w3.org/ns/prov#wasDerivedFrom"


def scenario_prop_path_occurrences(json_object, look_for, bound_variables):
    where = json_object["where"]

    # find scenarios property path

    result = False

    # multiple bgp (basic graph patterns)
    for where_part in where:

        if where_part["type"] == "bgp":
            for triple in where_part["triples"]:

                if ("type" in triple["predicate"]):
                    # on "normal" properties, there is only a 'termType' and no 'type'
                    if (triple["predicate"]["type"] == "path") :
                        if look_for in str(triple["predicate"]["items"]):
                            # TODO: add the bind variables here ?

                            result += 1
                    else:
                        if look_for in str(where_part):
                            raise Exception

    return result
