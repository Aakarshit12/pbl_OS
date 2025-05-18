"""
Data Logging Module
Handles logging of system metrics for historical analysis
"""
import csv
import os
import time
import json
from typing import Dict, Any, List, Optional
from datetime import datetime


class DataLogger:
    """Logs system metrics to files for trend analysis"""
    
    def __init__(self, log_dir: str = 'logs'):
        """Initialize logger
        
        Args:
            log_dir: Directory to store log files
        """
        self.log_dir = log_dir
        self.ensure_log_directory()
        self.csv_file = None
        self.csv_writer = None
        self.current_log_file = None
    
    def ensure_log_directory(self) -> None:
        """Create log directory if it doesn't exist"""
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)
    
    def start_logging(self, processor) -> None:
        """Start a new log session
        
        Args:
            processor: DataProcessor instance to get CSV headers
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.current_log_file = os.path.join(self.log_dir, f'system_metrics_{timestamp}.csv')
        
        # Create and initialize CSV file
        self.csv_file = open(self.current_log_file, 'w', newline='')
        self.csv_writer = csv.writer(self.csv_file)
        
        # Write header row
        self.csv_writer.writerow(processor.get_csv_header())
        self.csv_file.flush()
    
    def log_data(self, processor, processed_data: Dict[str, Any]) -> None:
        """Log a single data point to CSV
        
        Args:
            processor: DataProcessor instance to get CSV row
            processed_data: Processed metrics to log
        """
        if not self.csv_writer:
            self.start_logging(processor)
        
        # Write metrics row
        self.csv_writer.writerow(processor.get_csv_row(processed_data))
        self.csv_file.flush()
    
    def export_json_snapshot(self, processed_data: Dict[str, Any], filename: Optional[str] = None) -> str:
        """Export current metrics as a JSON snapshot
        
        Args:
            processed_data: Processed metrics to export
            filename: Optional custom filename
            
        Returns:
            Path to the exported JSON file
        """
        # Create a default filename if none provided
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = os.path.join(self.log_dir, f'snapshot_{timestamp}.json')
        else:
            filename = os.path.join(self.log_dir, filename)
        
        # Write JSON data
        with open(filename, 'w') as json_file:
            json.dump(processed_data, json_file, indent=2)
        
        return filename
    
    def close(self) -> Optional[str]:
        """Close log files
        
        Returns:
            Path to the log file if it was created
        """
        if self.csv_file:
            self.csv_file.close()
            self.csv_file = None
            self.csv_writer = None
            return self.current_log_file
        return None
    
    def get_available_logs(self) -> List[str]:
        """Get list of available log files
        
        Returns:
            List of log file paths
        """
        self.ensure_log_directory()
        return [
            os.path.join(self.log_dir, f) 
            for f in os.listdir(self.log_dir) 
            if f.endswith('.csv')
        ]
