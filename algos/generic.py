"""
Generic Node Processor
"""
import annotation

def generic(plan, isStart=False):
    # Process unknown node type
    output = annotation.getConnector(isStart)

    output += "perform " + plan["Node Type"] + ". "

    if "Plans" in plan:
        for child in plan["Plans"]:
            output += " " + annotation.processPlan(child)

    return output