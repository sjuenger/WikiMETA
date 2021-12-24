import os


# creates the structure of folders in /data, needed for the project
def create_dir_structure_of_data(TIMEFRAMES):
    # directory structure for data/
    data_dir = []
    # delete the "organic" form the timeframes
    for TIMEFRAME in TIMEFRAMES:
        data_dir.append("./data/" + TIMEFRAME[:21])

    # directory structure for one timeframe directory
    timeframe_dir = [
        "organic/qualifier_metadata",
        "organic/rank_metadata",
        "organic/reference_metadata"
    ]

    # directory structure for reference metadata
    reference_dir = [
        "all_three",
        "derived_+_reference_node",
        "derived_+_reference_property",
        "failed_queries",
        "only_derived",
        "only_reference_node",
        "only_reference_property",
        "reference_node_+_reference_property",
        "scenarios",
        "statistical_information"
    ]
    # directory structure for qualifier metadata
    qualifier_dir = [
        "failed_queries",
        "property_qualifier",
        "scenarios",
        "statistical_information"
    ]
    # directory structure for rank metadata
    rank_dir = [
        "failed_queries",
        "wikibase_rank",
        "scenarios",
        "statistical_information"
    ]

    # directory structure for scenarios
    scenarios_dir = [
        "bind",
        "blank_node",
        "eight",
        "eleven",
        "filter",
        "five",
        "four",
        "group",
        "literal",
        "minus",
        "nine",
        "one",
        "optional",
        "other",
        "prop_path",
        "ref_value",
        "seven",
        "six",
        "subselect",
        "ten",
        "three",
        "twelve",
        "two",
        "union"
    ]

    # check if the directories exist
    # .. and if not, create them
    for directory in data_dir:
        if not os.path.isdir(directory):
            os.makedirs(directory)

        for directory_U in timeframe_dir:
            tmp_diretory = directory + "/" + directory_U
            if not os.path.isdir(tmp_diretory):
                os.makedirs(tmp_diretory)

            # path for references:
            if directory_U == "organic/reference_metadata":
                for directory_U_U in reference_dir:
                    tmp_directory = directory + "/" + directory_U + "/" + directory_U_U
                    if not os.path.isdir(tmp_directory):
                        os.makedirs(tmp_directory)

                    # path for scenarios
                    if directory_U_U == "scenarios":
                        for directory_U_U_U in scenarios_dir:
                            tmp_directory = directory + "/" + directory_U + "/" + directory_U_U + "/" + directory_U_U_U
                            if not os.path.isdir(tmp_directory):
                                os.makedirs(tmp_directory)

            # path for qualifiers:
            if directory_U == "organic/qualifier_metadata":
                for directory_U_U in qualifier_dir:
                    tmp_directory = directory + "/" + directory_U + "/" + directory_U_U
                    if not os.path.isdir(tmp_directory):
                        os.makedirs(tmp_directory)

                    # path for scenarios
                    if directory_U_U == "scenarios":
                        for directory_U_U_U in scenarios_dir:
                            tmp_directory = directory + "/" + directory_U + "/" + directory_U_U + "/" + directory_U_U_U
                            if not os.path.isdir(tmp_directory):
                                os.makedirs(tmp_directory)

            # path for qualifiers:
            if directory_U == "organic/rank_metadata":
                for directory_U_U in rank_dir:
                    tmp_directory = directory + "/" + directory_U + "/" + directory_U_U
                    if not os.path.isdir(tmp_directory):
                        os.makedirs(tmp_directory)

                    # path for scenarios
                    if directory_U_U == "scenarios":
                        for directory_U_U_U in scenarios_dir:
                            tmp_directory = directory + "/" + directory_U + "/" + directory_U_U + "/" + directory_U_U_U
                            if not os.path.isdir(tmp_directory):
                                os.makedirs(tmp_directory)


def is_already_extracted():
    return


# delete the identified scenarios in the specific folders of all the handed
# .. over timeframes
def delete_identified_scenarios(TIMEFRAMES):
    # directory structure for scenarios
    scenarios_dir = [
        "bind",
        "blank_node",
        "eight",
        "eleven",
        "filter",
        "five",
        "four",
        "group",
        "literal",
        "minus",
        "nine",
        "one",
        "optional",
        "other",
        "prop_path",
        "ref_value",
        "seven",
        "six",
        "subselect",
        "ten",
        "three",
        "twelve",
        "two",
        "union"
    ]

    # loop through all different scenario directories and delete their content
    for TIMEFRAME in TIMEFRAMES:
        tmp_path_to_reference_scenarios = "./data/" + TIMEFRAME[:21] +\
                                "/organic/reference_metadata/scenarios/"
        tmp_path_to_qualifier_scenarios = "./data/" + TIMEFRAME[:21] +\
                                "/organic/qualifier_metadata/scenarios/"
        tmp_path_to_rank_scenarios = "./data/" + TIMEFRAME[:21] +\
                                "/organic/rank_metadata/scenarios/"

        for scenario in scenarios_dir:

            # iterate over all files
            for file in os.listdir(tmp_path_to_reference_scenarios + scenario):
                os.remove(tmp_path_to_reference_scenarios + scenario + "/" + file)
            for file in os.listdir(tmp_path_to_qualifier_scenarios + scenario):
                os.remove(tmp_path_to_qualifier_scenarios + scenario + "/" + file)
            for file in os.listdir(tmp_path_to_rank_scenarios + scenario):
                os.remove(tmp_path_to_rank_scenarios + scenario + "/" + file)



    return
# Maybe a class here?