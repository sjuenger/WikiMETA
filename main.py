import sparql_to_json_references
import sparql_to_json_qualifiers
import sparql_to_json_ranks
import bound_references
import redundant_detection

# TODO: Add the whole list of data sources
LOCATION = "2017-06-12_2017-07-09_organic"
# TODO: Wirte a script, which build an directory structure fpr extractSPARQLtoJSON

sparql_to_json_qualifiers.extract_SPARQL_to_JSON(LOCATION)
#sparql_to_json_references.extract_SPARQL_to_JSON(LOCATION)
#sparql_to_json_ranks.extract_SPARQL_to_JSON(LOCATION)
#bound_references.find_bound_references(LOCATION)
#redundant_detection.delete_redundant_queries(LOCATION)
