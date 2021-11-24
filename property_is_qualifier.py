# get, if a property on wikidata is a qualifier
# .. according to the recommended properties of wikidata
import SPARQLWrapper
import utilities

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

        print(prop_classes)

    result = ""

    if "restrictive qualifier" in prop_classes:
        result += "restrictive qualifier"
    elif "non-restrictive qualifier" in prop_classes:
        result += "non-restrictive qualifier"
    elif "Wikidata property used as \"depicts\" (P180) qualifier on Commons" in prop_classes:
        result += "Wikidata property used as \"depicts\" (P180) qualifier on Commons"
    elif "Wikidata qualifier" in prop_classes:
        result += "Wikidata qualifier"

    return prop_classes