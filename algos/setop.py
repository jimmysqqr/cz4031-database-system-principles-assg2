"""
SetOp Node Processor
"""

import annotation

def set_op(plan, output):
    annotation.processPlan(plan["Plans"][0], output)
    # Command name is usually UNION, INTERSECT, or EXCEPT
    command_name = str(plan["Command"])
    output_string = "Combine the 2 scanned relations using the "
    output_string += command_name + " operation."

    output.append(output_string)

    return