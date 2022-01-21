# method to detect scenario group
#
#
#
# constellation for a reference property
#
# scenario filter:
# SELECT( COUNT ( ?var1  ) AS  ?var2  )
# WHERE {
#   ?var1  <http://www.w3.org/ns/prov#wasDerivedFrom>  ?var3 .
#  {
#    ?var3  <http://www.wikidata.org/prop/reference/P248>  <http://www.wikidata.org/entity/Q29583405> .
#  }
# }
#
#
#
# look_for e.g. "http://www.wikidata.org/prop/reference/P ... "
#
# result:   1x scenario one for 'wasDerivedFrom'
#           1x scenario group for '.../prop/reference/P....'

def scenario_group_occurrences(json_object, look_for, _):
    where = json_object["where"]

    # find scenarios 'group'

    result = 0

    # multiple bgp (basic graph patterns)
    for where_part in where:
        if where_part["type"] == "group":
            if (look_for in str(where_part["patterns"])):
                # there may be more than one
                result += str(where_part["patterns"]).count(look_for)
            else:
                if look_for in str(where_part):
                    raise Exception

    return result