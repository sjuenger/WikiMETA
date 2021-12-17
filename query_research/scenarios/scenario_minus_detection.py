# method to detect scenario minus
#
#
#
# constellation for "wasDerivedFrom"
#
# scenario minus:
#SELECT ?var1
#WHERE {
#  ?var1  <http://wikiba.se/ontology#sitelinks> "0"^^<http://www.w3.org/2001/XMLSchema#integer> ;
# <http://wikiba.se/ontology#statements> "0"^^<http://www.w3.org/2001/XMLSchema#integer> .
#  MINUS   {
#    ?var2  <http://wikiba.se/ontology#propertyType>  <http://wikiba.se/ontology#WikibaseItem> ;
# <http://wikiba.se/ontology#claim>  ?var3 ;
# <http://wikiba.se/ontology#statementProperty>  ?var4 .
#    []  ?var3  [  ?var4  ?var1  ] .
#  }
#  MINUS   {
#    ?var5  <http://wikiba.se/ontology#propertyType>  <http://wikiba.se/ontology#WikibaseItem> ;
# <http://wikiba.se/ontology#qualifier>  ?var6 .
#    []  ?var6  ?var1 .
#  }
#  MINUS   {
#    ?var7  <http://wikiba.se/ontology#propertyType>  <http://wikiba.se/ontology#WikibaseItem> ;
# <http://wikiba.se/ontology#reference>  ?var8 .
#    []  <http://www.w3.org/ns/prov#wasDerivedFrom>  [  ?var8  ?var1  ] .
#  }
#  MINUS   {
#    ?var9  <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>  <http://wikiba.se/ontology#Property> ;
# <http://wikiba.se/ontology#claim>  ?var10 .
#    ?var1  ?var10  [] .
#  }
#  MINUS   {
#    ?var11  <http://schema.org/about>  ?var1 .
#  }
# }
#
#
#
# look_for e.g. "http://www.w3.org/ns/prov#wasDerivedFrom"


def scenario_minus_occurrences(json_object, look_for):
    where = json_object["where"]

    # find scenarios 'minus'

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:
        if where_part["type"] == "minus":
            if (look_for in str(where_part["patterns"])):
                result += 1

    #if result:
    #    print(result)
    #    print("Scenario union")
    #    print(where)

    return result
