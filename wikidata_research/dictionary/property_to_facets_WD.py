# get the abstract items on Wikidata, of which the property is a facet (if of any)
import SPARQLWrapper
import wikidata_research.dictionary.utilities as utilities

def getFacet(property_PID):

    sparql = SPARQLWrapper.SPARQLWrapper("https://query.wikidata.org/sparql")

    # can be a facet of a item on different hierarchy levels -> here all items are counted
    # ?o2 can not be "entity" Q35120 (-> to prevent a chain of "subclass of" above
    # .. "wikidata property"

    sparql.setQuery("""
    SELECT ?facetOFLabel
    WHERE
    {
        wd:"""+ property_PID + """ wdt:P31 ?o .
        ?o wdt:P279* ?o2 .
        FILTER (!regex(STR(?o2), "Q35120"))
        ?o2 wdt:P1269 ?facetOF .
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

