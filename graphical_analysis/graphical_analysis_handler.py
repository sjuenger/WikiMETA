import graphical_analysis.wikidata_analysis as wikidata_analysis
import graphical_analysis.redundant_detection_analysis as redundant_detection_analysis
import graphical_analysis.query_metadata_percentage as query_metadata_percentage

def start_graphical_analysis():

    wikidata_analysis.plot_top_wikidata_research_properties()
    wikidata_analysis.plot_top_wikidata_research_accumulated_facets()
    wikidata_analysis.plot_top_wikidata_research_accumulated_datatypes()

    redundant_detection_analysis.plot_redundant_detection_data_exact()

    query_metadata_percentage.display_percentage_queries_with_metadata()



