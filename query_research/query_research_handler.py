import query_research.transform_data.transform_data_handler as transform_data_handler
import query_research.scenario_detection_unit as scenario_detection_unit
import query_research.properties_counter as properties_counter
import query_research.statistical_information_handler as statistical_information_handler
import query_research.wikidata_dictionary_and_found_query_properties as wikidata_dictionary_and_found_query_properties
import query_research.ranks_counter as ranks_counter
import query_research.example_queries_in_data as example_queries_in_data
import query_research.amount_of_queries as amount_of_queries

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

def start_research_of_query_data(args, x):

    # use a bit-like structure to tell the function, what actions to perform

    # generate the data
    if args[0] == 1:
        transform_data_handler.\
            start_creating_data(TIMEFRAMES, [DATA_TYPES_REFERENCE, DATA_TYPES_QUALIFIER, DATA_TYPES_RANK])

    # count the amount of queries with and without metadata (overall & per timeframe)
    if args[1] == 1:
        amount_of_queries.save_total_of_queries_amount_per_timeframe(TIMEFRAMES,
                                                                               ["qualifier_metadata",
                                                                                "reference_metadata",
                                                                                "rank_metadata"])
        amount_of_queries.save_total_of_queries_amount_overall(TIMEFRAMES,
                                                                           ["qualifier_metadata",
                                                                            "reference_metadata",
                                                                            "rank_metadata"])

    # detect scenarios
    if args[2] == 1:

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

    # count the gathered properties and ranks
    if args[3] == 1:

        for timeframe in TIMEFRAMES:

            properties_counter.count_property_in(timeframe, "reference_metadata", DATA_TYPES_REFERENCE, "redundant")
            properties_counter.count_property_in(timeframe, "reference_metadata", DATA_TYPES_REFERENCE, "non_redundant")
            properties_counter.count_property_in(timeframe, "qualifier_metadata", DATA_TYPES_QUALIFIER, "redundant")
            properties_counter.count_property_in(timeframe, "qualifier_metadata", DATA_TYPES_QUALIFIER, "non_redundant")

            ranks_counter.count_ranks_in(timeframe, "rank_metadata", DATA_TYPES_RANK, "redundant")
            ranks_counter.count_ranks_in(timeframe, "rank_metadata", DATA_TYPES_RANK, "non_redundant")

    # create the statistical information about the counted properties in relation to the gathered facets/datatypes
    # .. from Wikidata
    if args[4] == 1:

        for timeframe in TIMEFRAMES:
            for metadata_mode in ["qualifier_metadata", "reference_metadata"]:
                for redundancy_mode in ["redundant", "non_redundant"]:

                    wikidata_dictionary_and_found_query_properties.\
                        create_dict_based_on_properties_dict_timeframe_and_Wikidata_property_dict_per_timeframe(
                        timeframe, metadata_mode, redundancy_mode)

                    for recommended_mode in [True, False, None]:

                        statistical_information_handler. \
                            get_top_x_counted_properties_timeframe(timeframe, x, metadata_mode,
                                                                   recommended_mode, redundancy_mode)

                        statistical_information_handler.\
                            get_top_x_counted_facets_timeframe(
                            timeframe, x, metadata_mode, recommended_mode, redundancy_mode)

                        statistical_information_handler.\
                            get_top_x_counted_datatypes_timeframe(
                            timeframe, x, metadata_mode, recommended_mode, redundancy_mode)

                        statistical_information_handler.\
                            get_top_x_counted_accumulated_facets_timeframe(
                            timeframe, x, metadata_mode, recommended_mode, redundancy_mode)

                        statistical_information_handler.\
                            get_top_x_counted_accumulated_datatypes_timeframe(
                            timeframe, x, metadata_mode, recommended_mode, redundancy_mode)

                        statistical_information_handler. \
                            get_top_x_counted_properties_timeframe(timeframe, x,
                                                                   metadata_mode, recommended_mode, redundancy_mode)

                        statistical_information_handler.\
                            get_top_x_counted_facets_timeframe(
                            timeframe, x, metadata_mode, recommended_mode, redundancy_mode)

                        statistical_information_handler.\
                            get_top_x_counted_datatypes_timeframe(
                            timeframe, x, metadata_mode, recommended_mode, redundancy_mode)

                        statistical_information_handler.\
                            get_top_x_counted_accumulated_facets_timeframe(
                            timeframe, x, metadata_mode, recommended_mode, redundancy_mode)

                        statistical_information_handler.\
                            get_top_x_counted_accumulated_datatypes_timeframe(
                            timeframe, x, metadata_mode, recommended_mode, redundancy_mode)


    # look for Wikidata Example Queries in the Query data
    if args[5] == 1:

        for timeframe in TIMEFRAMES:


            for (metadata_mode, datatype) in [("qualifier_metadata", DATA_TYPES_QUALIFIER),
                                              ("reference_metadata", DATA_TYPES_REFERENCE),
                                              ("rank_metadata", DATA_TYPES_RANK)]:

                # count the example queries from the Wikidata SPARQL Endpoint in ALL queries
                example_queries_in_data.\
                    count_example_queries_in_queries("Wikidata_Example_Queries",timeframe,
                                                         metadata_mode, datatype, False)
                # count the example queries from the Wikidata SPARQL Endpoint in
                # .. the 'marked as redundant' queries
                example_queries_in_data.\
                    count_example_queries_in_queries("Wikidata_Example_Queries",timeframe,
                                                         metadata_mode, datatype, True)

    # summarize the information about the timeframes
    if args[6] == 1:

        for timeframe in TIMEFRAMES:


            for (metadata_mode, datatype) in [("qualifier_metadata", DATA_TYPES_QUALIFIER),
                                              ("reference_metadata", DATA_TYPES_REFERENCE),
                                              ("rank_metadata", DATA_TYPES_RANK)]:

                for redundancy_mode in ["redundant", "non_redundant"]:

                        statistical_information_handler.\
                            summarize_statistical_information_about_scenarios(timeframe,
                                                                              datatype,
                                                                              metadata_mode,
                                                                              redundancy_mode)

        for datatype in [DATA_TYPES_QUALIFIER, DATA_TYPES_REFERENCE, DATA_TYPES_RANK]:

            # summarize the information about the detected / found Wikidata example queries in the data
            example_queries_in_data.summarize_scenario_data_from_metadata_per_datatype_and_overall(TIMEFRAMES, datatype, True)
            example_queries_in_data.summarize_scenario_data_from_metadata_per_datatype_and_overall(TIMEFRAMES, datatype, False)


        for redundancy_mode in ["redundant", "non_redundant"]:
            for metadata_mode in ["qualifier_metadata", "reference_metadata", "rank_metadata"]:
                statistical_information_handler.summarize_statistical_information_about_timeframes(TIMEFRAMES,
                                                                                                   metadata_mode,
                                                                                                   redundancy_mode)


            for metadata_mode in ["rank_metadata"]:

                statistical_information_handler.summarize_statistical_information_about_counted_ranks(TIMEFRAMES,
                                                                                                          metadata_mode,
                                                                                                          redundancy_mode)


            for metadata_mode in ["qualifier_metadata", "reference_metadata"]:

                statistical_information_handler.summarize_statistical_information_about_counted_raw_properties(TIMEFRAMES,
                                                                                                          metadata_mode,
                                                                                                          redundancy_mode)
                statistical_information_handler.\
                    get_top_x_counted_raw_properties_overall(x, metadata_mode, redundancy_mode)

                for recommended_mode in [True, False, None]:

                    statistical_information_handler.\
                        summarize_timeframe_information_about_properties_and_get_top_x(x,
                                                                                       TIMEFRAMES,
                                                                                       metadata_mode,
                                                                                       recommended_mode,
                                                                                       redundancy_mode)
                    statistical_information_handler.\
                        summarize_timeframe_information_about_facets_and_get_top_x(x,
                                                                                       TIMEFRAMES,
                                                                                       metadata_mode,
                                                                                       recommended_mode,
                                                                                       redundancy_mode)
                    statistical_information_handler.\
                        summarize_timeframe_information_about_datatypes(TIMEFRAMES,
                                                                                   metadata_mode,
                                                                                   recommended_mode,
                                                                                   redundancy_mode)

                    statistical_information_handler.\
                        summarize_timeframe_information_about_accumulated_facets_and_get_top_x(x,
                                                                                                   TIMEFRAMES,
                                                                                                   metadata_mode,
                                                                                                   recommended_mode,
                                                                                                   redundancy_mode)
                    statistical_information_handler.\
                        summarize_timeframe_information_about_accumulated_datatypes(TIMEFRAMES,
                                                                                               metadata_mode,
                                                                                               recommended_mode,
                                                                                               redundancy_mode)

