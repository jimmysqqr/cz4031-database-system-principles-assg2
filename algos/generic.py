"""
Generic Node Processor
"""

import json
import annotation

def generic(plan, isStart=False):
    # Process unknown node type
    output = annotation.getConnector(isStart)

    output += "perform " + plan["Node Type"] + " on relation: " + plan["Relation Name"] + ". "

    if "Plans" in plan:
        for child in plan["Plans"]:
            output += " " + annotation.processPlan(child)

    return output