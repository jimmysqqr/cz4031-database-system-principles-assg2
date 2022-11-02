# Materialize Algorithm

import annotation

def materialize(plan, isStart = False):
    # Dict to add
    q_item = {}
    q_item["Mode Type"] = plan["Node Type"]
    q_item["Relation Name"] = plan["Relation Name"]
    q_item["Total Cost"] = plan["Total Cost"]

    queue.append(q_item)

    output = ""

    if "Plans" in plan:
        for child in plan["Plans"]:
            temp = annotation.processPlan(child, queue, isStart)
            output = output + temp + " "
            if isStart:
                isStart = False

    if plan["Node Type"] == "Materialize":
        output = output + annotation.getConnector(isStart)
        output = output + "Save the results in main memory to reduce latency and disk stroage overhead."

    return output