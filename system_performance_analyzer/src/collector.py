"""
System Data Collection Module
Handles collection of system metrics using psutil
"""
import psutil
import time
from typing import Dict, Any, List, Optional


class SystemDataCollector:
    """Collects raw system performance metrics"""
    
    def __init__(self):
        """Initialize the collector"""
        self.last_disk_io = psutil.disk_io_counters()
        self.last_net_io = psutil.net_io_counters()
        self.last_time = time.time()
    
    def collect_cpu_metrics(self) -> Dict[str, Any]:
        """Collect CPU usage metrics
        
        Returns:
            Dict with CPU usage percentage (overall and per-core)
        """
        try:
            return {
                'cpu_percent': psutil.cpu_percent(interval=0.1),
                'cpu_percent_per_core': psutil.cpu_percent(interval=0.1, percpu=True),
                'cpu_count': psutil.cpu_count(),
                'cpu_freq': psutil.cpu_freq(),
                'cpu_stats': psutil.cpu_stats(),
                'cpu_times': psutil.cpu_times(),
                'load_avg': psutil.getloadavg() if hasattr(psutil, 'getloadavg') else None
            }
        except Exception as e:
            return {'error': str(e)}
    
    def collect_memory_metrics(self) -> Dict[str, Any]:
        """Collect memory usage metrics
        
        Returns:
            Dict with memory usage information
        """
        try:
            virtual_memory = psutil.virtual_memory()
            swap_memory = psutil.swap_memory()
            
            return {
                'virtual_memory': {
                    'total': virtual_memory.total,
                    'available': virtual_memory.available,
                    'used': virtual_memory.used,
                    'percent': virtual_memory.percent
                },
                'swap_memory': {
                    'total': swap_memory.total,
                    'used': swap_memory.used,
                    'free': swap_memory.free,
                    'percent': swap_memory.percent
                }
            }
        except Exception as e:
            return {'error': str(e)}
    
    def collect_disk_metrics(self) -> Dict[str, Any]:
        """Collect disk usage and I/O metrics
        
        Returns:
            Dict with disk usage and I/O information
        """
        try:
            current_time = time.time()
            time_delta = current_time - self.last_time
            
            # Get disk partitions
            partitions = []
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    partitions.append({
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'fstype': partition.fstype,
                        'total': usage.total,
                        'used': usage.used,
                        'free': usage.free,
                        'percent': usage.percent
                    })
                except PermissionError:
                    # Some drives might not be accessible
                    pass
            
            # Calculate disk I/O rates
            current_disk_io = psutil.disk_io_counters()
            
            # Calculate rates
            read_bytes_rate = (current_disk_io.read_bytes - self.last_disk_io.read_bytes) / time_delta
            write_bytes_rate = (current_disk_io.write_bytes - self.last_disk_io.write_bytes) / time_delta
            
            # Update last values
            self.last_disk_io = current_disk_io
            self.last_time = current_time
            
            return {
                'partitions': partitions,
                'io': {
                    'read_bytes': current_disk_io.read_bytes,
                    'write_bytes': current_disk_io.write_bytes,
                    'read_count': current_disk_io.read_count,
                    'write_count': current_disk_io.write_count,
                    'read_rate': read_bytes_rate,
                    'write_rate': write_bytes_rate
                }
            }
        except Exception as e:
            return {'error': str(e)}
    
    def collect_network_metrics(self) -> Dict[str, Any]:
        """Collect network I/O metrics
        
        Returns:
            Dict with network I/O information
        """
        try:
            current_time = time.time()
            time_delta = current_time - self.last_time
            
            current_net_io = psutil.net_io_counters()
            
            # Calculate rates
            bytes_sent_rate = (current_net_io.bytes_sent - self.last_net_io.bytes_sent) / time_delta
            bytes_recv_rate = (current_net_io.bytes_recv - self.last_net_io.bytes_recv) / time_delta
            
            # Update last values
            self.last_net_io = current_net_io
            
            return {
                'bytes_sent': current_net_io.bytes_sent,
                'bytes_recv': current_net_io.bytes_recv,
                'packets_sent': current_net_io.packets_sent,
                'packets_recv': current_net_io.packets_recv,
                'bytes_sent_rate': bytes_sent_rate,
                'bytes_recv_rate': bytes_recv_rate
            }
        except Exception as e:
            return {'error': str(e)}
    
    def collect_all(self) -> Dict[str, Any]:
        """Collect all system metrics
        
        Returns:
            Dict with all system metrics
        """
        return {
            'timestamp': time.time(),
            'cpu': self.collect_cpu_metrics(),
            'memory': self.collect_memory_metrics(),
            'disk': self.collect_disk_metrics(),
            'network': self.collect_network_metrics()
        }
