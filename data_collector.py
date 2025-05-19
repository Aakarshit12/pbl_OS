import ctypes
import time
import os
import psutil
from typing import Dict, List, Optional, Tuple

MB_CONVERSION = 1024 * 1024

class MEMORYSTATUSEX(ctypes.Structure):
    _fields_ = [
        ("dwLength", ctypes.c_uint32),
        ("dwMemoryLoad", ctypes.c_uint32),
        ("ullTotalPhys", ctypes.c_uint64),
        ("ullAvailPhys", ctypes.c_uint64),
        ("ullTotalPageFile", ctypes.c_uint64),
        ("ullAvailPageFile", ctypes.c_uint64),
        ("ullTotalVirtual", ctypes.c_uint64),
        ("ullAvailVirtual", ctypes.c_uint64),
        ("ullAvailExtendedVirtual", ctypes.c_uint64)
    ]

def get_cpu_usage() -> Dict[str, float]:
    """
    Get detailed CPU usage information including per-core usage and process statistics.
    Returns a dictionary containing various CPU metrics.
    """
    try:
        # Get overall CPU usage
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        # Get per-core usage
        per_cpu = psutil.cpu_percent(interval=0.1, percpu=True)
        
        # Get CPU frequency
        freq = psutil.cpu_freq()
        current_freq = freq.current if freq else 0
        max_freq = freq.max if freq else 0
        
        # Get CPU times
        cpu_times = psutil.cpu_times()
        
        # Get CPU stats
        cpu_stats = psutil.cpu_stats()
        
        # Get process count
        process_count = len(psutil.pids())
        
        # Get top 5 CPU-consuming processes
        top_processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
            try:
                pinfo = proc.info
                if pinfo['cpu_percent'] > 0:
                    top_processes.append({
                        'pid': pinfo['pid'],
                        'name': pinfo['name'],
                        'cpu_percent': pinfo['cpu_percent']
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        # Sort and get top 5
        top_processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        top_processes = top_processes[:5]
        
        return {
            "Overall CPU Usage (%)": round(cpu_percent, 2),
            "Per Core Usage (%)": [round(usage, 2) for usage in per_cpu],
            "CPU Frequency (MHz)": {
                "Current": round(current_freq, 2),
                "Max": round(max_freq, 2)
            },
            "CPU Times": {
                "User": round(cpu_times.user, 2),
                "System": round(cpu_times.system, 2),
                "Idle": round(cpu_times.idle, 2)
            },
            "CPU Stats": {
                "Context Switches": cpu_stats.ctx_switches,
                "Interrupts": cpu_stats.interrupts,
                "Soft Interrupts": cpu_stats.soft_interrupts,
                "System Calls": cpu_stats.syscalls
            },
            "Process Count": process_count,
            "Top Processes": top_processes
        }
    except Exception as e:
        print(f"Error getting CPU usage: {str(e)}")
        return {
            "Overall CPU Usage (%)": 0.0,
            "Per Core Usage (%)": [],
            "CPU Frequency (MHz)": {"Current": 0.0, "Max": 0.0},
            "CPU Times": {"User": 0.0, "System": 0.0, "Idle": 0.0},
            "CPU Stats": {"Context Switches": 0, "Interrupts": 0, "Soft Interrupts": 0, "System Calls": 0},
            "Process Count": 0,
            "Top Processes": []
        }

def get_memory_info() -> Dict[str, float]:
    """Get memory usage information."""
    try:
        memory_status = MEMORYSTATUSEX()
        memory_status.dwLength = ctypes.sizeof(MEMORYSTATUSEX)
        
        if not ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(memory_status)):
            raise Exception("Failed to get memory status")
            
        total_memory = memory_status.ullTotalPhys / MB_CONVERSION
        available_memory = memory_status.ullAvailPhys / MB_CONVERSION
        memory_load = memory_status.dwMemoryLoad
        
        return {
            "Total Memory (MB)": round(total_memory, 2),
            "Available Memory (MB)": round(available_memory, 2),
            "Memory Usage (%)": memory_load
        }
    except Exception as e:
        print(f"Error getting memory info: {str(e)}")
        return {
            "Total Memory (MB)": 0.0,
            "Available Memory (MB)": 0.0,
            "Memory Usage (%)": 0.0
        }

def get_disk_info(drive_letter: str = "C:") -> Dict[str, float]:
    """Get disk usage information for a specific drive."""
    try:
        if not os.path.exists(f"{drive_letter}\\"):
            raise Exception(f"Drive {drive_letter} does not exist")
            
        free_bytes = ctypes.c_uint64()
        total_bytes = ctypes.c_uint64()
        total_free_bytes = ctypes.c_uint64()
        
        if not ctypes.windll.kernel32.GetDiskFreeSpaceExW(
            ctypes.c_wchar_p(f"{drive_letter}\\"),
            ctypes.byref(free_bytes),
            ctypes.byref(total_bytes),
            ctypes.byref(total_free_bytes)
        ):
            raise Exception(f"Failed to get disk information for {drive_letter}")
            
        total_space_mb = total_bytes.value / MB_CONVERSION
        free_space_mb = total_free_bytes.value / MB_CONVERSION
        
        return {
            "Drive": drive_letter,
            "Total Disk Space (MB)": round(total_space_mb, 2),
            "Free Disk Space (MB)": round(free_space_mb, 2),
            "Disk Usage (%)": round((1 - (free_space_mb / total_space_mb)) * 100, 2)
        }
    except Exception as e:
        print(f"Error getting disk info for {drive_letter}: {str(e)}")
        return {
            "Drive": drive_letter,
            "Total Disk Space (MB)": 0.0,
            "Free Disk Space (MB)": 0.0,
            "Disk Usage (%)": 0.0
        }

def get_all_disk_info() -> List[Dict[str, float]]:
    """Get disk usage information for all available drives."""
    drives = []
    for letter in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        drive = f"{letter}:"
        if os.path.exists(f"{drive}\\"):
            drives.append(get_disk_info(drive))
    return drives

def get_top_memory_processes(n: int = 5):
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
        try:
            pinfo = proc.info
            mem_mb = pinfo['memory_info'].rss / (1024 * 1024)
            processes.append({
                'pid': pinfo['pid'],
                'name': pinfo['name'],
                'memory_mb': round(mem_mb, 2)
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    processes.sort(key=lambda x: x['memory_mb'], reverse=True)
    return processes[:n]
