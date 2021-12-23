# method to detect scenario blank node
#
#
#
# constellation for "wasDerivedFrom"
#
# scenario blank node
# e.g.
# SELECT ?var1
# WHERE {
#   ?var1  ?var2  [  <http://www.w3.org/ns/prov#wasDerivedFrom>  [ ( <http://www.wikidata.org/prop/reference/P248> / <http://www.wikidata.org/prop/direct/P279> *) <http://www.wikidata.org/entity/Q2668072>  ]  ] .
# }
#
#
#
# look_for e.g. "http://www.w3.org/ns/prov#wasDerivedFrom"


def scenario_blank_node_occurrences(json_object, look_for):
    where = json_object["where"]

    # find scenarios blank node
    # -> there might be more than one scenario one found
    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:

        if where_part["type"] == "bgp":
            for triple in where_part["triples"]:

                if ((triple["subject"]["termType"] == "BlankNode")
                        or (triple["object"]["termType"] == "BlankNode")):
                    # on property paths, there also could be no termType - or on normal predicates no "type"
                    # -> compare the string

                    if look_for in str(triple["predicate"]):

                        result += 1
                        
    # if result:
    # print(result)
    # print("Scenario 1")
    # print(where)

    return result