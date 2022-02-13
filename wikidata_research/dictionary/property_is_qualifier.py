# get, if a property on wikidata is a qualifier
# .. according to the recommended properties of wikidata
import SPARQLWrapper
import wikidata_research.dictionary.utilities as utilities


def is_qualifier(property_PID):

    sparql = SPARQLWrapper.SPARQLWrapper("https://query.wikidata.org/sparql")

    # is a property a subclass of (in a "subclass chain"):
    #   restrictive qualifier (Q61719275)   --> qualifier
    #   non-restrictive qualifier (Q61719274) --> qualifer
    #   Wikidata property used as "depicts" (P180) qualifier on Commons (Q70564278) --> qualifier
    #   Wikidata qualifier (Q15720608)  --> qualifier (most common one)
    #   --> superclass of all the other classes

    sparql.setQuery("""
    SELECT ?classLabel
    WHERE
    {
        wd:"""+ property_PID + """ wdt:P31 ?class .
        SERVICE wikibase:label { bd:serviceParam wikibase:language "en" }
    }
    """)
    sparql.setReturnFormat(SPARQLWrapper.JSON)
    results = sparql.query().convert()

    prop_classes = []

    for var in results['results']['bindings']:

        prop_class = var['classLabel']['value']
        prop_classes.append(prop_class)

    result = []

    # save all the queried qualifiers to a list.
    # NOTE: in principal, every wikidata qualifier property is an instance of "Wikidata qualifier"
    #
    # But, to not create to much redundancy in the data, the "Wikidata qualifier" tag will only
    # ..  be applied to a property, if it wasn't tagged with any of the other 4 qualifier options
    # .. i.e. "restrictive-qualifier", "non-restrictive-qualifier", or "Wikidata property used as depicts...."

    if "restrictive qualifier" in prop_classes:
        result.append("restrictive qualifier")
    if "non-restrictive qualifier" in prop_classes:
        result.append("non-restrictive qualifier")
    if "Wikidata property used as \"depicts\" (P180) qualifier on Commons" in prop_classes:
        result.append("Wikidata property used as \"depicts\" (P180) qualifier on Commons")

    if len(result) == 0:
        if "Wikidata qualifier" in prop_classes:
            result.append("Wikidata qualifier")

    return result