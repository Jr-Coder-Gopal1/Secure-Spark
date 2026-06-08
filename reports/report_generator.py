from datetime import datetime


def generate_report(
    processes,
    connections,
    threats,
    risk
):

    timestamp = datetime.now().strftime(
        "%Y-%m-%d_%H-%M-%S"
    )

    filename = f"report_{timestamp}.txt"

    with open(
        filename,
        "w",
        encoding="utf-8"
    ) as report:

        report.write(
            "SECURE SPARK SECURITY REPORT\n"
        )

        report.write(
            "=" * 50 + "\n\n"
        )

        report.write(
            f"Processes: {len(processes)}\n"
        )

        report.write(
            f"Connections: {len(connections)}\n"
        )

        report.write(
            f"Threats: {len(threats)}\n"
        )

        report.write(
            f"Risk Score: {risk['score']}\n"
        )

        report.write(
            f"Status: {risk['status']}\n\n"
        )

        report.write(
            "Threat Details\n"
        )

        report.write(
            "-" * 30 + "\n"
        )

        if len(threats) == 0:

            report.write(
                "No threats detected\n"
            )

        else:

            for threat in threats:

                report.write(
                    f"{threat['process']} | "
                    f"{threat['level']} | "
                    f"{threat['reason']}\n"
                )

    return filename