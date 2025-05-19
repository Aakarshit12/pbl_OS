import json
from typing import Dict, List, Union, Any
from datetime import datetime

def format_data(
    cpu_data: Dict[str, Any],
    memory_data: Dict[str, float],
    disk_data: List[Dict[str, float]],
    top_mem: List[Dict[str, Any]]
) -> Dict[str, Union[float, str, List, Dict]]:
    """
    Format system metrics data for logging and display.
    
    Args:
        cpu_data: Dictionary containing detailed CPU metrics
        memory_data: Dictionary containing memory metrics
        disk_data: List of dictionaries containing disk metrics for each drive
        top_mem: List of top memory-consuming processes
        
    Returns:
        Dictionary containing formatted metrics with timestamp
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    formatted_data = {
        "Timestamp": timestamp,
        
        # CPU Metrics
        "Overall CPU Usage (%)": cpu_data["Overall CPU Usage (%)"],
        "CPU Frequency (MHz)": json.dumps(cpu_data["CPU Frequency (MHz)"]),
        "CPU Times": json.dumps(cpu_data["CPU Times"]),
        "CPU Stats": json.dumps(cpu_data["CPU Stats"]),
        "Process Count": cpu_data["Process Count"],
        
        # Memory Metrics
        "Memory Usage (%)": memory_data["Memory Usage (%)"],
        "Total Memory (MB)": memory_data["Total Memory (MB)"],
        "Available Memory (MB)": memory_data["Available Memory (MB)"],
        
        # Top Memory Processes
        "Top Memory Processes": json.dumps(top_mem)
    }
    
    # Add per-core CPU usage
    for i, usage in enumerate(cpu_data["Per Core Usage (%)"]):
        formatted_data[f"CPU Core {i} Usage (%)"] = usage
    
    # Add top CPU processes
    for i, proc in enumerate(cpu_data["Top Processes"]):
        formatted_data[f"Top CPU Process {i+1}"] = json.dumps(proc)
    
    # Add disk information for each drive
    for disk in disk_data:
        drive = disk["Drive"].rstrip(":")
        formatted_data.update({
            f"Drive {drive} Total Space (MB)": disk["Total Disk Space (MB)"],
            f"Drive {drive} Free Space (MB)": disk["Free Disk Space (MB)"],
            f"Drive {drive} Usage (%)": disk["Disk Usage (%)"]
        })
    
    return formatted_data
