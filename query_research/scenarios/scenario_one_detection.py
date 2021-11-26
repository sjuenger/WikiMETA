
def is_scenario_one(json_object):
    where = json_object["where"]

    # find BIND Variables
    bound_variables = []
    for where_part in where:
        if where_part["type"] == "bind":
            # print(where_part)
            # print(json_data.name)

            if where_part["expression"]["type"] == "literal":
                if where_part["variable"]["termType"] == "Variable":
                    bound_variables.append(
                        (where_part["variable"]["value"], where_part["expression"]["value"]))
            print(bound_variables)

    # find scenario 1

    # multiple bgp (basic graph patterns)
    for where_part in where:

        if where_part["type"] == "bgp":
            for triple in where_part["triples"]:

                if (triple["subject"]["termType"] == "Variable") or ((triple["subject"]["value"])
                                                                     not in bound_variables):

                    # predicate might also be a path
                    if triple["predicate"]["termType"] is not None:

                        if (((triple["predicate"]["termType"] == "NamedNode" and
                              triple["predicate"]["value"] ==
                              "<http://www.w3.org/ns/prov#wasDerivedFrom>"))
                                or ((triple["predicate"]["termType"] == "Variable" and
                                     ((triple["predicate"]["value"],
                                       "<http://www.w3.org/ns/prov#wasDerivedFrom>")
                                      in bound_variables)))):

                            if (triple["object"]["termType"] == "Variable") or ((triple["object"]
                            ["value"]) not in bound_variables):
                                print("Stack Canary")
