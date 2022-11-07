"""
Nested Loop Node Processor
"""

import annotation

def nested_loop(plan, output):
    # Process Nested Loop node type
    output_string = ""

    annotation.processPlan(plan["Plans"][0], output)
    annotation.processPlan(plan["Plans"][1], output)

    output_string += "Next, Nested Loop Join is used to join these 2 relations because PLACEHOLDER"

    output.append(output_string)
    return