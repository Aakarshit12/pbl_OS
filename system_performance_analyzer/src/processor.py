"""
Data Processing Module
Processes and formats raw system metrics data
"""
from typing import Dict, Any, List
import time
import datetime


class DataProcessor:
    """Processes raw system metrics into meaningful and formatted data"""
    
    @staticmethod
    def format_bytes(bytes_value: int) -> str:
        """Convert bytes to human-readable format
        
        Args:
            bytes_value: Value in bytes
            
        Returns:
            Human-readable string (e.g., '4.2 GB')
        """
        if bytes_value is None:
            return "N/A"
        
        for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
            if bytes_value < 1024.0 or unit == 'TB':
                return f"{bytes_value:.2f} {unit}"
            bytes_value /= 1024.0
    
    @staticmethod
    def format_timestamp(timestamp: float) -> str:
        """Convert timestamp to human-readable format
        
        Args:
            timestamp: Unix timestamp
            
        Returns:
            Formatted date/time string
        """
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
    @staticmethod
    def process_cpu_data(cpu_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process CPU metrics
        
        Args:
            cpu_data: Raw CPU metrics
            
        Returns:
            Processed CPU metrics
        """
        if 'error' in cpu_data:
            return cpu_data
        
        result = {
            'overall_percent': cpu_data['cpu_percent'],
            'per_core_percent': cpu_data['cpu_percent_per_core'],
            'core_count': cpu_data['cpu_count'],
        }
        
        # Add CPU frequency if available
        if cpu_data.get('cpu_freq'):
            result['frequency'] = {
                'current': f"{cpu_data['cpu_freq'].current:.2f} MHz" if cpu_data['cpu_freq'].current else "N/A",
                'min': f"{cpu_data['cpu_freq'].min:.2f} MHz" if hasattr(cpu_data['cpu_freq'], 'min') and cpu_data['cpu_freq'].min else "N/A",
                'max': f"{cpu_data['cpu_freq'].max:.2f} MHz" if hasattr(cpu_data['cpu_freq'], 'max') and cpu_data['cpu_freq'].max else "N/A"
            }
        
        # Add load average if available
        if cpu_data.get('load_avg'):
            result['load_avg'] = {
                '1min': cpu_data['load_avg'][0],
                '5min': cpu_data['load_avg'][1],
                '15min': cpu_data['load_avg'][2]
            }
        
        return result
    
    @staticmethod
    def process_memory_data(memory_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process memory metrics
        
        Args:
            memory_data: Raw memory metrics
            
        Returns:
            Processed memory metrics
        """
        if 'error' in memory_data:
            return memory_data
        
        virtual = memory_data['virtual_memory']
        swap = memory_data['swap_memory']
        
        return {
            'virtual': {
                'total': DataProcessor.format_bytes(virtual['total']),
                'available': DataProcessor.format_bytes(virtual['available']),
                'used': DataProcessor.format_bytes(virtual['used']),
                'percent': virtual['percent']
            },
            'swap': {
                'total': DataProcessor.format_bytes(swap['total']),
                'used': DataProcessor.format_bytes(swap['used']),
                'free': DataProcessor.format_bytes(swap['free']),
                'percent': swap['percent']
            }
        }
    
    @staticmethod
    def process_disk_data(disk_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process disk metrics
        
        Args:
            disk_data: Raw disk metrics
            
        Returns:
            Processed disk metrics
        """
        if 'error' in disk_data:
            return disk_data
        
        processed_partitions = []
        for partition in disk_data['partitions']:
            processed_partitions.append({
                'device': partition['device'],
                'mountpoint': partition['mountpoint'],
                'fstype': partition['fstype'],
                'total': DataProcessor.format_bytes(partition['total']),
                'used': DataProcessor.format_bytes(partition['used']),
                'free': DataProcessor.format_bytes(partition['free']),
                'percent': partition['percent']
            })
        
        io = disk_data['io']
        return {
            'partitions': processed_partitions,
            'io': {
                'read_total': DataProcessor.format_bytes(io['read_bytes']),
                'write_total': DataProcessor.format_bytes(io['write_bytes']),
                'read_count': io['read_count'],
                'write_count': io['write_count'],
                'read_rate': f"{DataProcessor.format_bytes(io['read_rate'])}/s",
                'write_rate': f"{DataProcessor.format_bytes(io['write_rate'])}/s"
            }
        }
    
    @staticmethod
    def process_network_data(network_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process network metrics
        
        Args:
            network_data: Raw network metrics
            
        Returns:
            Processed network metrics
        """
        if 'error' in network_data:
            return network_data
        
        return {
            'total_sent': DataProcessor.format_bytes(network_data['bytes_sent']),
            'total_received': DataProcessor.format_bytes(network_data['bytes_recv']),
            'packets_sent': network_data['packets_sent'],
            'packets_received': network_data['packets_recv'],
            'send_rate': f"{DataProcessor.format_bytes(network_data['bytes_sent_rate'])}/s",
            'receive_rate': f"{DataProcessor.format_bytes(network_data['bytes_recv_rate'])}/s"
        }
    
    def process_all(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process all system metrics
        
        Args:
            raw_data: Raw metrics from collector
            
        Returns:
            Processed system metrics
        """
        return {
            'timestamp': self.format_timestamp(raw_data['timestamp']),
            'raw_timestamp': raw_data['timestamp'],  # Keep raw timestamp for plotting
            'cpu': self.process_cpu_data(raw_data['cpu']),
            'memory': self.process_memory_data(raw_data['memory']),
            'disk': self.process_disk_data(raw_data['disk']),
            'network': self.process_network_data(raw_data['network'])
        }
    
    def get_csv_header(self) -> List[str]:
        """Get CSV header for logging
        
        Returns:
            List of column headers
        """
        return [
            'timestamp',
            'cpu_percent',
            'memory_percent',
            'swap_percent',
            'disk_read_rate',
            'disk_write_rate',
            'network_send_rate',
            'network_receive_rate'
        ]
    
    def get_csv_row(self, processed_data: Dict[str, Any]) -> List[Any]:
        """Extract CSV row data from processed metrics
        
        Args:
            processed_data: Processed metrics
            
        Returns:
            List of values for CSV row
        """
        # Extract values from processed data for CSV logging
        cpu_percent = processed_data['cpu']['overall_percent'] if 'error' not in processed_data['cpu'] else -1
        memory_percent = processed_data['memory']['virtual']['percent'] if 'error' not in processed_data['memory'] else -1
        swap_percent = processed_data['memory']['swap']['percent'] if 'error' not in processed_data['memory'] else -1
        
        # Extract rates (removing the "/s" suffix and converting back to raw numbers for plotting)
        if 'error' not in processed_data['disk']:
            disk_read_rate = processed_data['disk']['io']['read_rate'].split('/')[0].strip()
            disk_write_rate = processed_data['disk']['io']['write_rate'].split('/')[0].strip()
        else:
            disk_read_rate = "-1 B"
            disk_write_rate = "-1 B"
        
        if 'error' not in processed_data['network']:
            network_send_rate = processed_data['network']['send_rate'].split('/')[0].strip()
            network_receive_rate = processed_data['network']['receive_rate'].split('/')[0].strip()
        else:
            network_send_rate = "-1 B"
            network_receive_rate = "-1 B"
        
        return [
            processed_data['raw_timestamp'],
            cpu_percent,
            memory_percent,
            swap_percent,
            disk_read_rate,
            disk_write_rate,
            network_send_rate,
            network_receive_rate
        ]
