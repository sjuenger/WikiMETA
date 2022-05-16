# method to detect scenario prop_one
#
#
#
# constellation for "wasDerivedFrom"
#
# scenario prop_one:
# ?s prov:wasDerivedFrom ?o .
#
#
#
# look_for e.g. "http://www.w3.org/ns/prov#wasDerivedFrom"


def scenario_prop_one_occurrences(json_object, look_for, bound_variables):
    where = json_object["where"]

    # find scenarios prop_one
    # -> there might be more than one scenario found
    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:

        if "type" in where_part and where_part["type"] == "bgp":
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
                                look_for in triple["predicate"]["value"])\
                                or (look_for == triple["predicate"]["value"] and look_for in str(bound_variables)
                                    and triple["predicate"]["termType"] == "Variable"):
                            # -> if a 'var4' is bound to a item we are looking for
                            # e.g.

                            if (triple["object"]["termType"] == "Variable") and ((triple["object"]["value"])
                                                                                 not in bound_variables.__str__()):
                                result += 1

    return result
