# Merge Join Algorithm

import annotation

def merge_join(plan, isStart):
    output = ""

    if "Plans" in plan:
        for child in plan["Plans"]:
            output = output + annotation.processPlan(child, isStart) + " "
            if isStart:
                isStart = False

    output = output + annotation.getConnector(isStart)
    output = output + "Merge Join is performed on the output"

    if "Merge Cond" in plan:
        output = output + " with condition " + plan["Merge Cond"].replace("::text", "")

    if "Join Type" == "Semi":
        output = output + " however on the left relation's row is returned."
        
    else:
        output = output + "."

    return output