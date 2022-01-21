# the purpose of this module is, to create a text file, which displays the occurrences of every Wikidata property
# .. in the available data
# for this purpose the 'property_dictionary.json' is used

# mode can either ba "reference" or "qualifier" to describe the usage case as
# .. a qualifier
# ->
# .. a reference
# ->
def count_property_in(property, mode):

    if mode not in ["qualifier", "reference"]:
        error_message = "Not supported mode."
        raise Exception(error_message)

    # check, if the property dictionary already exists
    #if

    #with open("")

    return
