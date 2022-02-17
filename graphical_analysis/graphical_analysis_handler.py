import graphical_analysis.wikidata_analysis as wikidata_analysis
import graphical_analysis.redundant_detection_analysis as redundant_detection_analysis

def start_graphical_analysis():

    wikidata_analysis.plot_top_wikidata_research_properties()
    wikidata_analysis.plot_top_wikidata_research_accumulated_facets()
    wikidata_analysis.plot_top_wikidata_research_accumulated_datatypes()

    redundant_detection_analysis.plot_redundant_detection_data_exact()

