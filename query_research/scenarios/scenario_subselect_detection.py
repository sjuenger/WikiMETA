# method to detect scenario subselect
#
#
#
# constellation for "wasDerivedFrom"
#
# scenario subselect:
# SELECT ?var1 ( COUNT ( ?var1  ) AS  ?var2  )
# WHERE {
#  SELECT DISTINCT ?var3  ?var1
#  WHERE  {
#    ?var3  <http://www.wikidata.org/prop/direct/P279>  <http://www.wikidata.org/entity/Q7187> ;
#  <http://www.wikidata.org/prop/direct/P703>  <http://www.wikidata.org/entity/Q5> ;
#  ?var1  ?var4 .
#  FILTER (   ( !( REGEX (  STR (  ?var1  ) , "string1" ) ) )
# ) .
#  FILTER (   (  REGEX (  STR (  ?var1  ) , "string2" )  )
# ) .
#  FILTER (   (  NOT EXISTS   {
#     ?var3  ?var1  ?var4 .
#     ?var4  <http://www.w3.org/ns/prov#wasDerivedFrom>  ?var5 .
#   }
#  )
# ) .
#  }
# }
# GROUP BY  ?var1
# ORDER BY  DESC( ?var2 )
#
#
#
# look_for e.g. "http://www.w3.org/ns/prov#wasDerivedFrom"


def scenario_subselect_occurrences(json_object, look_for):
    where = json_object["where"]

    # find scenarios 'subselect'

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:
        if "queryType" in where_part:
            if where_part["queryType"] == "SELECT":
                if (look_for in str(where_part["where"])):
                    # there may be more than one
                    result += str(where_part["where"]).count(look_for)
                else:
                    if look_for in str(where_part):
                        raise Exception

    #if result:
    #    print(result)
    #    print("Scenario union")
    #    print(where)

    return result
