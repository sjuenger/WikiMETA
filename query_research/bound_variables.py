import glob
import json

# to hand over the bound variables of a quuery
# e.g. ["var4", "<http://www.w3.org/ns/prov#wasDerivedFrom>"]
# for :
#SELECT ?var1  ?var2Label  ?var3
#WHERE {
#  BIND (  <http://www.w3.org/ns/prov#wasDerivedFrom>  AS  ?var4 ).
#  ?var5  ?var6  ?var4 .
#  ?var5  <http://www.w3.org/1999/02/22-rdf-syntax-ns#type>  <http://wikiba.se/ontology#Property> .
#  ?var5  <http://www.wikidata.org/prop/direct/P1659>  ?var1 .
#  ?var1  <http://www.w3.org/2000/01/rdf-schema#label>  ?var2Label .
#  ?var1  <http://schema.org/description>  ?var3 .
# FILTER (  ( (  LANG (  ?var2Label  )  =  "en" ) )
#) .
# FILTER (  ( (  LANG (  ?var3  )  =  "en" ) )
#) .
#}
#

def find_bound_variables(json_object):
    where = json_object["where"]

    # find BIND Variables
    bound_variables = []
    for where_part in where:
        if where_part["type"] == "bind":
            print(where_part)

            if "termType" in where_part["expression"]:
                if where_part["expression"]["termType"] == "NamedNode":
                    if where_part["variable"]["termType"] == "Variable":
                        bound_variables.append(
                            (where_part["variable"]["value"], where_part["expression"]["value"]))
                print("Bound Variables: ")
                print(bound_variables)

                # TODO: Declare a reference in bound variables as an own scenario
                # TODO: Change this bound variables tuple arry to a dictionary to get rid of the .__str__()

    return bound_variables
