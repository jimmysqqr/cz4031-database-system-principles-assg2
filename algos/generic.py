"""
Generic Node Processor
"""

import json
import annotation

def generic(plan, isStart=False):
    # Process unknown node type
    processedPlan = annotation.getConnector(isStart)

    processedPlan += "perform " + plan["Node Type"] + " on relation: " + plan["Relation Name"] + ". "

    if "Plans" in plan:
        for child in plan["Plans"]:
            processedPlan += " " + annotation.processPlan(child)

    return processedPlan