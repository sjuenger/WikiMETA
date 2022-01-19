import wikidata_research.dictionary.dictionary_evaluation as dictionary_evaluation

# mode must either be "reference" or "qualifier"
# the x must by at least 1 or grater
def generate_information_of_property_dictionary(x, mode):

    if mode not in ["qualifier", "reference"]:
        error_message = "Not supported mode."
        raise Exception(error_message)
    if (type(x) != int or x < 1):
        error_message = "The number of requested top x items must be at least 1 or greater."
        raise Exception(error_message)

    dictionary_evaluation.get_top_x_metadata(x, mode)
    dictionary_evaluation.get_top_x_metadata(x, mode)
    dictionary_evaluation.get_top_x_metadata(x, mode, True)
    dictionary_evaluation.get_top_x_metadata(x, mode, True)
    dictionary_evaluation.get_top_x_metadata(x, mode, False)
    dictionary_evaluation.get_top_x_metadata(x, mode, False)

    dictionary_evaluation.get_top_x_facets_by_metadata(x, mode, True)
    dictionary_evaluation.get_top_x_facets_by_metadata(x, mode, False)
    dictionary_evaluation.get_top_x_facets_by_metadata(x, mode, True)
    dictionary_evaluation.get_top_x_facets_by_metadata(x, mode, False)
    dictionary_evaluation.get_top_x_facets_by_metadata(x, mode)
    dictionary_evaluation.get_top_x_facets_by_metadata(x, mode)

    # there are only 19 available datatypes for properties in Wikidata
    # -> no need for a top x functionality
    dictionary_evaluation.get_datatypes_by_metadata(mode, True)
    dictionary_evaluation.get_datatypes_by_metadata(mode, False)
    dictionary_evaluation.get_datatypes_by_metadata(mode, True)
    dictionary_evaluation.get_datatypes_by_metadata(mode, False)
    dictionary_evaluation.get_datatypes_by_metadata(mode)
    dictionary_evaluation.get_datatypes_by_metadata(mode)

    dictionary_evaluation.get_top_x_facets_by_accumulated_properties(x, mode, True)
    dictionary_evaluation.get_top_x_facets_by_accumulated_properties(x, mode, False)
    dictionary_evaluation.get_top_x_facets_by_accumulated_properties(x, mode, True)
    dictionary_evaluation.get_top_x_facets_by_accumulated_properties(x, mode, False)
    dictionary_evaluation.get_top_x_facets_by_accumulated_properties(x, mode)
    dictionary_evaluation.get_top_x_facets_by_accumulated_properties(x, mode)

    dictionary_evaluation.get_datatypes_by_accumulated_properties(mode, True)
    dictionary_evaluation.get_datatypes_by_accumulated_properties(mode, False)
    dictionary_evaluation.get_datatypes_by_accumulated_properties(mode, True)
    dictionary_evaluation.get_datatypes_by_accumulated_properties(mode, False)
    dictionary_evaluation.get_datatypes_by_accumulated_properties(mode)
    dictionary_evaluation.get_datatypes_by_accumulated_properties(mode)

