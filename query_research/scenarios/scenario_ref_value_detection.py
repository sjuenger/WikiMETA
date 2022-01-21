# method to detect scenario reference value (normalized
#
#
#
# constellation for "wasDerivedFrom"
#
# scenario subselect:
# SELECT ?var1  ?var2
# WHERE {
#  ?var1  <http://www.wikidata.org/prop/reference/value/P248>  <http://www.wikidata.org/entity/Q23571040> .
#}
#
# SELECT ?var1  ?var1Label
# WHERE {
#   ?var2  <http://www.wikidata.org/prop/reference/value-normalized/P149P149>  ?var1 .
#  SERVICE  <http://wikiba.se/ontology#label>   {
#     <http://www.bigdata.com/rdf#serviceParam>  <http://wikiba.se/ontology#language>  "en,en".
#   }
# }
# LIMIT 100
#
#
# look_for e.g. "http://www.w3.org/ns/prov#wasDerivedFrom"


def scenario_ref_value_occurrences(json_object, look_for, _):
    where = json_object["where"]

    # find scenarios 'ref value'

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:
        if "http://www.wikidata.org/prop/reference/value" in str(where_part):
            # there may be more than one
            result += str(where_part).count("http://www.wikidata.org/prop/reference/value")

    return result
