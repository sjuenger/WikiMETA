import query_research.transform_data.sparql_to_json_references as sparql_to_json_references
import query_research.transform_data.sparql_to_json_qualifiers as sparql_to_json_qualifiers
import query_research.transform_data.sparql_to_json_ranks as sparql_to_json_ranks
import query_research.bound_references as bound_references
import query_research.redundant_detection as redundant_detection
import query_research.scenarios.scenario_detection_unit as scenario_detection_unit
import wikidata_research.dictionary.txt_to_dict as txt_to_dict

# TODO: Add the whole list of data sources
LOCATION = "2017-06-12_2017-07-09_organic"
#DATA_TYPE = "reference_metadata/only_derived"
DATA_TYPE = "reference_metadata/only_reference_node"
#DATA_TYPE = "reference_metadata/only_reference_property"
#DATA_TYPE = "reference_metadata/derived_+_reference_property"
#: Wirte a script, which build an directory structure fpr extractSPARQLtoJSON

# TODO: Add some modi here, like "Extraction",
#  "redundant_detection", "sitaution detection"...

#sparql_to_json_qualifiers.extract_SPARQL_to_JSON(LOCATION)
#sparql_to_json_references.extract_SPARQL_to_JSON(LOCATION)
#sparql_to_json_ranks.extract_SPARQL_to_JSON(LOCATION)
#bound_references.find_bound_references(LOCATION)
#redundant_detection.delete_redundant_queries(LOCATION)
scenario_detection_unit.detect_scenarios(LOCATION, DATA_TYPE)
#txt_to_dict.get_dict()
