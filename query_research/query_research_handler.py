import query_research.transform_data.transform_data_handler as transform_data_handler
import query_research.scenario_detection_unit as scenario_detection_unit
import query_research.properties_counter as properties_counter
import query_research.statistical_information_handler as statistical_information_handler
import query_research.wikidata_dictionary_and_found_query_properties as wikidata_dictionary_and_found_query_properties

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

def start_research_of_query_data(args):

    # use a bit-like structure to tell the function, what actions to perform

    # generate the data
    if args[0] == 1:
        transform_data_handler(TIMEFRAMES, [DATA_TYPES_REFERENCE, DATA_TYPES_QUALIFIER, DATA_TYPES_RANK])

    # detect scenarios
    if args[1] == 1:

        for timeframe in TIMEFRAMES:
           for datatype in DATA_TYPES_REFERENCE:
               scenario_detection_unit.detect_scenarios(timeframe, datatype, "redundant")
               scenario_detection_unit.detect_scenarios(timeframe, datatype, "non_redundant")

           for datatype in DATA_TYPES_QUALIFIER:
              scenario_detection_unit.detect_scenarios(timeframe, datatype, "redundant")
              scenario_detection_unit.detect_scenarios(timeframe, datatype, "non_redundant")

           for datatype in DATA_TYPES_RANK:
              scenario_detection_unit.detect_scenarios(timeframe, datatype, "redundant")
              scenario_detection_unit.detect_scenarios(timeframe, datatype, "non_redundant")

    # count the gathered properties
    if args[2] == 1:

        for timeframe in TIMEFRAMES:

           properties_counter.count_property_in(timeframe, "reference_metadata", DATA_TYPES_REFERENCE, "redundant")
           properties_counter.count_property_in(timeframe, "reference_metadata", DATA_TYPES_REFERENCE, "non_redundant")
           properties_counter.count_property_in(timeframe, "qualifier_metadata", DATA_TYPES_QUALIFIER, "redundant")
           properties_counter.count_property_in(timeframe, "qualifier_metadata", DATA_TYPES_QUALIFIER, "non_redundant")

    # create the statistical information about the counted properties in relation to the gathered facets/datatypes
    # .. from Wikidata
    if args[3] == 1:

        for timeframe in TIMEFRAMES:
            for metadata_mode in ["qualifier_metadata", "reference_metadata"]:
                for redundancy_mode in ["redundant", "non_redundant"]:
                    
                    wikidata_dictionary_and_found_query_properties.\
                        create_dict_based_on_properties_dict_timeframe_and_Wikidata_property_dict_per_timeframe(
                        timeframe, metadata_mode, redundancy_mode)

                    wikidata_dictionary_and_found_query_properties. \
                        get_top_x_counted_properties_timeframe(timeframe, 10, metadata_mode, redundancy_mode)

                    wikidata_dictionary_and_found_query_properties.\
                        get_top_x_counted_facets_timeframe(
                        timeframe, 10, metadata_mode, redundancy_mode)

                    wikidata_dictionary_and_found_query_properties.\
                        get_top_x_counted_datatypes_timeframe(
                        timeframe, 10, metadata_mode, redundancy_mode)

                    wikidata_dictionary_and_found_query_properties.\
                        get_top_x_counted_accumulated_facets_timeframe(
                        timeframe, 10, metadata_mode, redundancy_mode)

                    wikidata_dictionary_and_found_query_properties.\
                        get_top_x_counted_accumulated_datatypes_timeframe(
                        timeframe, 10, metadata_mode, redundancy_mode)

                    wikidata_dictionary_and_found_query_properties. \
                        get_top_x_counted_properties_timeframe(timeframe, 10, metadata_mode, True, redundancy_mode)
                    wikidata_dictionary_and_found_query_properties. \
                        get_top_x_counted_properties_timeframe(timeframe, 10, metadata_mode, False, redundancy_mode)

                    wikidata_dictionary_and_found_query_properties.\
                        get_top_x_counted_facets_timeframe(
                        timeframe, 10, metadata_mode, True, redundancy_mode)
                    wikidata_dictionary_and_found_query_properties. \
                        get_top_x_counted_facets_timeframe(
                        timeframe, 10, metadata_mode, False, redundancy_mode)

                    wikidata_dictionary_and_found_query_properties.\
                        get_top_x_counted_datatypes_timeframe(
                        timeframe, 10, metadata_mode, True, redundancy_mode)
                    wikidata_dictionary_and_found_query_properties. \
                        get_top_x_counted_datatypes_timeframe(
                        timeframe, 10, metadata_mode, False, redundancy_mode)

                    wikidata_dictionary_and_found_query_properties.\
                        get_top_x_counted_accumulated_facets_timeframe(
                        timeframe, 10, metadata_mode, True, redundancy_mode)
                    wikidata_dictionary_and_found_query_properties. \
                        get_top_x_counted_accumulated_facets_timeframe(
                        timeframe, 10, metadata_mode, False, redundancy_mode)

                    wikidata_dictionary_and_found_query_properties.\
                        get_top_x_counted_accumulated_datatypes_timeframe(
                        timeframe, 10, metadata_mode, True, redundancy_mode)
                    wikidata_dictionary_and_found_query_properties. \
                        get_top_x_counted_accumulated_datatypes_timeframe(
                        timeframe, 10, metadata_mode, False, redundancy_mode)


    # summarize the information about the timeframes
    if args[4] == 1:

        for timeframe in TIMEFRAMES:
           statistical_information_handler. \
               summarize_statistical_information_about_scenarios(timeframe,
                                                                 DATA_TYPES_REFERENCE,
                                                                 "reference_metadata", "redundant")
           statistical_information_handler. \
               summarize_statistical_information_about_scenarios(timeframe,
                                                                 DATA_TYPES_REFERENCE,
                                                                 "reference_metadata", "non_redundant")
           statistical_information_handler. \
              summarize_statistical_information_about_scenarios(timeframe,
                                                                 DATA_TYPES_QUALIFIER,
                                                                "qualifier_metadata", "redundant")
           statistical_information_handler. \
              summarize_statistical_information_about_scenarios(timeframe,
                                                                 DATA_TYPES_QUALIFIER,
                                                                "qualifier_metadata", "non_redundant")
           statistical_information_handler. \
              summarize_statistical_information_about_scenarios(timeframe,
                                                                 DATA_TYPES_RANK,
                                                                "rank_metadata", "redundant")
           statistical_information_handler. \
              summarize_statistical_information_about_scenarios(timeframe,
                                                                 DATA_TYPES_RANK,
                                                                "rank_metadata", "non_redundant")

        statistical_information_handler. \
          summarize_statistical_information_about_timeframes(TIMEFRAMES,
                                                             "reference_metadata", "redundant")
        statistical_information_handler. \
          summarize_statistical_information_about_timeframes(TIMEFRAMES,
                                                             "reference_metadata", "non_redundant")

        statistical_information_handler. \
          summarize_statistical_information_about_timeframes(TIMEFRAMES,
                                                             "qualifier_metadata", "redundant")
        statistical_information_handler. \
          summarize_statistical_information_about_timeframes(TIMEFRAMES,
                                                             "qualifier_metadata", "non_redundant")

        statistical_information_handler. \
          summarize_statistical_information_about_timeframes(TIMEFRAMES,
                                                             "rank_metadata", "redundant")
        statistical_information_handler. \
          summarize_statistical_information_about_timeframes(TIMEFRAMES,
                                                             "rank_metadata", "non_redundant")

        statistical_information_handler.\
          summarize_statistical_information_about_counted_properties(TIMEFRAMES, "qualifier_metadata", "redundant")
        statistical_information_handler.\
          summarize_statistical_information_about_counted_properties(TIMEFRAMES, "qualifier_metadata", "non_redundant")
        statistical_information_handler.\
          summarize_statistical_information_about_counted_properties(TIMEFRAMES, "reference_metadata", "redundant")
        statistical_information_handler.\
          summarize_statistical_information_about_counted_properties(TIMEFRAMES, "reference_metadata", "non_redundant")

        statistical_information_handler.\
          get_top_x_counted_properties_overall(10, "qualifier_metadata", "redundant")
        statistical_information_handler.\
          get_top_x_counted_properties_overall(10, "qualifier_metadata", "non_redundant")
        statistical_information_handler.\
          get_top_x_counted_properties_overall(10, "reference_metadata", "redundant")
        statistical_information_handler.\
          get_top_x_counted_properties_overall(10, "reference_metadata","non_redundant")
