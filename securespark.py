from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from rich.text import Text
from core.threat_detector import detect_threats
import time
from core.risk_engine import calculate_risk
from core.network_monitor import get_connections
from core.process_monitor import get_processes
from reports.report_generator import generate_report

console = Console()

# ==========================
# LOGO
# ==========================

logo = """
 ███████╗███████╗ ██████╗██╗   ██╗██████╗ ███████╗
 ██╔════╝██╔════╝██╔════╝██║   ██║██╔══██╗██╔════╝
 ███████╗█████╗  ██║     ██║   ██║██████╔╝█████╗
 ╚════██║██╔══╝  ██║     ██║   ██║██╔══██╗██╔══╝
 ███████║███████╗╚██████╗╚██████╔╝██║  ██║███████╗
 ╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝

  ███████╗██████╗  █████╗ ██████╗ ██╗  ██╗
  ██╔════╝██╔══██╗██╔══██╗██╔══██╗██║ ██╔╝
  ███████╗██████╔╝███████║██████╔╝█████╔╝
  ╚════██║██╔═══╝ ██╔══██║██╔══██╗██╔═██╗
  ███████║██║     ██║  ██║██║  ██║██║  ██╗
  ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝
"""

console.print(
    Panel.fit(
        Text(logo, style="bold bright_cyan"),
        title="[bold bright_blue]SECURE SPARK[/bold bright_blue]",
        subtitle="[green]Privacy • Security • Monitoring[/green]",
        border_style="bright_blue",
        box=box.DOUBLE
    )
)

# ==========================
# BOOT SEQUENCE
# ==========================

console.print("[bright_green][+][/bright_green] Initializing Security Core...")
time.sleep(0.3)

console.print("[bright_yellow][*][/bright_yellow] Loading Process Monitor...")
time.sleep(0.3)

console.print("[bright_yellow][*][/bright_yellow] Loading Network Engine...")
time.sleep(0.3)

console.print("[bright_yellow][*][/bright_yellow] Loading Risk Analyzer...")
time.sleep(0.3)

console.print("[bright_green][✓][/bright_green] Secure Spark Ready!\n")

# ==========================
# STATUS PANEL
# ==========================

console.print(
    Panel.fit(
"""
[green]STATUS      : ONLINE[/green]
[cyan]ENGINE      : ACTIVE[/cyan]
[yellow]RISK CORE   : LOADED[/yellow]
[blue]NETWORK     : STANDBY[/blue]
[magenta]VERSION     : 0.1 ALPHA[/magenta]
""",
        title="[bold cyan]SYSTEM STATUS[/bold cyan]",
        border_style="green"
    )
)

# ==========================
# PROCESS SCAN
# ==========================

processes = get_processes()

table = Table(
    title="[bold cyan]Running Processes[/bold cyan]",
    border_style="bright_blue",
    box=box.ROUNDED
)

table.add_column("PID", style="green")
table.add_column("PROCESS", style="cyan")
table.add_column("CPU %", style="yellow")
table.add_column("STATUS", style="green")

for process in processes[:25]:
    table.add_row(
        str(process["pid"]),
        str(process["name"]),
        str(process["cpu"]),
        "SAFE"
    )

console.print(table)

# ==========================
# NETWORK CONNECTIONS
# ==========================

connections = get_connections()

network_table = Table(
    title="[bold red]Network Connections[/bold red]",
    border_style="red",
    box=box.ROUNDED
)

network_table.add_column(
    "PROCESS",
    style="cyan"
)

network_table.add_column(
    "REMOTE IP",
    style="yellow"
)

network_table.add_column(
    "PORT",
    style="green"
)

network_table.add_column(
    "STATUS",
    style="magenta"
)

for conn in connections[:20]:

    network_table.add_row(
        str(conn["process"]),
        str(conn["ip"]),
        str(conn["port"]),
        str(conn["status"])
    )

console.print(network_table)

risk = calculate_risk(
    processes,
    connections
)

threats = detect_threats(processes)
#threat tabe================
from rich.table import Table

threat_table = Table(
    title="[bold red]Threat Detection[/bold red]",
    border_style="red",
    box=box.ROUNDED
)

threat_table.add_column(
    "PROCESS",
    style="yellow"
)

threat_table.add_column(
    "PID",
    style="cyan"
)

threat_table.add_column(
    "LEVEL",
    style="red"
)

threat_table.add_column(
    "REASON",
    style="magenta"
)

if len(threats) == 0:

    threat_table.add_row(
        "None",
        "-",
        "SAFE",
        "No threats detected"
    )

else:

    for threat in threats:

        threat_table.add_row(
            str(threat["process"]),
            str(threat["pid"]),
            str(threat["level"]),
            str(threat["reason"])
        )

console.print(threat_table)

report_file = generate_report(
    processes,
    connections,
    threats,
    risk
)

console.print(
    f"\n[green]Report Saved:[/green] {report_file}"
)
# ==========================
# SECURITY SUMMARY
# ==========================

console.print("\n")
console.print("═" * 55, style="bright_blue")

if risk["status"] == "SYS_SAFE":
    color = "green"

elif risk["status"] == "SYS_LOW":
    color = "cyan"

elif risk["status"] == "SYS_WARN":
    color = "yellow"

elif risk["status"] == "SYS_SUSP":
    color = "bright_red"

else:
    color = "red"

console.print(
    f"[green]HOST STATUS : SECURE[/green]"
)

console.print(
    f"[yellow]RISK SCORE : {risk['score']}[/yellow]"
)

console.print(
    f"[{color}]STATE : {risk['status']}[/{color}]"
)

console.print(
    f"[cyan]PROCESSES : {len(processes)}[/cyan]"
)

console.print(
    f"[magenta]CONNECTIONS : {len(connections)}[/magenta]"
)

console.print("\n[bold]Risk Reasons:[/bold]")
console.print(
    f"[red]THREATS FOUND : {len(threats)}[/red]"
)

for reason in risk["reasons"]:
    console.print(f" • {reason}")

console.print("═" * 55, style="bright_blue")

from core.live_monitor import start_monitoring
from core.privacy_audit import run_privacy_audit
from rich.table import Table
from rich.progress import Progress
import time

while True:

    console.print("\n")
    console.print(
        "[bold cyan]══════════════ COMMAND CENTER ══════════════[/bold cyan]"
    )

    console.print("[green][1][/green] Live Device Monitoring")
    console.print("[cyan][2][/cyan] Re-Run Full Security Scan")
    console.print("[yellow][3][/yellow] Generate Security Report")
    console.print("[magenta][4][/magenta] Help")
    console.print("[bright_blue][5][/bright_blue] Privacy Audit")
    console.print("[bright_blue][6][/bright_blue] Permission Audit")
    console.print("[red][7][/red] Exit")

    choice = input(
        "\nSecureSpark> "
    ).strip()

    # ==================================
    # LIVE MONITOR
    # ==================================

    if choice == "1":

        start_monitoring()

    # ==================================
    # FULL SCAN
    # ==================================

    elif choice == "2":

        console.print(
            "\n[green]Security Scan Already Completed.[/green]"
        )

        console.print(
            "[cyan]Restart Secure Spark for a fresh scan.[/cyan]"
        )

    # ==================================
    # REPORT
    # ==================================

    elif choice == "3":

        report_file = generate_report(
            processes,
            connections,
            threats,
            risk
        )

        console.print(
            f"\n[green]Report Saved:[/green] {report_file}"
        )

    # ==================================
    # HELP
    # ==================================

    elif choice == "4":

        console.print(
"""
[bold cyan]SECURE SPARK HELP[/bold cyan]

[green]1[/green] Live Device Monitoring
 • Process Tracking
 • Network Tracking
 • Threat Detection
 • CPU Monitoring
 • RAM Monitoring

[cyan]2[/cyan] Full Security Scan

[yellow]3[/yellow] Generate Report

[blue]5[/blue] Privacy Audit

[red]7[/red] Exit
"""
        )

    # ==================================
    # PRIVACY AUDIT
    # ==================================

    elif choice == "5":

        console.print()

        with Progress() as progress:

            task = progress.add_task(
                "[cyan]Running Privacy Audit...",
                total=100
            )

            while not progress.finished:

                progress.update(
                    task,
                    advance=5
                )

                time.sleep(0.05)

        result = run_privacy_audit()

        privacy_table = Table(
            title="[bold blue]Privacy Audit[/bold blue]",
            border_style="blue"
        )

        privacy_table.add_column(
            "LEVEL",
            style="yellow"
        )

        privacy_table.add_column(
            "MESSAGE",
            style="cyan"
        )

        if len(result["findings"]) == 0:

            privacy_table.add_row(
                "SAFE",
                "No privacy issues found"
            )

        else:

            for item in result["findings"]:

                privacy_table.add_row(
                    item["level"],
                    item["message"]
                )

        console.print(
            privacy_table
        )

        console.print()

        console.print(
            "[bold blue]Approximate Location[/bold blue]"
        )

        console.print(
            f"[cyan]City:[/cyan] {result['city']}"
        )

        console.print(
            f"[cyan]Region:[/cyan] {result['region']}"
        )

        console.print(
            f"[cyan]Country:[/cyan] {result['country']}"
        )

        console.print(
            f"[cyan]ISP:[/cyan] {result['isp']}"
        )

        console.print()

        console.print(
            f"[green]Privacy Score:[/green] "
            f"{result['score']}/100"
        )

        console.print(
            f"[yellow]Open Ports:[/yellow] "
            f"{len(result['ports'])}"
        )

        console.print(
            f"[magenta]Connections:[/magenta] "
            f"{result['active_connections']}"
        )

        console.print(
            f"[bold green]Status:[/bold green] "
            f"{result['status']}"
        )

        console.print(
"""
[bold green]Protection Recommendations[/bold green]

✓ Enable Firewall

✓ Close Unused Services

✓ Remove Unknown Software

✓ Keep Windows Updated

✓ Avoid Public Wi-Fi

✓ Use Strong Passwords
"""
        )

    # ==================================
    # PERMISSION AUDIT
    # ==================================

    elif choice == "6":

        console.print(
            "\n[yellow]Permission Audit Coming Soon[/yellow]"
        )

    # ==================================
    # EXIT
    # ==================================

    elif choice == "7":

        console.print(
            "\n[bold red]Thank you for using Secure Spark.[/bold red]"
        )

        break

    else:

        console.print(
            "\n[bold red]Invalid Option[/bold red]"
        )