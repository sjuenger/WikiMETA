import os

import wikidata_research.dictionary.txt_to_dict as txt_to_dict
import wikidata_research.dictionary_evaluation_handler as wikidata_property_dictionary_evaluation_handler
import utilities.directory_structure_handler as directory_structure_handler
import query_research.statistical_information_handler as statistical_information_handler
import query_research.scenario_detection_unit as scenario_detection_unit
import query_research.transform_data.redundant_detection as redundant_detection
import query_research.transform_data.sparql_to_json_references as sparql_to_json_references
import query_research.transform_data.sparql_to_json_qualifiers as sparql_to_json_qualifiers
import query_research.transform_data.sparql_to_json_ranks as sparql_to_json_ranks
import query_research.properties_counter as properties_counter

TIMEFRAMES = [
    "2017-06-12_2017-07-09_organic",
    "2017-07-10_2017-08-06_organic",
    "2017-08-07_2017-09-03_organic",
    "2017-12-03_2017-12-30_organic",
    "2018-01-01_2018-01-28_organic",
    "2018-01-29_2018-02-25_organic",
    "2018-02-26_2018-03-25_organic"
]

DATA_TYPES_REFERENCE = [
    "reference_metadata/all_three",
    "reference_metadata/derived_+_reference_node",
    "reference_metadata/derived_+_reference_property",
    "reference_metadata/only_derived",
    "reference_metadata/only_reference_node",
    "reference_metadata/only_reference_property",
    "reference_metadata/reference_node_+_reference_property"
]

DATA_TYPES_QUALIFIER = [
    "qualifier_metadata/property_qualifier"
]

DATA_TYPES_RANK = [
    "rank_metadata/rank_property",
    "rank_metadata/best_rank_+_rank_property",
    "rank_metadata/normal_rank_+_rank_property",
    "rank_metadata/deprecated_rank_+_rank_property",
    "rank_metadata/best_+_normal_rank_+_rank_property",
    "rank_metadata/best_+_deprecated_rank_+_rank_property",
    "rank_metadata/normal_+_deprecated_rank_+_rank_property",
    "rank_metadata/all_ranks_+_rank_property",
    "rank_metadata/normal_rank",
    "rank_metadata/deprecated_rank",
    "rank_metadata/best_rank",
    "rank_metadata/best_+_normal_rank",
    "rank_metadata/best_+_deprecated_rank",
    "rank_metadata/normal_+_deprecated_rank",
    "rank_metadata/all_ranks"
]

#: Wirte a script, which buils an directory structure fpr extractSPARQLtoJSON

# TODO: Add some modi here, like "Extraction",
#  "redundant_detection", "sitaution detection"...

# TODO: Add a method, that automatically extracts the entries from SQID + the 5 missing properties from Wikidata Property Talk
# + stated IN, Retrieved, Reference URL, instance of, series ordinal ! .... fehlen in SQID
# TODO: Also add in that method, to automatically download the data from the SAPRQL logs
# TODO: Add a GUI for the project
# TODO: Add references a https://sqid.toolforge.org/#/ to the code


#directory_structure_handler.create_dir_structure_of_data(TIMEFRAMES)
#directory_structure_handler.delete_identified_scenarios(TIMEFRAMES)

#for TIMEFRAME in TIMEFRAMES:
#    sparql_to_json_qualifiers.extract_SPARQL_to_JSON(TIMEFRAME)
#    sparql_to_json_references.extract_SPARQL_to_JSON(TIMEFRAME)
#    sparql_to_json_ranks.extract_SPARQL_to_JSON(TIMEFRAME)

# bound_references.find_bound_references(LOCATION)

# redundant_detection.delete_redundant_queries(LOCATION)

#for TIMEFRAME in TIMEFRAMES:
#    print("REFERENCES")
#    for DATA_TYPE in DATA_TYPES_REFERENCE:
#        scenario_detection_unit.detect_scenarios(TIMEFRAME, DATA_TYPE)
#    print("\n\n")
#    print("QUALIFIERS")
#    for DATA_TYPE in DATA_TYPES_QUALIFIER:
#       scenario_detection_unit.detect_scenarios(TIMEFRAME, DATA_TYPE)
#    print("\n\n")
#    print("RANKS")
#    for DATA_TYPE in DATA_TYPES_RANK:
#       scenario_detection_unit.detect_scenarios(TIMEFRAME, DATA_TYPE)
#    print("\n\n")

for TIMEFRAME in TIMEFRAMES:
    properties_counter.count_property_in(TIMEFRAME, "reference_metadata", DATA_TYPES_REFERENCE)
    properties_counter.count_property_in(TIMEFRAME, "qualifier_metadata", DATA_TYPES_QUALIFIER)

#if not os.path.isfile("data/property_dictionary.json"):
#    txt_to_dict.get_dict()

#wikidata_property_dictionary_evaluation_handler.generate_information_of_property_dictionary(10, "reference")
#wikidata_property_dictionary_evaluation_handler.generate_information_of_property_dictionary(10, "qualifier")

#for timeframe in TIMEFRAMES:
#    statistical_information_handler. \
#        summarize_statistical_information_about_scenarios(timeframe,
#                                                          DATA_TYPES_REFERENCE, "reference_metadata")
#    statistical_information_handler. \
#       summarize_statistical_information_about_scenarios(timeframe,
#                                                          DATA_TYPES_QUALIFIER, "qualifier_metadata")
#    statistical_information_handler. \
#       summarize_statistical_information_about_scenarios(timeframe,
#                                                          DATA_TYPES_RANK, "rank_metadata")


#statistical_information_handler. \
#    summarize_statistical_information_about_timeframes(TIMEFRAMES,
#                                                       "reference_metadata")
#statistical_information_handler. \
#    summarize_statistical_information_about_timeframes(TIMEFRAMES,
#                                                       "qualifier_metadata")
#statistical_information_handler. \
#    summarize_statistical_information_about_timeframes(TIMEFRAMES,
#                                                       "rank_metadata")
#for timeframe in TIMEFRAMES:
    #for location in DATA_TYPES_REFERENCE:
        #redundant_detection.delete_redundant_queries(timeframe, location)



