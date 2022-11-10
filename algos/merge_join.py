"""
Merge Join Node Processor
"""

import annotation

def merge_join(plan, output):
    # Process the child nodes first
    if "Plans" in plan:
        for child in plan["Plans"]:
            annotation.processPlan(child, output)

    output_string = "Merge Join is performed on the output"

    if "Merge Cond" in plan:
        output_string += " with condition " + plan["Merge Cond"].replace("::text", "") + ". "
    else:
        output = output + ". "
        
    output_string += "Merge Join is used for the join because PLACEHOLDER"
    output.append(output_string)
    return