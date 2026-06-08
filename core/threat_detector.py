def detect_threats(processes):

    threats = []

    suspicious_keywords = [
        "miner",
        "crypto",
        "stealer",
        "keylogger",
        "inject",
        "rat",
        "trojan",
        "hack",
        "malware",
        "backdoor"
    ]

    for process in processes:

        name = str(process["name"]).lower()

        for keyword in suspicious_keywords:

            if keyword in name:

                threats.append({
                    "process": process["name"],
                    "pid": process["pid"],
                    "level": "HIGH",
                    "reason": f"Contains keyword '{keyword}'"
                })

                break

    return threats