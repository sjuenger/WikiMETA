# method to detect scenario bind
#
#
#
# constellation for "wasDerivedFrom"
#
# scenario bind:
# BIND(EXISTS
# {
# ?var4 < http: // www.w3.org / ns / prov
# wasDerivedFrom>  ?var5 .
# }
# AS  ?var3 ).
#
#
#
# look_for e.g. "http://www.w3.org/ns/prov#wasDerivedFrom"


def scenario_bind_occurrences(json_object, look_for):
    where = json_object["where"]

    # find scenarios 'filter'

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:
        if where_part["type"] == "bind":
            # if the bind operation is not just an assignment to a variable
            # {'type': 'bind', 'variable': {'termType': 'Variable', 'value': 'var3'}, 'expression': {'type': 'operation', 'operator': 'exists', 'args': [{'type': 'bgp', 'triples': [{'subject': {'termType': 'Variable', 'value': 'var4'}, 'predicate': {'termType': 'NamedNode', 'value': 'http://www.w3.org/ns/prov#wasDerivedFrom'}, 'object': {'termType': 'Variable', 'value': 'var5'}}]}]}}
            # TODO: Which type of BIND? Exist, If, ...
            if "args" in where_part["expression"]:
                if (look_for in str(where_part["expression"]["args"])):
                    print("args " + where_part["expression"]["operator"])

                    # there may be more than one
                    result += str(where_part["expression"]["args"]).count(look_for)

            # if the bind operation is just an assignment to a variable
            # {'type': 'bind', 'variable': {'termType': 'Variable', 'value': 'var4'}, 'expression': {'termType': 'NamedNode', 'value': 'http://www.wikidata.org/prop/qualifier/P582'}}
            if "termType" in where_part["expression"]:
                print("termType")

                if (look_for in str(where_part["expression"]["value"])):

                    # there may be more than one
                    result += str(where_part["expression"]["value"]).count(look_for)

                # TODO: if that happens -> detect the scenario, the resultnig variable was in!

    # if result:
    # print(result)
    # print("Scenario 1")
    # print(where)

    return result