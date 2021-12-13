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
# look_for e.g. "<http://www.w3.org/ns/prov#wasDerivedFrom>"


def is_scenario_prop_path(json_object, look_for):
    where = json_object["where"]

    # find BIND Variables
    bound_variables = []
    for where_part in where:
        if where_part["type"] == "bind":

            if "termType" in where_part["expression"]:
                if where_part["expression"]["termType"] == "NamedNode":
                    if where_part["variable"]["termType"] == "Variable":
                        bound_variables.append(
                            (where_part["variable"]["value"], where_part["expression"]["value"]))

    # find scenario property path

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

                            result = True

    # if result:
    # print(result)
    # print("Scenario 1")
    # print(where)

    return result
