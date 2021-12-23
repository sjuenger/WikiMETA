import os


# creates the structure of folders in /data, needed for the project
def create_dir_structure_of_data(TIMEFRAMES):

    # directory structure for data/
    data_dir = []
    # delete the "organic" form the timeframes
    for TIMEFRAME in TIMEFRAMES:
        data_dir.append(".data/" + TIMEFRAME[21:])

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
        "reference_node_+_reference_property"
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
        "proerty_qualifier",
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

        for directory in timeframe_dir:
            if not os.path.isdir(directory):
                os.makedirs(directory)

            # path for references:
            if directory == "organic/reference_metadata":
                for directory in reference_dir:
                    if not os.path.isdir(directory):
                        os.makedirs(directory)

                    # path for scenarios
                    if directory == "scenarios":
                        for directory in scenarios_dir:
                            if not os.path.isdir(directory):
                                os.makedirs(directory)

            # path for qualifiers:
            if directory == "organic/qualifier_metadata":
                for directory in qualifier_dir:
                    if not os.path.isdir(directory):
                        os.makedirs(directory)

                    # path for scenarios
                    if directory == "scenarios":
                        for directory in scenarios_dir:
                            if not os.path.isdir(directory):
                                os.makedirs(directory)

            # path for ranks:
            if directory == "organic/rank_metadata":
                for directory in rank_dir:
                    if not os.path.isdir(directory):
                        os.makedirs(directory)

                    # path for scenarios
                    if directory == "scenarios":
                        for directory in scenarios_dir:
                            if not os.path.isdir(directory):
                                os.makedirs(directory)


def is_already_extracted():
    return

def delete_gathered_data():
    return
# Maybe a class here?