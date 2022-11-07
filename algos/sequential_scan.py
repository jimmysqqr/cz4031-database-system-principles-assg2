"""
Sequential Scan Node Processor
"""

import annotation

def sequential_scan(plan, output):
    # Process Sequential Scan node type
    # output = annotation.getConnector(isStart)

    output_string = "Perform Sequential Scan on relation: "

    # State the relation name
    if "Relation Name" in plan:
        output_string += plan["Relation Name"]
    
    # State the alias if it's different from the relation name
    if "Alias" in plan and plan["Relation Name"]!=plan["Alias"]:
        output_string += " as " + plan["Alias"]

    # Check if the sequential scan was done with a filter
    if "Filter" in plan:
        output_string += ", with condition: "
        output_string += plan['Filter'].replace('::text', '')

    output_string += ", as there is no index built on the desired attribute. Also a majority of rows are getting fetched due to low selectivity of the predicate. "
    output.append(output_string)
    return 
    
