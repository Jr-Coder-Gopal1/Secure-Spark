from rich.console import Console
import time
from datetime import datetime

from core.process_monitor import get_processes
from core.network_monitor import get_connections
from core.threat_detector import detect_threats

console = Console()


def log_info(message):

    timestamp = datetime.now().strftime(
        "%H:%M:%S"
    )

    console.print(
        f"[bold green][{timestamp}][/bold green] "
        f"{message}"
    )


def log_network(message):

    timestamp = datetime.now().strftime(
        "%H:%M:%S"
    )

    console.print(
        f"[bold cyan][{timestamp}][/bold cyan] "
        f"{message}"
    )


def log_warning(message):

    timestamp = datetime.now().strftime(
        "%H:%M:%S"
    )

    console.print(
        f"[bold yellow][{timestamp}][/bold yellow] "
        f"{message}"
    )


def log_threat(message):

    timestamp = datetime.now().strftime(
        "%H:%M:%S"
    )

    console.print(
        f"[bold red][{timestamp}][/bold red] "
        f"{message}"
    )


def start_monitoring():

    console.print(
        "\n[bold cyan]══════════════════════════════════════════════[/bold cyan]"
    )

    console.print(
        "[bold green]SECURE SPARK LIVE MONITOR[/bold green]"
    )

    console.print(
        "[yellow]Press CTRL + C to stop[/yellow]"
    )

    console.print(
        "[bold cyan]══════════════════════════════════════════════[/bold cyan]\n"
    )

    previous_processes = set()
    previous_connections = set()

    try:

        while True:

            # ==================================
            # PROCESS MONITORING
            # ==================================

            current_processes = get_processes()

            current_process_set = set()

            for process in current_processes:

                current_process_set.add(
                    (
                        process["pid"],
                        process["name"]
                    )
                )

            new_processes = (
                current_process_set -
                previous_processes
            )

            for pid, name in new_processes:

                log_info(
                    f"[PROCESS] NEW -> "
                    f"{name} "
                    f"(PID {pid})"
                )

            closed_processes = (
                previous_processes -
                current_process_set
            )

            for pid, name in closed_processes:

                log_warning(
                    f"[PROCESS] CLOSED -> "
                    f"{name} "
                    f"(PID {pid})"
                )

            previous_processes = (
                current_process_set
            )

            # ==================================
            # CPU / RAM MONITORING
            # ==================================

            for process in current_processes:

                try:

                    cpu = float(
                        process.get(
                            "cpu",
                            0
                        )
                    )

                    ram = float(
                        process.get(
                            "ram",
                            0
                        )
                    )

                    if cpu > 50:

                        log_warning(
                            f"[CPU] "
                            f"{process['name']} "
                            f"using {cpu}% CPU"
                        )

                    if ram > 500:

                        log_warning(
                            f"[RAM] "
                            f"{process['name']} "
                            f"using {ram} MB RAM"
                        )

                except:
                    pass

            # ==================================
            # THREAT DETECTION
            # ==================================

            threats = detect_threats(
                current_processes
            )

            for threat in threats:

                log_threat(
                    f"[THREAT] "
                    f"{threat['process']} | "
                    f"{threat['reason']}"
                )

            # ==================================
            # NETWORK MONITORING
            # ==================================

            connections = get_connections()

            current_connection_set = set()

            for conn in connections:

                current_connection_set.add(
                    (
                        conn["process"],
                        conn["ip"],
                        conn["port"]
                    )
                )

            new_connections = (
                current_connection_set -
                previous_connections
            )

            for process, ip, port in new_connections:

                log_network(
                    f"[NETWORK] "
                    f"{process} -> "
                    f"{ip}:{port}"
                )

            previous_connections = (
                current_connection_set
            )

            # ==================================
            # WAIT
            # ==================================

            time.sleep(5)

    except KeyboardInterrupt:

        console.print(
            "\n[bold red]Monitoring Stopped[/bold red]"
        )