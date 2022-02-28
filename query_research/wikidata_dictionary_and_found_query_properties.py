import json

# create a list of the extracted properties and combine their facets to them -> using the property_dictionary.json
# .. from the wikidata_research
# .. per timeframe
#
def create_dict_based_on_properties_dict_timeframe_and_Wikidata_property_dict_per_timeframe(location, mode, redundant_mode):
    if mode not in ["qualifier_metadata", "reference_metadata"]:
        error_message = "Not supported mode: ", mode
        raise Exception(error_message)
    if redundant_mode not in ["redundant", "non_redundant"]:
        error_message = "Not supported redundancy mode: ", redundant_mode
        raise Exception(error_message)

    result_dict = {}
    result_dict["real_wikidata_properties"] = {}
    # in case, someone used a property, e.g. "P969", which is not a property anywhere to be found in Wikidata
    result_dict["false_wikidata_properties"] = {}

    path_to_stat_information = "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" \
                                   + redundant_mode + "/" + mode + "/raw_counted_properties/properties_counted.json"
    path_to_wikidata_property_dict = "data/property_dictionary.json"

    with open(path_to_stat_information, "r") as stat_info_file:
        stat_info = json.load(stat_info_file)
        with open(path_to_wikidata_property_dict, "r") as wikidata_props_file:
            wikidata_props = json.load(wikidata_props_file)

            for PID in stat_info["properties"]:


                # in case, a property mentioned in a query is in fact not a property to be found on Wikidata
                # NOTE: we can be sure, that the property_dictionary.json of the wikidata_research contains
                # ..  all of the properties, that could have been available at the time the query was prompted,
                # .. because, the data from SQID was extracted in 2022 and the queries are from 2017-2018
                #
                # of cours, someone might just accidentally chose a property PID, that was false in 2017-2018
                # .. but is in fact a property in 2022.
                # But, as far as I see this case, this problem is too hard to solve and will not have any significant
                # .. effect on the results of my analysis
                if(PID not in wikidata_props):
                    result_dict["false_wikidata_properties"][PID] = {}
                    result_dict["false_wikidata_properties"][PID]["occurrences"] = stat_info["properties"][PID]
                else:
                    result_dict["real_wikidata_properties"][PID] = {}
                    result_dict["real_wikidata_properties"][PID]["occurrences"] = stat_info["properties"][PID]
                    result_dict["real_wikidata_properties"][PID]["facets"] = wikidata_props[PID]["facet_of"]
                    result_dict["real_wikidata_properties"][PID]["label"] = wikidata_props[PID]["label"]
                    result_dict["real_wikidata_properties"][PID]["datatype"] = wikidata_props[PID]["datatype"]
                    result_dict["real_wikidata_properties"][PID]["is_reference"] = wikidata_props[PID]["is_reference"]
                    result_dict["real_wikidata_properties"][PID]["qualifier_class"] = wikidata_props[PID]["qualifier_class"]


    path_to_output = "data/" + location[:21] + "/" + location[22:] + "/statistical_information/" \
                                   + redundant_mode + "/" + mode + "/raw_counted_properties/properties_facets_and_datatypes.json"

    with open(path_to_output, "w") as result_data:
        json.dump(result_dict, result_data)


