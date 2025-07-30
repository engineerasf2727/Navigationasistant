import psutil
import time
import matplotlib.pyplot as plt

# target process name (örneğin 'python' veya 'main.py' çalıştıran PID)
TARGET_NAME = "main.py"

def find_main_process():
    for proc in psutil.process_iter(['name', 'cmdline']):
        if TARGET_NAME in proc.info['name'] or 'main.py' in str(proc.info['cmdline']):
            return proc
    return None

cpu_usage = []
timestamps = []
start_time = time.time()

proc = find_main_process()
if not proc:
    print("Process not found.")
    exit()

for _ in range(60):  # 60 ölçüm (yaklaşık 30 saniye, 0.5s interval)
    cpu = proc.cpu_percent(interval=0.5)
    t = time.time() - start_time
    cpu_usage.append(cpu)
    timestamps.append(t)

plt.plot(timestamps, cpu_usage, marker='o')
plt.xlabel("Time (s)")
plt.ylabel("CPU Usage (%)")
plt.title("CPU Usage of main.py")
plt.grid(True)
plt.tight_layout()
plt.show()
