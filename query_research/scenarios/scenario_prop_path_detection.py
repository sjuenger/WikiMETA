# method to detect scenario property path
#
#
#
# constellation for "wasDerivedFrom"
#
# scenario filter:
# ?s prov:wasDerivedFrom / ?p ?o .
#
#
#
# look_for e.g. "http://www.w3.org/ns/prov#wasDerivedFrom"

import json
import os

def scenario_prop_path_occurrences(json_object, look_for, location, bound_variables, look_for_additional_layer, data_type):
    where = json_object["where"]

    # find scenarios property path

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:

        if "type" in where_part and where_part["type"] == "bgp":
            for triple in where_part["triples"]:

                if ("type" in triple["predicate"]):
                    # on "normal" properties, there is only a 'termType' and no 'type'
                    if (triple["predicate"]["type"] == "path") :
                        if look_for in str(triple["predicate"]["items"]):
                            # TODO: add the bind variables here ?
                            #
                            # there may be more than one found item to look for
                            # e.g.
                            """SELECT ?var1  ?var2  ?var3  ?var3Label  ?var4  ?var5  ?var6  ?var7  ?var8
                            WHERE
                            {
                                VALUES(  ?var1  ) {
                                (< http: // www.wikidata.org / entity / Q100188 >)
                            }
                            ?var1 < http: // www.wikidata.org / prop / direct / P17 >  ?var3.
                                OPTIONAL
                            {
                                BIND(IRI(REPLACE(
                                    STR(  ?var2  ), STR( < http: // www.wikidata.org / prop / direct / >  ), STR( < http: // www.wikidata.org / prop / >  )  )  )  AS  ?var5 ).
                            BIND(IRI(REPLACE(
                                STR(  ?var2  ), STR( < http: // www.wikidata.org / prop / direct / >  ), STR( < http: // www.wikidata.org / prop / statement / >  )  )  )  AS  ?var6 ).
                            ?var1  ?var5  ?var4.
                            ?var4  ?var6  ?var3.
                            ?var4  ?var7  ?var8.
                                FILTER((STRSTARTS(STR(  ?var7),
                                STR( < http: // www.wikidata.org / prop / qualifier / >  )  ) & & !(STRSTARTS(STR(
                                                                                                   ?var7), STR( < http: // www.wikidata.org / prop / qualifier / value / >  )  ) ) )
                            ).
                            }
                            SERVICE < http: // wikiba.se / ontology  # label>   {
                                               < http: // www.bigdata.com / rdf
                            # serviceParam>  <http://wikiba.se/ontology#language>  "en".
                            }
                            }"""


                            result += str(triple["predicate"]["items"]).count(look_for)

                            # also look for the kind of the proppath and save it
                            # but ONLY do that, if the 'look_for_aditional_layer boolean is set to true
                            # (to prevent re-iteration)
                            if look_for_additional_layer:

                                # look, if there already exists a 'prop_path_operator_information'
                                if os.path.isfile(location + "/prop_path_statistical_information.json"):
                                    with open(location + "/prop_path_statistical_information.json", "r") as json_data:
                                        prop_path_statistical_information = json.load(json_data)
                                        json_data.close()
                                else:
                                    prop_path_statistical_information = \
                                        {
                                            "total_found_operators": 0,
                                            "found_operators_overall": {}}



                                # -> detect the operator of the prop_path
                                #
                                # e.g. "!", "/", aso.

                                if triple["predicate"]["pathType"] in prop_path_statistical_information[
                                    "found_operators_overall"]:
                                    prop_path_statistical_information["found_operators_overall"][
                                        triple["predicate"]["pathType"]] += 1
                                else:
                                    prop_path_statistical_information["found_operators_overall"][
                                        triple["predicate"]["pathType"]] = 1
                                prop_path_statistical_information["total_found_operators"] += 1

                                # do the same thing again -> but now, also for the datatypes
                                if data_type in prop_path_statistical_information:

                                    if triple["predicate"]["pathType"] in prop_path_statistical_information[
                                        data_type]:
                                        prop_path_statistical_information[data_type][
                                            triple["predicate"]["pathType"]] += 1
                                    else:
                                        prop_path_statistical_information[data_type][
                                            triple["predicate"]["pathType"]] = 1

                                else:
                                    prop_path_statistical_information[data_type] = {}
                                    prop_path_statistical_information[data_type][
                                        triple["predicate"]["pathType"]] = 1


                                # save the json object
                                with open(location + "/prop_path_statistical_information.json", "w") as json_data:
                                    json.dump(prop_path_statistical_information, json_data)
                                    json_data.close()
                                    # print(prop_path_statistical_information)

                    else:
                        if look_for in str(where_part):
                            raise Exception

    return result
