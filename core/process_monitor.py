import psutil
import time


def get_processes():

    processes = []

    # CPU readings initialize
    for proc in psutil.process_iter():
        try:
            proc.cpu_percent()
        except:
            pass

    time.sleep(1)

    for proc in psutil.process_iter():

        try:

            process_info = {
                "pid": proc.pid,
                "name": proc.name(),
                "cpu": proc.cpu_percent(),
                "ram": round(
                    proc.memory_info().rss /
                    1024 /
                    1024,
                    2
                )
            }

            processes.append(
                process_info
            )

        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            psutil.ZombieProcess
        ):
            pass

    return processes