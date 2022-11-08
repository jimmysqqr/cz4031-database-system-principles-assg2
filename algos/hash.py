"""
Hash Node Processor
"""

import annotation


def hash(plan, output):
    # Recursive step
    if "Plans" in plan:
        annotation.processPlan(plan['Plans'][0], output)

    output_string = "A Hash index is created on the previous relation."

    output.append(output_string)

    return
