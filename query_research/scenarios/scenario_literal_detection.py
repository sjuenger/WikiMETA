# method to detect scenario literal
#
#
#
# constellation for "literal"
#
# scenario literal
# e.g.
# SELECT DISTINCT ?var1
# WHERE {
#   ?var1  <http://www.wikidata.org/prop/P1087>  ?var2 .
#   ?var3  <http://www.wikidata.org/prop/reference/P1440>  "P1440".
# }
#
#
#
# look_for e.g. "http://www.wikidata.org/prop/reference/P...."


def scenario_literal_occurrences(json_object, look_for, _):
    where = json_object["where"]

    # find scenarios with literals
    # -> there might be more than one scenario one found
    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:

        if where_part["type"] == "bgp":
            for triple in where_part["triples"]:

                if ((triple["subject"]["termType"] == "Literal")
                        or (triple["object"]["termType"] == "Literal")):
                    # on property paths, there also could be no termType - or on normal predicates no "type"
                    # -> compare the string

                    if look_for in str(triple["predicate"]):
                        result += 1

    return result