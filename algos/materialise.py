# Materialise Algorithm

import annotation

def materialise(plan, isStart = False):
    output = ""

    if "Plans" in plan:
        for child in plan["Plans"]:
            temp = annotation.processPlan(child, isStart)
            output = output + temp + " "
            if isStart:
                isStart = False

    if plan["Node Type"] == "Materialise":
        output = output + annotation.getConnector(isStart)
        output = output + "Save the results in main memory to reduce latency and disk stroage overhead"

    return output