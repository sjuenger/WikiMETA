# Statistics based on data dump 11/8/2021
# https://sqid.toolforge.org/#/browse?type=properties
from time import sleep
import json
import urllib

import wikidata_research.dictionary.property_to_facets_WD as property_to_facets_WD
import wikidata_research.dictionary.property_is_qualifier as property_is_qualifier


def get_dict():
    # a dictionary for all properties with the property PID (e.g. P1476) as the key
    prop_dict = {}

    # variable to count the referenes
    references_in_data = 0

    # variable to count the qualifiers
    qualifiers_in_data = 0

    i = 0

    with open("data/SQID_properties_list.txt") as txt_list:
        # iterate through all the lines
        for line_index, line in enumerate(txt_list):
            #
            title_complex_string = str(line)
            statements_no = txt_list.readline().strip("\n")
            txt_list.readline()
            qualifiers_no = txt_list.readline().strip("\n")
            txt_list.readline()
            reference_no = txt_list.readline().strip("\n")

            # extract the information and put it into a dictionary
            title_string_array = title_complex_string.split(" ")
            PID_with_brackets = title_string_array[title_string_array.__len__() - 1].split("\t")[0]
            PID = PID_with_brackets.strip("(").strip(")")
            datatype = title_string_array[title_string_array.__len__() - 1].split("\t")[1].strip("\n")

            title_string_array.pop()
            label = ' '.join(title_string_array).strip("\n")

            # a dictionary for every property with information about
            # KEY1: label : The name/label of the property
            # KEY2: datatype : The datatype of the property
            # KEY3: statments_no : Number of usage cases of the property in a statement
            # KEY4: qualifiers_no : Number of usage cases of the property as a qualifier
            # KEY5: references_no : Number of usage cases of the property in a refernce
            # KEY6: facet_of : list of every entity, that the property is a facet of
            # KEY7: qualifier_class : if the property is intended by wikidata to be used
            #                         as a qualifier -> here is the exact class(es)
            #                          e.g. "restrictive qualifier", ...
            # KEY8: is_reference : if the property is intended by Wikidata to be used
            #                       as a reference property -> true / false here
            #                       true: the property is a facet of:
            #                       'Wikipedia:Citing sources'
            values = {}

            # to counter the html TIMEOUT of Wikidata -> if a timeout occurs, just try it again after 2 sec
            successful = False
            while not successful:
                try:

                    # get the abstract items, of which the property is a facet (if of any)
                    facet_of = property_to_facets_WD.getFacet(PID)

                    # decide, whether the property is a qualifier or reference
                    # according to the recommended properties of Wikidata
                    qualifier = property_is_qualifier.is_qualifier(PID)

                    # if the property if a facet of "Wikipedia:Citing sources" ->
                    is_a_reference = facet_of.__contains__("Wikipedia:Citing sources")
                    # -> the class "Wikidata property to indicate a source" is a facet of
                    #          "Wikipedia:Citing sources"
                    successful = True

                except urllib.error.HTTPError:
                    sleep(2)
                    successful = False

            # ... and put it into the dictionary per property
            values["label"] = label
            values["datatype"] = datatype
            values["statement_no"] = statements_no
            values["qualifier_no"] = qualifiers_no
            values["reference_no"] = reference_no
            values["facet_of"] = facet_of
            values["qualifier_class"] = qualifier
            values["is_reference"] = is_a_reference

            # TODO: Think about doing a "Datatype" Analysis on the properties

            # attach the dictionary per property to the general dictionary of all properties
            prop_dict[PID] = values

            i += 1
            if is_a_reference:
                references_in_data += 1
            if qualifier != "":
                qualifiers_in_data += 1

            print("PID: ", PID)
            print("Label: ", label)
            print("Datatype: ", datatype)
            print("Facets found: ", facet_of)
            print("Total amount of references found: ", references_in_data)
            print("Total amount of qualifiers found: ", qualifiers_in_data)
            print("Total amount of properties: ", i)
            print("\n")


    with open("data/property_dictionary.json", "wt") as result_data:
        json.dump(prop_dict, result_data)

    txt_list.close()
    result_data.close()
    # Statistics based on data dump 11/8/2021
    # TODO: Add a comment for github here, explaining it.