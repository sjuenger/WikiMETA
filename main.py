import query_research.transform_data.sparql_to_json_references as sparql_to_json_references
import query_research.transform_data.sparql_to_json_qualifiers as sparql_to_json_qualifiers
import query_research.transform_data.sparql_to_json_ranks as sparql_to_json_ranks
import query_research.bound_references as bound_references
import query_research.redundant_detection as redundant_detection
import query_research.scenario_detection_unit as scenario_detection_unit
import wikidata_research.dictionary.txt_to_dict as txt_to_dict

# TODO: Add the whole list of data sources
TIMEFRAME_1 = "2017-06-12_2017-07-09_organic"
TIMEFRAME_2 = "2017-07-10_2017-08-06_organic"
TIMEFRAME_3 = "2017-08-07_2017-09-03_organic"
TIMEFRAME_4 = "2017-12-03_2017-12-30_organic"
TIMEFRAME_5 = "2018-01-01_2018-01-28_organic"
TIMEFRAME_6 = "2018-01-29_2018-02-25_organic"
TIMEFRAME_7 = "2018-02-26_2018-03-25_organic"

DATA_TYPES_REFERENCE = [
                        "reference_metadata/all_three",\
                        "reference_metadata/derived_+_reference_node",\
                        "reference_metadata/derived_+_reference_property",\
                        "reference_metadata/only_derived",\
                        "reference_metadata/only_reference_node",\
                        "reference_metadata/only_reference_property",\
                        "reference_metadata/reference_node_+_reference_property"
                        ]

#: Wirte a script, which build an directory structure fpr extractSPARQLtoJSON

# TODO: Add some modi here, like "Extraction",
#  "redundant_detection", "sitaution detection"...

#sparql_to_json_qualifiers.extract_SPARQL_to_JSON(LOCATION)

#sparql_to_json_references.extract_SPARQL_to_JSON(TIMEFRAME_2)

#sparql_to_json_ranks.extract_SPARQL_to_JSON(LOCATION)

#bound_references.find_bound_references(LOCATION)

#redundant_detection.delete_redundant_queries(LOCATION)

for DATA_TYPE in DATA_TYPES_REFERENCE:
    scenario_detection_unit.detect_scenarios(TIMEFRAME_2, DATA_TYPE)

#txt_to_dict.get_dict()
