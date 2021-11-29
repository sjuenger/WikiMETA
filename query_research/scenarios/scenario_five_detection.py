# find scenario 5

# multiple bgp
for where_part in where:

    if where_part["type"] == "bind":
        where_str = str(where_part)
        if "<http://www.w3.org/ns/prov#wasDerivedFrom>" in where_str:
            print(where_str)