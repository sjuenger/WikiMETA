# method to detect scenario 'values'
#
#
#
# constellation for "NormalRank"
#
#SELECT DISTINCT ?var1 ( COUNT ( ?var1  ) AS  ?var2  )
#WHERE {
#  VALUES (  ?var1  ) {
#   (  <http://wikiba.se/ontology#DeprecatedRank>  )
#   (  <http://wikiba.se/ontology#NormalRank>  )
#  }
#  ?var3  <http://www.wikidata.org/prop/P699>  ?var4 .
#  ?var4  <http://wikiba.se/ontology#rank>  ?var1 .
#}
#GROUP BY  ?var1
#
#
#
# look_for e.g. "http://wikiba.se/ontology#NormalRank"


def scenario_values_occurrences(json_object, look_for, _):
    where = json_object["where"]

    # find scenarios 'values'

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:
        if where_part["type"] == "values":
            if (look_for in str(where_part["values"])):
                # there may be more than one
                result += str(where_part["values"]).count(look_for)
            else:
                if look_for in str(where_part):
                    raise Exception

    return result
