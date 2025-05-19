import time
from typing import List, Dict, Any
from data_collector import get_cpu_usage, get_memory_info, get_disk_info, get_all_disk_info, get_top_memory_processes
from data_processor import format_data
from logger import log_data
from cli import parse_args
from utils import handle_error

def print_progress(current: int, total: int, width: int = 50) -> None:
    """Print a progress bar."""
    progress = int(width * current / total)
    bar = "█" * progress + "░" * (width - progress)
    print(f"\rProgress: [{bar}] {current}/{total} samples", end="", flush=True)

def display_metrics(cpu_data: Dict[str, Any], memory_data: Dict[str, float], disk_data: List[Dict[str, float]], top_mem: List[Dict[str, Any]]) -> None:
    """Display system metrics in a formatted way."""
    print("\n" + "=" * 50)
    print(f"CPU Usage: {cpu_data['Overall CPU Usage (%)']}%")
    print(f"Memory Usage: {memory_data['Memory Usage (%)']}%")
    print(f"Available Memory: {memory_data['Available Memory (MB)']:.2f} MB")
    
    for disk in disk_data:
        print(f"\nDrive {disk['Drive']}:")
        print(f"  Total Space: {disk['Total Disk Space (MB)']:.2f} MB")
        print(f"  Free Space: {disk['Free Disk Space (MB)']:.2f} MB")
        print(f"  Usage: {disk['Disk Usage (%)']}%")
    print("\nTop Memory Processes:")
    for proc in top_mem:
        print(f"  {proc['name']} (PID {proc['pid']}): {proc['memory_mb']} MB")
    print("=" * 50)

def main():
    try:
        interval, duration, log_only, drives, show_progress = parse_args()
        data_log = []
        total_samples = duration // interval
        
        print(f"Starting system monitoring for {duration} seconds...")
        print(f"Sampling interval: {interval} seconds")
        print(f"Monitoring drives: {', '.join(drives)}")
        print("-" * 50)
        
        for i in range(total_samples):
            # Collect system metrics
            cpu_data = get_cpu_usage()
            memory_data = get_memory_info()
            disk_data = [get_disk_info(drive) for drive in drives]
            top_mem = get_top_memory_processes()
            
            # Format and log data
            formatted_data = format_data(cpu_data, memory_data, disk_data, top_mem)
            log_data(formatted_data)
            data_log.append(formatted_data)
            
            # Display metrics if not in log-only mode
            if not log_only:
                if show_progress:
                    print_progress(i + 1, total_samples)
                display_metrics(cpu_data, memory_data, disk_data, top_mem)
            
            # Sleep until next sample
            if i < total_samples - 1:  # Don't sleep after the last sample
                time.sleep(interval)
        
        if show_progress:
            print()  # New line after progress bar
        
        print("\nMonitoring complete!")
        print(f"Data has been logged to performance_log.csv")
        
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user.")
    except Exception as e:
        handle_error(str(e))

if __name__ == "__main__":
    main()
