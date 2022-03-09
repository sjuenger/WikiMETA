# get the abstract items on Wikidata, of which the property is a facet (if of any)
import SPARQLWrapper
import wikidata_research.dictionary.utilities as utilities


def getFacet(property_PID):

    sparql = SPARQLWrapper.SPARQLWrapper("https://query.wikidata.org/sparql")

    sparql.setQuery("""
    SELECT ?facetOFLabel
    WHERE
    {
        wd:"""+ property_PID + """ wdt:P31 ?o .
        ?o wdt:P1269 ?facetOF .
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
    }
    """)
    sparql.setReturnFormat(SPARQLWrapper.JSON)
    results = sparql.query().convert()

    facet_of = []

    for var in results['results']['bindings']:
        item = var['facetOFLabel']['value']

        if not utilities.found_in_array(item, facet_of):
            facet_of.append(item)

    return facet_of

