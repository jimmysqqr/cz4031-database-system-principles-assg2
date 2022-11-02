# setOp node type

import annotation

def setop(plan, isStart):
    # Dict to add
    q_item = {}
    q_item["Mode Type"] = plan["Node Type"]
    q_item["Relation Name"] = plan["Relation Name"]
    q_item["Total Cost"] = plan["Total Cost"]

    queue.append(q_item)


    output = annotation.processPlan(plan["Plans"][0], queue, isStart)
    output = output + " " + annotation.getConnector()
    output = output + "Detect "
    command_name = str(plan["Command"])
    
    if command_name == "Except" or command_name == "Except All":
        output = output + "differences "
    else:
        output = output + "similarities "
    
    output = output + "between the 2 scanned relations using the "
    output = output + plan["Node Type"] + " operation."