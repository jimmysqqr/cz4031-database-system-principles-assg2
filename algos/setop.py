# setOp node type

import annotation

def setop(plan, isStart):
    output = annotation.processPlan(plan["Plans"][0], isStart)
    output = output + " " + annotation.getConnector()
    output = output + "Detect "
    command_name = str(plan["Command"])
    
    if command_name == "Except" or command_name == "Except All":
        output = output + "differences "
    else:
        output = output + "similarities "
    
    output = output + "between the 2 scanned relations using the "
    output = output + plan["Node Type"] + " operation."