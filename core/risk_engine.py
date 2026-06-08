def calculate_risk(processes, connections):

    score = 0
    reasons = []

    process_count = len(processes)
    connection_count = len(connections)

    # Process Count Check
    if process_count > 250:
        score += 20
        reasons.append("High process count")

    elif process_count > 180:
        score += 10
        reasons.append("Moderately high process count")

    # Connection Count Check
    if connection_count > 100:
        score += 30
        reasons.append("Very high network activity")

    elif connection_count > 50:
        score += 15
        reasons.append("High network activity")

    # Unknown Processes
    unknown_count = 0

    for process in processes:

        name = str(process["name"]).lower()

        if (
            "unknown" in name
            or name == "none"
            or name == ""
        ):
            unknown_count += 1

    if unknown_count > 0:
        score += min(unknown_count * 5, 25)

        reasons.append(
            f"{unknown_count} unknown processes detected"
        )

    # Status

    if score <= 20:
        status = "SYS_SAFE"

    elif score <= 40:
        status = "SYS_LOW"

    elif score <= 60:
        status = "SYS_WARN"

    elif score <= 80:
        status = "SYS_SUSP"

    else:
        status = "SYS_CRIT"

    return {
        "score": score,
        "status": status,
        "reasons": reasons
    }