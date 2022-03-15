import os

import wikidata_research.dictionary.txt_to_dict as txt_to_dict
import wikidata_research.dictionary_evaluation_handler as wikidata_property_dictionary_evaluation_handler
import utilities.directory_structure_handler as directory_structure_handler

import query_research.query_research_handler as query_research_handler

import query_research.transform_data.redundant_detection as redundant_detection

import graphical_analysis.graphical_analysis_handler as graphical_analysis_handler


# TODO: Add a method, that automatically extracts the entries from SQID + the 5 missing properties from Wikidata Property Talk
# + stated IN, Retrieved, Reference URL, instance of, series ordinal ! .... fehlen in SQID
# TODO: Also add in that method, to automatically download the data from the SAPRQL logs
# TODO: Add references a https://sqid.toolforge.org/#/ to the code


def main():
    #directory_structure_handler.create_dir_structure_of_data()
    #directory_structure_handler.delete_identified_scenarios()

    #do_wikidata_research_stuff(15)

    #do_query_research_stuff([0,0,1,1,1,0,1], 15)
    #do_query_research_stuff([0,0,0,0,1,0,0], 15)
    #do_query_research_stuff([0,1,0,0,0,0,0], 15)

    analyse_research_stuff(15)

    # the ALL is missing with the recommmended / non_recommended things

    # summarize the statistical information on the redundant queries
    #

def do_wikidata_research_stuff(x):
    # Wikidata Stuff
    if not os.path.isfile("data/property_dictionary.json"):
        txt_to_dict.get_dict()

    wikidata_property_dictionary_evaluation_handler.generate_information_of_property_dictionary(x, "reference")
    wikidata_property_dictionary_evaluation_handler.generate_information_of_property_dictionary(x, "qualifier")


def do_query_research_stuff(args, x):

    query_research_handler.start_research_of_query_data(args, x)

            # TODO: Add properties to the recommended / non-recommended thing
            # TODO: Summarize the query information per timeframe to a property information over all timeframes
            # TODO: move the code of the WIKIDATA....module to the statistical_information_handler
            #
            # TODO: Try th redundant detection
            # TODO: Divide the query_research data even more into "with_redundancies" and "without_redundancies"
            #
            # TODO: get the 'total datatypes and facets' right -> also accumulatenthem

def analyse_research_stuff(x):
    graphical_analysis_handler.start_graphical_analysis(x)



if __name__ == "__main__":
    main()