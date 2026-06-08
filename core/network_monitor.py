import psutil
import socket


def get_connections():
    connections = []

    try:
        for conn in psutil.net_connections(kind="inet"):

            if not conn.raddr:
                continue

            try:
                process = psutil.Process(conn.pid)

                process_name = process.name()

            except:
                process_name = "Unknown"

            connections.append({
                "pid": conn.pid,
                "process": process_name,
                "ip": conn.raddr.ip,
                "port": conn.raddr.port,
                "status": conn.status
            })

    except:
        pass

    return connections