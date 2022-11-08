"""
Subquery Scan Node Processor
"""
import annotation

def subquery_scan(plan, output):
    # Process Subquery Scan node type
    output_string = ""

    if "Plans" in plan:
        for child in plan["Plans"]:
            annotation.processPlan(child, output)

    output_string += "Do a subquery scan on the output of the sub-query in earlier operations"

    # Check if the sequential scan was done with a filter
    if "Filter" in plan:
        output_string += ", with condition: "
        output_string += plan['Filter'].replace('::text', '')

    output_string += ". "
    output.append(output_string)

    return