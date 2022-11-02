"""
Nested Loop Node Processor
"""

import annotation

def nested_loop(plan, queue, isStart=False):
    # Dictionary to be enqueued
    q_item = {}
    q_item["Node Type"] = plan["Node Type"]
    q_item["Total Cost"] = plan["Total Cost"]

    queue.append(q_item)

    # Process Nested Loop node type
    output = ""

    tmp = annotation.processPlan(plan["Plans"][0], queue, isStart)
    output += tmp + ""
    tmp = annotation.processPlan(plan["Plans"][1], queue)
    output += tmp + ""

    output += "Next, Nested Loop join is used to join these 2 relations because... (This is where the QEP comes in). "

    return output