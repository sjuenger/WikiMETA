import query_research.transform_data.redundant_detection as redundant_detection
import query_research.transform_data.sparql_to_json_references as sparql_to_json_references
import query_research.transform_data.sparql_to_json_qualifiers as sparql_to_json_qualifiers
import query_research.transform_data.sparql_to_json_ranks as sparql_to_json_ranks
import query_research.transform_data.sarql_to_json_example_queries as sparql_to_json_example_queries

def start_creating_data(TIMEFRAMES, LOCATIONS):

    sparql_to_json_example_queries.extract_example_queries("Wikidata_Example_Queries")

    for timeframe in TIMEFRAMES:

        sparql_to_json_references(timeframe)
        sparql_to_json_qualifiers(timeframe)
        sparql_to_json_ranks(timeframe)

        for LOCATIONS_PER_METADATA in LOCATIONS:

            for location in LOCATIONS_PER_METADATA:

                redundant_detection.delete_redundant_queries(timeframe, location)

