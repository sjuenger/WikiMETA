import sparql_to_json
import bound_references
import redundant_detection

# TODO: Add the whole list of data sources
LOCATION = "2017-06-12_2017-07-09_organic"
# TODO: Wirte a script, which build an directory structure fpr extractSPARQLtoJSON

sparql_to_json.extract_SPARQL_to_JSON(LOCATION)
bound_references.find_bound_references(LOCATION)
redundant_detection.delete_redundant_queries(LOCATION)
