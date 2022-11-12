"""
CTE Scan Node Processor
"""


def cte_scan(plan, output):
    # If node type is "CTE Scan"
    if plan["Node Type"] == "CTE Scan":
        output_string = "The planner performs a CTE scan on the relation: " + \
            plan["CTE Name"]

        # Check if there is a condition in the index scan
        if "Index Cond" in plan:
            output_string += ", based on the following condition(s) " + plan["Index Cond"].replace(
                '::text', '')

        # Check if there are extra filters on the output of the CTE scan
        if "Filter" in plan:
            output_string += ". The CTE scan output is further filtered based on these condition(s): " + plan["Filter"].replace(
                '::text', '')

        output_string += ". "

    output.append(output_string)
    return
