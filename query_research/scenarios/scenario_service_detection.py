# method to detect scenario service
#
#
#
# constellation for "wikidata.org/prop/qualifier"
#
# scenario subselect:
# SELECT ?var1  ?var1Label  ?var2  ?var3  ?var4  ?var5  ?var6  ?var7
# WHERE {
#  SERVICE  <http://wikiba.se/ontology#box>   {
#     ?var8  <http://www.wikidata.org/prop/qualifier/P625>  ?var3 .
#     <http://www.bigdata.com/rdf#serviceParam>  <http://wikiba.se/ontology#cornerWest>  "POINT(88 23)"^^<http://www.opengis.net/ont/geosparql#wktLiteral> .
#     <http://www.bigdata.com/rdf#serviceParam>  <http://wikiba.se/ontology#cornerEast>  "POINT(88 23)"^^<http://www.opengis.net/ont/geosparql#wktLiteral> .
#   }
#   ?var1  <http://www.wikidata.org/prop/P119>  ?var8 ;
#  <http://www.wikidata.org/prop/direct/P31>  <http://www.wikidata.org/entity/Q5> .
#  OPTIONAL {
#   ?var1  <http://www.wikidata.org/prop/direct/P1442>  ?var4 .
#  }
#  OPTIONAL {
#   ?var1  <http://www.wikidata.org/prop/direct/P18>  ?var5 .
#  }
#  OPTIONAL {
#   ?var1  <http://www.wikidata.org/prop/direct/P569>  ?var6 .
#  }
#  OPTIONAL {
#   ?var1  <http://www.wikidata.org/prop/direct/P570>  ?var7 .
#  }
# SERVICE  <http://wikiba.se/ontology#label>   {
#     <http://www.bigdata.com/rdf#serviceParam>  <http://wikiba.se/ontology#language>  "en".
#   }
# }
# ORDER BY ASC( ?var1Label )
#
#
#
# look_for e.g. "http://www.wikidata.org/prop/qualifier/"


def scenario_service_occurrences(json_object, look_for):
    where = json_object["where"]

    # find scenarios 'service'

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:
        if "type" in where_part:
            if where_part["type"] == "service":
                if (look_for in str(where_part["patterns"])):
                    # there may be more than one
                    result += str(where_part["patterns"]).count(look_for)
                else:
                    if look_for in str(where_part):
                        raise Exception

    #if result:
    #    print(result)
    #    print("Scenario union")
    #    print(where)

    return result
