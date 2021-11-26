# Statistics based on data dump 11/8/2021
# https://sqid.toolforge.org/#/browse?type=properties
from time import sleep
import json

import wikidata_research.dictionary.property_to_facets_WD as property_to_facets_WD
import wikidata_research.dictionary.property_is_qualifier as property_is_qualifier


def get_dict():

    # a dictionary for all properties with the property PID (e.g. P1476) as the key
    prop_dict = {}

    # variable to count the referenes
    references_in_data = 0

    i = 0

    with open("data/SQID_properties_list.txt") as txt_list:
        for index in range(56160):

            if (index-1)%6 == 0: #title line

                # to counter the TIMEOUT of Wikidata
                sleep(2)

                title_complex_string = txt_list.readline()
                statements_no = txt_list.readline().strip("\n")
                txt_list.readline()
                qualifiers_no = txt_list.readline().strip("\n")
                txt_list.readline()
                reference_no = txt_list.readline().strip("\n")

                # extract the information and put it into a dictionary
                tmp = title_complex_string.split(" ")
                PID_with_brackets = tmp[tmp.__len__()-1].split("\t")[0]
                PID = PID_with_brackets.strip("(").strip(")");

                # a dictionary for every property with information about
                # KEY1: statments_no : Number of usage cases of the property in a statement
                # KEY2: qualifiers_no : Number of usage cases of the property as a qualifier
                # KEY3: references_no : Number of usage cases of the property in a refernce
                # KEY4: facet_of : list of every entity, that the property is a facet of
                # KEY5: qualifier_class : if the property is intended by wikidata to be used
                #                         as a qualifier -> here is the exact class(es)
                #                          e.g. "restrictive qualifier", ...
                # KEY6: is_reference : if the property is intended by Wikidata to be used
                #                       as a reference property -> true / false here
                #                       true: the property is a facet of:
                #                       'Wikipedia:Citing sources'
                values = {}

                # get the abstract items, of which the property is a facet (if of any)
                facet_of = property_to_facets_WD.getFacet(PID)

                # decide, whether the property is a qualifier or reference
                # according to the recommended properties of Wikidata
                qualifier = property_is_qualifier.is_qualifier(PID)

                # if the property if a facet of "Wikipedia:Citing sources" ->
                is_a_reference = facet_of.__contains__("Wikipedia:Citing sources")
                # -> the class "Wikidata property to indicate a source" is a facet of
                #          "Wikipedia:Citing sources"

                # ... and put it into the dictionary per property
                values["statement_no"] = statements_no
                values["qualifier_no"] = qualifiers_no
                values["reference_no"] = reference_no
                values["facet_of"] = facet_of
                values["qualifier_class"] = qualifier
                values["is_reference"] = is_a_reference

                # attach the dictionary per property to the general dictionary of all properties
                prop_dict[PID] = values

                i += 1
                if is_a_reference:
                    references_in_data += 1

                print(PID)
                print(facet_of)
                print(references_in_data)
                print(i)

    with open("data/property_dictionary.json", "wt") as result_data:
        json.dump(prop_dict, result_data)

    # Statistics based on data dump 11/8/2021