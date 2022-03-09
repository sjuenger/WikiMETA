import graphical_analysis.wikidata_analysis as wikidata_analysis
import graphical_analysis.redundant_detection_analysis as redundant_detection_analysis
import graphical_analysis.query_metadata_percentage as query_metadata_percentage
import graphical_analysis.query_scenario_analysis as query_scenario_analysis
import graphical_analysis.properties_analysis as properties_analysis
import graphical_analysis.query_properties_accumulated_facets_analysis as \
    query_properties_accumulated_facets_analysis
import graphical_analysis.query_properties_accumulated_datatypes_analysis as \
    query_properties_accumulated_datatypes_analysis


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

    "reference_metadata/only_derived",
    "reference_metadata/only_reference_node",
    "reference_metadata/only_reference_property",
    "reference_metadata/derived_+_reference_node",
    "reference_metadata/derived_+_reference_property",
    "reference_metadata/reference_node_+_reference_property",
    "reference_metadata/all_three"
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



def start_graphical_analysis(x):

    wikidata_analysis.plot_top_wikidata_research_properties(x)
    wikidata_analysis.plot_top_wikidata_research_accumulated_facets(x)
    wikidata_analysis.plot_top_wikidata_research_accumulated_datatypes()

    redundant_detection_analysis.plot_redundant_detection_data_exact()

    query_metadata_percentage.display_percentage_queries_with_metadata()

    query_scenario_analysis.plot_timeframe_metadata_distribution_per_datatype(
        TIMEFRAMES, [DATA_TYPES_QUALIFIER, DATA_TYPES_REFERENCE, DATA_TYPES_RANK])

    query_scenario_analysis.plot_timeframe_metadata_distribution(TIMEFRAMES, "reference_metadata")
    query_scenario_analysis.plot_timeframe_metadata_distribution(TIMEFRAMES, "qualifier_metadata")
    query_scenario_analysis.plot_timeframe_metadata_distribution(TIMEFRAMES, "rank_metadata")

    for recommended_mode in ["recommended", "non_recommended", "all"]:
        for metadata_mode in ["reference_metadata", "qualifier_metadata"]:

            properties_analysis.plot_top_properties_timeframe(
                TIMEFRAMES, metadata_mode, recommended_mode, x)
            properties_analysis.plot_top_properties_overall(metadata_mode,
                                                            recommended_mode, x)
            properties_analysis.plot_top_properties_overall_percentage(
                metadata_mode, recommended_mode, x)

            query_properties_accumulated_facets_analysis.\
                plot_top_accumulated_facets_timeframe(TIMEFRAMES,
                                                      metadata_mode,
                                                      recommended_mode, x)
            query_properties_accumulated_facets_analysis.\
                plot_top_accumulated_facets_overall(metadata_mode, recommended_mode, x)
            query_properties_accumulated_facets_analysis.\
                plot_top_accumulated_facets_overall_percentage(metadata_mode,
                                                               recommended_mode, x)

            query_properties_accumulated_datatypes_analysis.\
                plot_top_accumulated_datatypes_timeframe(TIMEFRAMES,
                                                         metadata_mode,
                                                         recommended_mode)
            query_properties_accumulated_datatypes_analysis.\
                plot_top_accumulated_datatypes_overall(metadata_mode, recommended_mode)
            query_properties_accumulated_datatypes_analysis.\
                plot_top_accumulated_datatypes_overall_percentage(metadata_mode,
                                                                  recommended_mode)

