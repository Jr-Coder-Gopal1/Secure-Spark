import psutil
import requests
import time


def run_privacy_audit():

    findings = []
    score = 100

    # ==========================
    # ANIMATION
    # ==========================

    print("\n")
    print("[*] Checking Open Ports...")
    time.sleep(0.5)

    print("[*] Analyzing Network Exposure...")
    time.sleep(0.5)

    print("[*] Scanning Active Connections...")
    time.sleep(0.5)

    print("[*] Calculating Privacy Score...")
    time.sleep(0.5)

    # ==========================
    # OPEN PORTS
    # ==========================

    listening_ports = []

    try:

        for conn in psutil.net_connections():

            if conn.status == "LISTEN":

                if conn.laddr:

                    listening_ports.append(
                        conn.laddr.port
                    )

    except:
        pass

    dangerous_ports = [
        21,
        23,
        135,
        139,
        445,
        3389
    ]

    for port in listening_ports:

        if port in dangerous_ports:

            score -= 15

            findings.append({
                "level": "HIGH",
                "message":
                f"Sensitive port open: {port}"
            })

    if len(listening_ports) > 10:

        score -= 10

        findings.append({
            "level": "WARNING",
            "message":
            "Large number of open ports"
        })

    # ==========================
    # ACTIVE CONNECTIONS
    # ==========================

    active_connections = len(
        psutil.net_connections()
    )

    if active_connections > 50:

        score -= 10

        findings.append({
            "level": "WARNING",
            "message":
            "High number of active connections"
        })

    # ==========================
    # LOCATION LOOKUP
    # ==========================

    city = "Unknown"
    region = "Unknown"
    country = "Unknown"
    isp = "Unknown"

    try:

        data = requests.get(
            "https://ipinfo.io/json",
            timeout=5
        ).json()

        city = data.get(
            "city",
            "Unknown"
        )

        region = data.get(
            "region",
            "Unknown"
        )

        country = data.get(
            "country",
            "Unknown"
        )

        isp = data.get(
            "org",
            "Unknown"
        )

    except:
        pass

    # ==========================
    # SCORE
    # ==========================

    if score >= 90:

        status = "EXCELLENT"

    elif score >= 75:

        status = "GOOD"

    elif score >= 50:

        status = "MEDIUM"

    else:

        status = "HIGH RISK"

    return {

        "score": score,

        "status": status,

        "ports": listening_ports,

        "findings": findings,

        "active_connections":
        active_connections,

        "city": city,

        "region": region,

        "country": country,

        "isp": isp
    }