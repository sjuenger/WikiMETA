# get the facets on wikidata to a property on Wikidata (if available)
import SPARQLWrapper
import utilities

def getFacet(property_PID):

    sparql = SPARQLWrapper.SPARQLWrapper("https://query.wikidata.org/sparql")

    # can have a facet on different hierarchy levels - counting all
    # ?o2 can not be "entity" Q35120 (-> to prevent a chain of "subclass of" above
    # .. "wikidata property"

    sparql.setQuery("""
    SELECT ?facetLabel
    WHERE
    {
        wd:"""+ property_PID + """ wdt:P31 ?o .
        ?o wdt:P279* ?o2 .
        FILTER (!regex(STR(?o2), "Q35120"))
        ?o2 wdt:P1269 ?facet .
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
    }
    """)
    sparql.setReturnFormat(SPARQLWrapper.JSON)
    results = sparql.query().convert()

    facets = []

    for var in results['results']['bindings']:
        facet = var['facetLabel']['value']

        if not utilities.found_in_array(facet, facets):
            facets.append(facet)

        print(facets)

    return facets

