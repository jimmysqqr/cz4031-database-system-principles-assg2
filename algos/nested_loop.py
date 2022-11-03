"""
Nested Loop Node Processor
"""

import annotation

def nested_loop(plan, isStart=False):
    # Process Nested Loop node type
    output = ""

    tmp = annotation.processPlan(plan["Plans"][0], isStart)
    output += tmp + ""
    tmp = annotation.processPlan(plan["Plans"][1])
    output += tmp + ""

    output += "Next, Nested Loop join is used to join these 2 relations because... (This is where the QEP comes in). "

    return output