"""
Group Node Processor
"""

import annotation

def group(plan, isStart=False):
    """Parser function for node type limit"""
    output = annotation.processPlan(plan["Plans"][0], isStart)
    if isStart:
        isStart = False
    output += " " + annotation.getConnector(isStart)
    if len(plan["Group Key"]) == 1:
        output += "the output from the previous operation is grouped based on the key: "
        output += plan["Group Key"][0].replace("::text", "")
    else:
        output += "the output from the previous operation is grouped based on the keys: ("
        for key in plan["Group Key"]:
            output += key.replace("::text", "") + ", "
        output = output[:-2] + ")"
    output += "."

    return output