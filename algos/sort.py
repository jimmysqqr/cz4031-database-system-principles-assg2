# sort algorithm

import annotation

def sort(plan, isStart):
    output = annotation.getConnector(isStart)

    if "Plans" in plan:
        for child in plan["Plans"]:
            temp = annotation.processPlan(child, isStart)
            output = output + temp + " "

            if isStart:
                isaStart = False

    if plan["Node Type"] == "Sort":
        output = output + annotation.getConnector(isStart)
        output = output + "Output results is sorted based on attribute "

        if "DESC" in str(plan["Sort Key"]):
            output = output + str(plan["Sort Key"]).replace("DESC", "") + " in descending order."
        else:
            output = output + str(plan["Sort Key"]) + "."

    return output