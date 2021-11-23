# Statistics based on data dump 11/8/2021
# https://sqid.toolforge.org/#/browse?type=properties
import property_to_facets_WD

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

            # ... and put it into a dictionary
            property_qualifer_reference_facets[PID] = (statements_no, qualifiers_no, reference_no, facets)

            print(PID)
            print(statements_no)
            print(qualifiers_no)
            print(reference_no)

            print(property_qualifer_reference_facets)







property_qualifier_reference = {
    "P1476" : (63990, 1736182),
    "P577"  : (484233, 2862002),
    "P1433" : (6783, 12032),
    "P304"  : (428675, 108772),
    "P478" : (173416, 11760),
    "P1215" : (1, 0),
    "P433" : (31350, 14837),
    "P528" : (16615, 4456),
    "P356" : (20328, 167652),
    "P50" : (14820, 8963),
    "P921" : (1343, 104),
    "P17" : (75004, 25),
    "P407" : (1082869, 1730903),
    "P131" : (146847, 30),
    "P2215" : (1,0),
    "P106" : (135068, 171),
    "P625" : (118920, 247),
    "P30382" : (1,2)
}
# Statistics based on data dump 11/8/2021