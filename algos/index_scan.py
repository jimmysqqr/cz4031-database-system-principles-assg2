"""
Index Scan Node Processor
"""


def index_scan(plan, output):
    # Process Index Scan node type:
    # output = annotation.getConnector(isStart)

    output_string = ""
    # If node type is "Index Scan"
    if plan["Node Type"] == "Index Scan" or plan["Node Type"] == "Index Only Scan":
        output_string += "Perform Index Scan on relation: " + \
            plan["Relation Name"]
        output_string += ", with index: " + plan["Index Name"]

        # Check if there is a condition in the index scan
        if "Index Cond" in plan:
            output_string += ", based on the following condition(s): " + plan["Index Cond"].replace(
                '::text', '')

        # Check if there are extra filters on the output of the index scan
        if "Filter" in plan:
            output_string += ". Index scan output is further filtered based on these condition(s): " + plan["Filter"].replace(
                '::text', '')

        output_string += ". It is faster than a Sequential Scan due to high selectivity of predicate."

    output.append(output_string)
    return
