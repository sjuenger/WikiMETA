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


def scenario_prop_path_occurrences(json_object, look_for, bound_variables):
    where = json_object["where"]

    # find scenarios property path

    result = False

    # multiple bgp (basic graph patterns)
    for where_part in where:

        if where_part["type"] == "bgp":
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
                            print(str(triple["predicate"]["items"]))

                    else:
                        if look_for in str(where_part):
                            raise Exception

    return result
