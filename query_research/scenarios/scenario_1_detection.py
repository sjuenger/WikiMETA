# method to detect scenario one
#
#
#
# constellation for "wasDerivedFrom"
#
# scenario 1:
# ?s prov:wasDerivedFrom ?o .
#
#
#
# look_for e.g. "http://www.w3.org/ns/prov#wasDerivedFrom"


def scenario_one_occurrences(json_object, look_for):
    where = json_object["where"]

    # find BIND Variables
    bound_variables = []
    for where_part in where:
        if where_part["type"] == "bind":
            print(where_part)

            if "termType" in where_part["expression"]:
                if where_part["expression"]["termType"] == "NamedNode":
                    if where_part["variable"]["termType"] == "Variable":
                        bound_variables.append(
                            (where_part["variable"]["value"], where_part["expression"]["value"]))
                print("Bound Variables: 1")
                print(bound_variables)

                # TODO: Declare a reference in bound variables as an own scenario

    # find scenarios 1
    # -> there might be more than one scenario one found
    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:

        if where_part["type"] == "bgp":
            for triple in where_part["triples"]:

                if (triple["subject"]["termType"] == "Variable") and ((triple["subject"]["value"])
                                                                      not in bound_variables.__str__()):
                    # on property paths, there also could be no termType
                    if "termType" in triple["predicate"]:
                        # the "look_for in" is necessary, for the properties / nodes with a specific identifying number
                        # Example:
                        # Triple: ?var5  <http://www.wikidata.org/prop/reference/P3987>  ?var6 .
                        # Code: "http://www.wikidata.org/prop/reference/P" in triple["predicate"]["value"]
                        # All variables in the data are named in a schema like ?var1, ?var2, ...
                        # .. so, there can't be e.g. a varaible named "http://www.wikidata.org/prop/reference/Pxxx"
                        if (triple["predicate"]["termType"] == "NamedNode" and
                                look_for in triple["predicate"]["value"]):

                            if (triple["object"]["termType"] == "Variable") and ((triple["object"]["value"])
                                                                                 not in bound_variables.__str__()):
                                result += 1
    # if result:
    # print(result)
    # print("Scenario 1")
    # print(where)

    return result
