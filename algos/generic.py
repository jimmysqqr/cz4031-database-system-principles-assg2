"""
Generic Node Processor
"""
import annotation

def generic(plan, queue, isStart=False):
    # Dictionary to be enqueued
    q_item = {}
    q_item["Node Type"] = plan["Node Type"]
    
    try:
        q_item["Relation Name"] = plan["Relation Name"]
    except:
        plan["Relation Name"] = "I DOT HAVE A RELATION NAME"
    # SOme operators dont have relation name for some weird reason

    q_item["Total Cost"] = plan["Total Cost"]

    queue.append(q_item)

    # Process unknown node type
    output = annotation.getConnector(isStart)

    output += "perform " + plan["Node Type"] + " on relation: " + plan["Relation Name"] + ". "

    if "Plans" in plan:
        for child in plan["Plans"]:
            output += " " + annotation.processPlan(child, queue)

    return output