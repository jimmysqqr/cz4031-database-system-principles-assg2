"""
Unique Node Processor
"""
import annotation

def unique(plan, output):
    # Process Unique node type
    annotation.processPlan(plan["Plans"][0], output)
    output_string = "The sorted output will be scanned with the Unique operator and adjacent duplicates will be eliminated. "
    output_string += "The Unique operator is used as it is useful for DISTINCT clauses if the input is already sorted (the query also includes ORDER BY). "
    output.append(output_string)
    return