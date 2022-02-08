import os

TIMEFRAMES = [
    "2017-06-12_2017-07-09_organic",
    "2017-07-10_2017-08-06_organic",
    "2017-08-07_2017-09-03_organic",
    "2017-12-03_2017-12-30_organic",
    "2018-01-01_2018-01-28_organic",
    "2018-01-29_2018-02-25_organic",
    "2018-02-26_2018-03-25_organic"
]

# creates the structure of folders in /data, needed for the project
def create_dir_structure_of_data():
    # directory structure for data/
    data_dir = [
        "./data/statistical_information",

        "./data/statistical_information/query_research",
        "./data/statistical_information/query_research/redundant",
        "./data/statistical_information/query_research/non_redundant",



        "./data/statistical_information/query_research/redundant/reference_metadata",
        "./data/statistical_information/query_research/redundant/reference_metadata/raw_counted_properties",


        "./data/statistical_information/query_research/redundant/reference_metadata/recommended",
        "./data/statistical_information/query_research/redundant/reference_metadata/recommended/properties",
        "./data/statistical_information/query_research/redundant/reference_metadata/recommended/facets",
        "./data/statistical_information/query_research/redundant/reference_metadata/recommended/accumulated_facets",
        "./data/statistical_information/query_research/redundant/reference_metadata/recommended/datatypes",
        "./data/statistical_information/query_research/redundant/reference_metadata/recommended/accumulated_datatypes",

        "./data/statistical_information/query_research/redundant/reference_metadata/non_recommended",
        "./data/statistical_information/query_research/redundant/reference_metadata/non_recommended/properties",
        "./data/statistical_information/query_research/redundant/reference_metadata/non_recommended/facets",
        "./data/statistical_information/query_research/redundant/reference_metadata/non_recommended/accumulated_facets",
        "./data/statistical_information/query_research/redundant/reference_metadata/non_recommended/datatypes",
        "./data/statistical_information/query_research/redundant/reference_metadata/non_recommended/accumulated_datatypes",
        

        "./data/statistical_information/query_research/redundant/qualifier_metadata",
        "./data/statistical_information/query_research/redundant/qualifier_metadata/raw_counted_properties",

        "./data/statistical_information/query_research/redundant/qualifier_metadata/recommended",
        "./data/statistical_information/query_research/redundant/qualifier_metadata/recommended/properties",
        "./data/statistical_information/query_research/redundant/qualifier_metadata/recommended/facets",
        "./data/statistical_information/query_research/redundant/qualifier_metadata/recommended/accumulated_facets",
        "./data/statistical_information/query_research/redundant/qualifier_metadata/recommended/datatypes",
        "./data/statistical_information/query_research/redundant/qualifier_metadata/recommended/accumulated_datatypes",

        "./data/statistical_information/query_research/redundant/qualifier_metadata/non_recommended",
        "./data/statistical_information/query_research/redundant/qualifier_metadata/non_recommended/properties",
        "./data/statistical_information/query_research/redundant/qualifier_metadata/non_recommended/facets",
        "./data/statistical_information/query_research/redundant/qualifier_metadata/non_recommended/accumulated_facets",
        "./data/statistical_information/query_research/redundant/qualifier_metadata/non_recommended/datatypes",
        "./data/statistical_information/query_research/redundant/qualifier_metadata/non_recommended/accumulated_datatypes",


        "./data/statistical_information/query_research/redundant/rank_metadata",



        "./data/statistical_information/wikidata_research",
        "./data/statistical_information/wikidata_research/properties",
        "./data/statistical_information/wikidata_research/facets",
        "./data/statistical_information/wikidata_research/accumulated_facets",
        "./data/statistical_information/wikidata_research/datatypes",
        "./data/statistical_information/wikidata_research/accumulated_datatypes",



        "./data/statistical_information/query_research/non_redundant/reference_metadata",
        "./data/statistical_information/query_research/non_redundant/reference_metadata/raw_counted_properties",


        "./data/statistical_information/query_research/non_redundant/reference_metadata/recommended",
        "./data/statistical_information/query_research/non_redundant/reference_metadata/recommended/properties",
        "./data/statistical_information/query_research/non_redundant/reference_metadata/recommended/facets",
        "./data/statistical_information/query_research/non_redundant/reference_metadata/recommended/accumulated_facets",
        "./data/statistical_information/query_research/non_redundant/reference_metadata/recommended/datatypes",
        "./data/statistical_information/query_research/non_redundant/reference_metadata/recommended/accumulated_datatypes",

        "./data/statistical_information/query_research/non_redundant/reference_metadata/non_recommended",
        "./data/statistical_information/query_research/non_redundant/reference_metadata/non_recommended/properties",
        "./data/statistical_information/query_research/non_redundant/reference_metadata/non_recommended/facets",
        "./data/statistical_information/query_research/non_redundant/reference_metadata/non_recommended/accumulated_facets",
        "./data/statistical_information/query_research/non_redundant/reference_metadata/non_recommended/datatypes",
        "./data/statistical_information/query_research/non_redundant/reference_metadata/non_recommended/accumulated_datatypes",


        "./data/statistical_information/query_research/non_redundant/qualifier_metadata",
        "./data/statistical_information/query_research/non_redundant/qualifier_metadata/raw_counted_properties",


        "./data/statistical_information/query_research/non_redundant/qualifier_metadata/recommended",
        "./data/statistical_information/query_research/non_redundant/qualifier_metadata/recommended/properties",
        "./data/statistical_information/query_research/non_redundant/qualifier_metadata/recommended/facets",
        "./data/statistical_information/query_research/non_redundant/qualifier_metadata/recommended/accumulated_facets",
        "./data/statistical_information/query_research/non_redundant/qualifier_metadata/recommended/datatypes",
        "./data/statistical_information/query_research/non_redundant/qualifier_metadata/recommended/accumulated_datatypes",

        "./data/statistical_information/query_research/non_redundant/qualifier_metadata/non_recommended",
        "./data/statistical_information/query_research/non_redundant/qualifier_metadata/non_recommended/properties",
        "./data/statistical_information/query_research/non_redundant/qualifier_metadata/non_recommended/facets",
        "./data/statistical_information/query_research/non_redundant/qualifier_metadata/non_recommended/accumulated_facets",
        "./data/statistical_information/query_research/non_redundant/qualifier_metadata/non_recommended/datatypes",
        "./data/statistical_information/query_research/non_redundant/qualifier_metadata/non_recommended/accumulated_datatypes",


        "./data/statistical_information/query_research/non_redundant/rank_metadata"
    ]


    # delete the "organic" form the timeframes
    for TIMEFRAME in TIMEFRAMES:
        data_dir.append("./data/" + TIMEFRAME[:21])
        data_dir.append("./data/statistical_information/redundant_detection/" + TIMEFRAME[:21])
        data_dir.append("./data/statistical_information/redundant_detection/" + TIMEFRAME[:21] + "/qualifier_metadata")
        data_dir.append("./data/statistical_information/redundant_detection/" + TIMEFRAME[:21] + "/reference_metadata")
        data_dir.append("./data/statistical_information/redundant_detection/" + TIMEFRAME[:21] + "/rank_metadata")

    # directory structure for one timeframe directory
    timeframe_dir = [
        "organic/qualifier_metadata",
        "organic/rank_metadata",
        "organic/reference_metadata",
        "organic/statistical_information"
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
        "statistical_information/redundant",
        "statistical_information/non_redundant",
        "statistical_information"
    ]
    # directory structure for qualifier metadata
    qualifier_dir = [
        "failed_queries",
        "property_qualifier",
        "scenarios",
        "statistical_information/redundant",
        "statistical_information/non_redundant",
        "statistical_information"
    ]
    # directory structure for rank metadata
    rank_dir = [
        "failed_queries",
        "scenarios",
        "statistical_information",
        "statistical_information/redundant",
        "statistical_information/non_redundant",
        "rank_property",
        "best_rank_+_rank_property",
        "normal_rank_+_rank_property",
        "deprecated_rank_+_rank_property",
        "best_+_normal_rank_+_rank_property",
        "best_+_deprecated_rank_+_rank_property",
        "normal_+_deprecated_rank_+_rank_property",
        "all_ranks_+_rank_property",
        "normal_rank",
        "deprecated_rank",
        "best_rank",
        "best_+_normal_rank",
        "best_+_deprecated_rank",
        "normal_+_deprecated_rank",
        "all_ranks"
    ]

    # directory structure for the statistical information per timeframe
    statistical_information_dir = [
        "redundant",
        "non_redundant"
    ]

    # directory structure for the redundant / non-redundant information in the statistical information folder
    statistical_information_redundancy_dir = [
        "rank_metadata",
        
        "qualifier_metadata/raw_counted_properties",
        "reference_metadata/raw_counted_properties",

        "qualifier_metadata/recommended",
        "reference_metadata/recommended",
        "qualifier_metadata/recommended/properties",
        "reference_metadata/recommended/properties",
        "qualifier_metadata/recommended/facets",
        "reference_metadata/recommended/facets",
        "qualifier_metadata/recommended/datatypes",
        "reference_metadata/recommended/datatypes",
        "qualifier_metadata/recommended/accumulated_facets",
        "reference_metadata/recommended/accumulated_facets",
        "qualifier_metadata/recommended/accumulated_datatypes",
        "reference_metadata/recommended/accumulated_datatypes",

        "qualifier_metadata/non_recommended",
        "reference_metadata/non_recommended",
        "qualifier_metadata/non_recommended/properties",
        "reference_metadata/non_recommended/properties",
        "qualifier_metadata/non_recommended/facets",
        "reference_metadata/non_recommended/facets",
        "qualifier_metadata/non_recommended/datatypes",
        "reference_metadata/non_recommended/datatypes",
        "qualifier_metadata/non_recommended/accumulated_facets",
        "reference_metadata/non_recommended/accumulated_facets",
        "qualifier_metadata/non_recommended/accumulated_datatypes",
        "reference_metadata/non_recommended/accumulated_datatypes",

        "qualifier_metadata/all",
        "reference_metadata/all",
        "qualifier_metadata/all/properties",
        "reference_metadata/all/properties",
        "qualifier_metadata/all/facets",
        "reference_metadata/all/facets",
        "qualifier_metadata/all/datatypes",
        "reference_metadata/all/datatypes",
        "qualifier_metadata/all/accumulated_facets",
        "reference_metadata/all/accumulated_facets",
        "qualifier_metadata/all/accumulated_datatypes",
        "reference_metadata/all/accumulated_datatypes"
    ]

    # directory structure for scenarios
    scenarios_dir = [
        "redundant",
        "non_redundant"
    ]

    # directory structure for scenarios
    scenarios_redundancy_dir = [
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
        "seven",
        "six",
        "subselect",
        "ten",
        "three",
        "twelve",
        "two",
        "union",
        "values",
        "service"
    ]

    # check if the directories exist
    # .. and if not, create them
    for directory in data_dir:

        if "statistical_information" not in directory:

            if not os.path.isdir(directory):
                os.makedirs(directory)

            for directory_U in timeframe_dir:
                tmp_diretory = directory + "/" + directory_U
                if not os.path.isdir(tmp_diretory):
                    os.makedirs(tmp_diretory)

                # path for the statistical information:
                if directory_U == "organic/statistical_information":
                    for directory_U_U in statistical_information_dir:
                        tmp_directory = directory + "/" + directory_U + "/" + directory_U_U
                        if not os.path.isdir(tmp_directory):
                            os.makedirs(tmp_directory)
                        # for the folders inside the redundant / non redundant folders
                        for directory_U_U_U in statistical_information_redundancy_dir:
                            tmp_directory = directory + "/" + directory_U + "/" + directory_U_U + "/" + directory_U_U_U
                            if not os.path.isdir(tmp_directory):
                                os.makedirs(tmp_directory)

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

                                 # for the folders in the redundancies
                                for directory_U_U_U_U in scenarios_redundancy_dir:
                                    tmp_directory = directory + "/" + directory_U + "/" + directory_U_U + "/" + \
                                                    directory_U_U_U + "/" + directory_U_U_U_U
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

                                 # for the folders in the redundancies
                                for directory_U_U_U_U in scenarios_redundancy_dir:
                                    tmp_directory = directory + "/" + directory_U + "/" + directory_U_U + "/" + \
                                                    directory_U_U_U + "/" + directory_U_U_U_U
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

                                 # for the folders in the redundancies
                                for directory_U_U_U_U in scenarios_redundancy_dir:
                                    tmp_directory = directory + "/" + directory_U + "/" + directory_U_U + "/" + \
                                                    directory_U_U_U + "/" + directory_U_U_U_U
                                    if not os.path.isdir(tmp_directory):
                                        os.makedirs(tmp_directory)

        # add the statistical_information for the whole project to 'data'
        else:
            if not os.path.isdir(directory):
                os.makedirs(directory)


def is_already_extracted():
    return


# delete the identified scenarios in the specific folders of all the handed
# .. over timeframes
def delete_identified_scenarios():
    # directory structure for scenarios
    scenarios_dir = [
        "redundant",
        "non_redundant"
    ]

    # directory structure for scenarios
    scenarios_redundancy_dir = [
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
        "seven",
        "six",
        "subselect",
        "ten",
        "three",
        "twelve",
        "two",
        "union",
        "values",
        "service"
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

            for redundancy_scenario in scenarios_redundancy_dir:

                # iterate over all files
                for file in os.listdir(tmp_path_to_reference_scenarios + scenario + "/" + redundancy_scenario):
                    os.remove(tmp_path_to_reference_scenarios + scenario  + "/" + redundancy_scenario + "/" + file)
                for file in os.listdir(tmp_path_to_qualifier_scenarios + scenario  + "/" + redundancy_scenario):
                    os.remove(tmp_path_to_qualifier_scenarios + scenario  + "/" + redundancy_scenario + "/" + file)
                for file in os.listdir(tmp_path_to_rank_scenarios + scenario  + "/" + redundancy_scenario):
                    os.remove(tmp_path_to_rank_scenarios + scenario  + "/" + redundancy_scenario + "/" + file)

            # delete the found scenarios "inside" the bind scenarios
            if os.path.isfile(tmp_path_to_rank_scenarios + scenario + "/" + "bind_statistical_information.json"):
                os.remove(tmp_path_to_rank_scenarios + scenario + "/" + "bind_statistical_information.json")
            if os.path.isfile(tmp_path_to_qualifier_scenarios + scenario + "/" + "bind_statistical_information.json"):
                os.remove(tmp_path_to_qualifier_scenarios + scenario + "/" + "bind_statistical_information.json")
            if os.path.isfile(tmp_path_to_reference_scenarios + scenario + "/" + "bind_statistical_information.json"):
                os.remove(tmp_path_to_reference_scenarios + scenario + "/" + "bind_statistical_information.json")


    return
# Maybe a class here?