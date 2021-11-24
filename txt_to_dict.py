# Statistics based on data dump 11/8/2021
# https://sqid.toolforge.org/#/browse?type=properties
import property_to_facets_WD
import property_is_qualifier

property_qualifer_reference_facets = {}

with open("data/SQID_properties_list.txt") as txt_list:
    for index in range(56160):
        if (index-1)%6 == 0: #title line
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

            # get the facets, attached to a property (if any)
            facets = property_to_facets_WD.getFacet(PID)

            # decide, whether the property is a qualifier or reference
            # according to the recommended properties of Wikidata
            qualifier = property_is_qualifier.is_qualifier(PID)

            # ... and put it into a dictionary
            property_qualifer_reference_facets[PID] = (statements_no, qualifiers_no, reference_no, facets, qualifier)

            print(PID)
            print(statements_no)
            print(qualifiers_no)
            print(reference_no)
            print(facets)
            print(qualifier)

            print(property_qualifer_reference_facets)


# Statistics based on data dump 11/8/2021