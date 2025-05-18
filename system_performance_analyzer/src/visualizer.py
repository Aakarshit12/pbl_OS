"""
Live Data Visualization Module
Handles rendering and displaying system metrics 
"""
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import time
from typing import Dict, Any, List, Optional, Tuple
from tabulate import tabulate
import os
import colorama
from colorama import Fore, Style


class SystemVisualizer:
    """Handles visualization of system metrics"""
    
    def __init__(self, max_data_points: int = 60):
        """Initialize visualizer
        
        Args:
            max_data_points: Maximum number of data points to display in charts
        """
        self.max_data_points = max_data_points
        self.timestamps = []
        self.cpu_data = []
        self.memory_data = []
        self.swap_data = []
        self.disk_read_data = []
        self.disk_write_data = []
        self.net_send_data = []
        self.net_recv_data = []
        
        # Initialize colorama for colored terminal output
        colorama.init()
        
        # Set up the plot style
        plt.style.use('ggplot')
    
    def update_data(self, processed_data: Dict[str, Any]) -> None:
        """Update data series with new metrics
        
        Args:
            processed_data: Processed metrics data
        """
        # Append timestamp
        self.timestamps.append(processed_data['raw_timestamp'])
        
        # Ensure we don't exceed max_data_points
        if len(self.timestamps) > self.max_data_points:
            self.timestamps = self.timestamps[-self.max_data_points:]
        
        # Update CPU data
        if 'error' not in processed_data['cpu']:
            self.cpu_data.append(processed_data['cpu']['overall_percent'])
        else:
            self.cpu_data.append(0)
        
        if len(self.cpu_data) > self.max_data_points:
            self.cpu_data = self.cpu_data[-self.max_data_points:]
        
        # Update memory data
        if 'error' not in processed_data['memory']:
            self.memory_data.append(processed_data['memory']['virtual']['percent'])
            self.swap_data.append(processed_data['memory']['swap']['percent'])
        else:
            self.memory_data.append(0)
            self.swap_data.append(0)
        
        if len(self.memory_data) > self.max_data_points:
            self.memory_data = self.memory_data[-self.max_data_points:]
            self.swap_data = self.swap_data[-self.max_data_points:]
        
        # Update disk I/O data
        if 'error' not in processed_data['disk']:
            # Extract numeric values from formatted strings
            read_rate = processed_data['disk']['io']['read_rate'].split('/')[0].strip()
            write_rate = processed_data['disk']['io']['write_rate'].split('/')[0].strip()
            
            # Convert to bytes for consistent storage
            read_bytes = self._convert_to_bytes(read_rate)
            write_bytes = self._convert_to_bytes(write_rate)
            
            self.disk_read_data.append(read_bytes)
            self.disk_write_data.append(write_bytes)
        else:
            self.disk_read_data.append(0)
            self.disk_write_data.append(0)
        
        if len(self.disk_read_data) > self.max_data_points:
            self.disk_read_data = self.disk_read_data[-self.max_data_points:]
            self.disk_write_data = self.disk_write_data[-self.max_data_points:]
        
        # Update network data
        if 'error' not in processed_data['network']:
            # Extract numeric values from formatted strings
            send_rate = processed_data['network']['send_rate'].split('/')[0].strip()
            recv_rate = processed_data['network']['receive_rate'].split('/')[0].strip()
            
            # Convert to bytes for consistent storage
            send_bytes = self._convert_to_bytes(send_rate)
            recv_bytes = self._convert_to_bytes(recv_rate)
            
            self.net_send_data.append(send_bytes)
            self.net_recv_data.append(recv_bytes)
        else:
            self.net_send_data.append(0)
            self.net_recv_data.append(0)
        
        if len(self.net_send_data) > self.max_data_points:
            self.net_send_data = self.net_send_data[-self.max_data_points:]
            self.net_recv_data = self.net_recv_data[-self.max_data_points:]
    
    def _convert_to_bytes(self, formatted_str: str) -> float:
        """Convert a formatted string (e.g., '4.5 MB') to bytes
        
        Args:
            formatted_str: Formatted string with unit
            
        Returns:
            Value in bytes
        """
        try:
            parts = formatted_str.split()
            if len(parts) != 2:
                return 0
            
            value = float(parts[0])
            unit = parts[1]
            
            # Convert based on unit
            if unit == 'B':
                return value
            elif unit == 'KB':
                return value * 1024
            elif unit == 'MB':
                return value * 1024 * 1024
            elif unit == 'GB':
                return value * 1024 * 1024 * 1024
            elif unit == 'TB':
                return value * 1024 * 1024 * 1024 * 1024
            else:
                return 0
        except Exception:
            return 0
    
    def _format_bytes_for_display(self, bytes_value: float) -> str:
        """Convert bytes to appropriate unit for display
        
        Args:
            bytes_value: Value in bytes
            
        Returns:
            Formatted string
        """
        units = ['B', 'KB', 'MB', 'GB', 'TB']
        unit_index = 0
        
        while bytes_value >= 1024 and unit_index < len(units) - 1:
            bytes_value /= 1024
            unit_index += 1
        
        return f"{bytes_value:.2f} {units[unit_index]}/s"
    
    def display_terminal(self, processed_data: Dict[str, Any]) -> None:
        """Display metrics in terminal
        
        Args:
            processed_data: Processed metrics data
        """
        os.system('cls' if os.name == 'nt' else 'clear')
        
        # Create header
        print(f"{Fore.CYAN}======= SYSTEM PERFORMANCE MONITOR ======={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Time: {processed_data['timestamp']}{Style.RESET_ALL}")
        print("")
        
        # CPU Information
        print(f"{Fore.GREEN}CPU USAGE:{Style.RESET_ALL}")
        if 'error' not in processed_data['cpu']:
            cpu_data = processed_data['cpu']
            overall_percent = cpu_data['overall_percent']
            
            # Color-code based on usage
            color = Fore.GREEN
            if overall_percent > 50:
                color = Fore.YELLOW
            if overall_percent > 80:
                color = Fore.RED
            
            print(f"  Overall: {color}{overall_percent:.1f}%{Style.RESET_ALL}")
            
            # Per-core data
            if 'per_core_percent' in cpu_data:
                core_data = []
                for i, percent in enumerate(cpu_data['per_core_percent']):
                    # Color-code based on usage
                    color = Fore.GREEN
                    if percent > 50:
                        color = Fore.YELLOW
                    if percent > 80:
                        color = Fore.RED
                    
                    core_data.append(f"Core {i}: {color}{percent:.1f}%{Style.RESET_ALL}")
                
                # Print in columns (4 cores per row)
                for i in range(0, len(core_data), 4):
                    print("  " + "  ".join(core_data[i:i+4]))
            
            # CPU frequency
            if 'frequency' in cpu_data:
                print(f"  Frequency: {cpu_data['frequency']['current']}")
            
            # Load average
            if 'load_avg' in cpu_data:
                load = cpu_data['load_avg']
                print(f"  Load Average: 1min: {load['1min']:.2f}, 5min: {load['5min']:.2f}, 15min: {load['15min']:.2f}")
        else:
            print(f"  {Fore.RED}Error: {processed_data['cpu']['error']}{Style.RESET_ALL}")
        
        print("")
        
        # Memory Information
        print(f"{Fore.GREEN}MEMORY USAGE:{Style.RESET_ALL}")
        if 'error' not in processed_data['memory']:
            memory = processed_data['memory']['virtual']
            swap = processed_data['memory']['swap']
            
            # Color-code based on usage
            memory_color = Fore.GREEN
            if memory['percent'] > 50:
                memory_color = Fore.YELLOW
            if memory['percent'] > 80:
                memory_color = Fore.RED
                
            swap_color = Fore.GREEN
            if swap['percent'] > 50:
                swap_color = Fore.YELLOW
            if swap['percent'] > 80:
                swap_color = Fore.RED
            
            print(f"  RAM: {memory_color}{memory['percent']:.1f}%{Style.RESET_ALL} (Used: {memory['used']} / Total: {memory['total']})")
            print(f"  Swap: {swap_color}{swap['percent']:.1f}%{Style.RESET_ALL} (Used: {swap['used']} / Total: {swap['total']})")
        else:
            print(f"  {Fore.RED}Error: {processed_data['memory']['error']}{Style.RESET_ALL}")
        
        print("")
        
        # Disk Information
        print(f"{Fore.GREEN}DISK USAGE:{Style.RESET_ALL}")
        if 'error' not in processed_data['disk']:
            # Disk partitions
            partitions = processed_data['disk']['partitions']
            headers = ["Device", "Mount", "Total", "Used", "Free", "Usage"]
            partition_data = []
            
            for p in partitions:
                # Color-code based on usage
                usage_color = Fore.GREEN
                if p['percent'] > 70:
                    usage_color = Fore.YELLOW
                if p['percent'] > 90:
                    usage_color = Fore.RED
                
                partition_data.append([
                    p['device'], 
                    p['mountpoint'], 
                    p['total'], 
                    p['used'], 
                    p['free'], 
                    f"{usage_color}{p['percent']:.1f}%{Style.RESET_ALL}"
                ])
            
            print(tabulate(partition_data, headers=headers, tablefmt="simple"))
            
            # Disk I/O
            io = processed_data['disk']['io']
            print(f"\n  I/O Read:  {io['read_rate']}  |  Write: {io['write_rate']}")
            print(f"  Operations: {io['read_count']} reads, {io['write_count']} writes")
        else:
            print(f"  {Fore.RED}Error: {processed_data['disk']['error']}{Style.RESET_ALL}")
        
        print("")
        
        # Network Information
        print(f"{Fore.GREEN}NETWORK USAGE:{Style.RESET_ALL}")
        if 'error' not in processed_data['network']:
            network = processed_data['network']
            print(f"  Upload:   {network['send_rate']}  |  Total: {network['total_sent']}")
            print(f"  Download: {network['receive_rate']}  |  Total: {network['total_received']}")
            print(f"  Packets:  {network['packets_sent']} sent, {network['packets_received']} received")
        else:
            print(f"  {Fore.RED}Error: {processed_data['network']['error']}{Style.RESET_ALL}")
        
        print("\n" + "=" * 40)
        print(f"{Fore.YELLOW}Press Ctrl+C to stop monitoring{Style.RESET_ALL}")
    
    def create_plots(self) -> Figure:
        """Create matplotlib plot with all metrics
        
        Returns:
            Matplotlib figure
        """
        fig, axs = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle('System Performance Metrics', fontsize=16)
        
        # Adjust timestamps for x-axis (relative time in seconds)
        if self.timestamps:
            x_values = [t - self.timestamps[0] for t in self.timestamps]
        else:
            x_values = []
        
        # CPU and Memory Plot (top left)
        ax1 = axs[0, 0]
        ax1.set_title('CPU & Memory Usage')
        ax1.set_ylabel('Usage %')
        ax1.set_xlabel('Time (seconds)')
        ax1.set_ylim(0, 100)
        
        if x_values:
            ax1.plot(x_values, self.cpu_data, 'r-', label='CPU')
            ax1.plot(x_values, self.memory_data, 'b-', label='RAM')
            ax1.plot(x_values, self.swap_data, 'g-', label='Swap')
        
        ax1.legend(loc='upper left')
        ax1.grid(True)
        
        # Disk I/O Plot (top right)
        ax2 = axs[0, 1]
        ax2.set_title('Disk I/O')
        ax2.set_ylabel('Bytes/s')
        ax2.set_xlabel('Time (seconds)')
        
        if x_values:
            ax2.plot(x_values, self.disk_read_data, 'g-', label='Read')
            ax2.plot(x_values, self.disk_write_data, 'm-', label='Write')
        
        ax2.legend(loc='upper left')
        ax2.grid(True)
        
        # Use log scale if values are large enough
        if any(v > 1000000 for v in self.disk_read_data + self.disk_write_data):
            ax2.set_yscale('log')
        
        # Network Plot (bottom left)
        ax3 = axs[1, 0]
        ax3.set_title('Network I/O')
        ax3.set_ylabel('Bytes/s')
        ax3.set_xlabel('Time (seconds)')
        
        if x_values:
            ax3.plot(x_values, self.net_send_data, 'c-', label='Upload')
            ax3.plot(x_values, self.net_recv_data, 'y-', label='Download')
        
        ax3.legend(loc='upper left')
        ax3.grid(True)
        
        # Use log scale if values are large enough
        if any(v > 1000000 for v in self.net_send_data + self.net_recv_data):
            ax3.set_yscale('log')
        
        # CPU Load Bar Chart (bottom right)
        ax4 = axs[1, 1]
        ax4.set_title('Current System Load')
        
        # Create bar chart with current metrics
        if self.cpu_data and self.memory_data and self.swap_data:
            categories = ['CPU', 'Memory', 'Swap']
            values = [self.cpu_data[-1], self.memory_data[-1], self.swap_data[-1]]
            colors = ['red', 'blue', 'green']
            
            # Create horizontal bar chart
            bars = ax4.barh(categories, values, color=colors)
            ax4.set_xlim(0, 100)
            ax4.set_xlabel('Usage %')
            
            # Add value labels
            for i, bar in enumerate(bars):
                width = bar.get_width()
                ax4.text(width + 1, bar.get_y() + bar.get_height()/2, f'{values[i]:.1f}%', 
                         ha='left', va='center')
        
        plt.tight_layout(rect=[0, 0, 1, 0.95])  # Adjust for the title
        return fig
    
    def display_gui(self, processed_data: Dict[str, Any]) -> None:
        """Display metrics in a GUI window
        
        Args:
            processed_data: Processed metrics data
        """
        # Update data series
        self.update_data(processed_data)
        
        # Create plots
        fig = self.create_plots()
        
        # Display the plots
        plt.pause(0.01)  # Small pause to update the plots
    
    def close_gui(self) -> None:
        """Close all plot windows"""
        plt.close('all')
