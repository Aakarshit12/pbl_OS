import matplotlib.pyplot as plt

def plot_data(data_log):
    timestamps = [entry["Timestamp"] for entry in data_log]
    cpu_usage = [entry["CPU Usage (%)"] for entry in data_log]
    memory_usage = [entry["Memory Usage (%)"] for entry in data_log]
    disk_usage = [entry["Disk Usage (%)"] for entry in data_log]

    plt.figure(figsize=(10, 6))
    
    plt.plot(timestamps, cpu_usage, label="CPU Usage (%)", color='red')
    plt.plot(timestamps, memory_usage, label="Memory Usage (%)", color='blue')
    plt.plot(timestamps, disk_usage, label="Disk Usage (%)", color='green')

    plt.xlabel("Time")
    plt.ylabel("Usage (%)")
    plt.title("System Performance Data")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
