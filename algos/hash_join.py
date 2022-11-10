"""
Hash Join Node Processor
"""

import annotation

def hash_join(plan, output):
    # Process Hash Join
    # Process child nodes first
    annotation.processPlan(plan["Plans"][1], output)
    annotation.processPlan(plan["Plans"][0], output)

    output_string = "Next, Hash Join the 2 results from previous operations. "
    output_string += plan["Join Type"] + "Join is used"

    if "Hash Cond" in plan:
        output_string += " with the condition " + plan["Hash Cond"].replace("::text", "") + ". "
    else:
        output_string += ". "

    output_string += "Hash Join is used for the join because PLACEHOLDER"
    output.append(output_string)
    return