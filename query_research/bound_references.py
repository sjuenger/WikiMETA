import glob
import json

# to hand over the bound references to each scenario detection -> so, that is does not have to be done there

def find_bound_references(location):
    # Retrieve all files, ending with .json
    files_json_both = glob.glob("data/" + location[:21] + "/" +
                                location[22:] + "/both/*.json")
    files_json_only_derived = glob.glob("data/" + location[:21] + "/" +
                                        location[22:] + "/only_derived/*.json")
    files_json_only_reference = glob.glob("data/" + location[:21] + "/" +
                                          location[22:] + "/only_reference/*.json")

    i = 0
    # ! no proof for completeness
    for json_file in files_json_both:
        with open(json_file, "rt") as json_data:
            json_object = json.load(json_data)

            if json_object["queryType"] == "SELECT":
                # "bgp" = Basic Graph Pattern
                for where_part in json_object["where"]:
                    if where_part["type"] == "bgp":
                        triples = where_part["triples"]
                        for triple in triples:

                            # bound statement node -> reference node
                            if triple["subject"]["termType"] == "NamedNode":

                                # TODO, add the property path

                                if triple["predicate"]["termType"] == "NamedNode":
                                    if triple["predicate"]["value"] == "http://www.w3.org/ns/prov#wasDerivedFrom":
                                        bound_reference_file = "data/" + location[
                                                                         :21] + "/bound_references/" + json_file.split("/")[4]
                                        with open(bound_reference_file, "wt") as result_data:
                                            json.dump(json_object, result_data)
                                            i += 1
                                        result_data.close()


            print("f")
            print(i)
        json_data.close()
