"""
Command-Line Interface Module
Handles parsing arguments and providing user interface
"""
import argparse
import sys
import time
from typing import Dict, Any, List, Optional, Tuple
import signal
import colorama
from colorama import Fore, Style


class CommandInterface:
    """Command-line interface for the system analyzer"""
    
    def __init__(self):
        """Initialize CLI"""
        # Initialize colorama for colored terminal output
        colorama.init()
        
        # Set up signal handler for clean exit
        signal.signal(signal.SIGINT, self._signal_handler)
        
        # Flag to indicate when user wants to exit
        self.exit_requested = False
    
    def parse_arguments(self) -> Dict[str, Any]:
        """Parse command-line arguments
        
        Returns:
            Dictionary of parsed arguments
        """
        parser = argparse.ArgumentParser(
            description='System Performance Analyzer - Monitor and log system metrics',
            formatter_class=argparse.ArgumentDefaultsHelpFormatter
        )
        
        parser.add_argument(
            '--interval', 
            type=float, 
            default=1.0,
            help='Time between measurements in seconds'
        )
        
        parser.add_argument(
            '--duration', 
            type=int, 
            default=0,
            help='Total monitoring duration in seconds (0 for continuous)'
        )
        
        parser.add_argument(
            '--output', 
            choices=['live', 'log', 'both'], 
            default='live',
            help='Output format: live display, log to file, or both'
        )
        
        parser.add_argument(
            '--metrics', 
            default='cpu,memory,disk,network',
            help='Comma-separated list of metrics to monitor (cpu,memory,disk,network)'
        )
        
        parser.add_argument(
            '--log-file', 
            help='Custom log file path (default: auto-generated)'
        )
        
        parser.add_argument(
            '--gui', 
            action='store_true',
            help='Use graphical interface instead of terminal output'
        )
        
        parser.add_argument(
            '--max-points', 
            type=int, 
            default=60,
            help='Maximum data points to display in live graphs'
        )
        
        # Parse arguments
        args = parser.parse_args()
        
        # Convert comma-separated lists to actual lists
        if isinstance(args.metrics, str):
            args.metrics = [m.strip() for m in args.metrics.split(',')]
        
        # Convert to dictionary
        return vars(args)
    
    def print_welcome(self) -> None:
        """Print welcome message"""
        print(f"{Fore.CYAN}==============================================={Style.RESET_ALL}")
        print(f"{Fore.CYAN}       SYSTEM PERFORMANCE ANALYZER           {Style.RESET_ALL}")
        print(f"{Fore.CYAN}==============================================={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Real-time monitoring of system resources{Style.RESET_ALL}")
        print(f"{Fore.GREEN}Press Ctrl+C to exit{Style.RESET_ALL}")
        print("")
    
    def print_configuration(self, config: Dict[str, Any]) -> None:
        """Print current configuration
        
        Args:
            config: Configuration dictionary
        """
        print(f"{Fore.YELLOW}Configuration:{Style.RESET_ALL}")
        print(f"  Interval: {config['interval']} seconds")
        
        # Format duration
        if config['duration'] == 0:
            duration_str = "continuous"
        else:
            duration_str = f"{config['duration']} seconds"
        print(f"  Duration: {duration_str}")
        
        print(f"  Output mode: {config['output']}")
        print(f"  Monitoring: {', '.join(config['metrics'])}")
        
        if config.get('log_file'):
            print(f"  Log file: {config['log_file']}")
        
        print(f"  Display: {'GUI' if config.get('gui') else 'Terminal'}")
        print("")
    
    def print_summary(self, duration: float, log_file: Optional[str]) -> None:
        """Print monitoring summary
        
        Args:
            duration: Total monitoring duration in seconds
            log_file: Path to log file if created
        """
        print(f"\n{Fore.CYAN}==============================================={Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Monitoring Summary:{Style.RESET_ALL}")
        print(f"  Total duration: {duration:.1f} seconds")
        
        if log_file:
            print(f"  Data logged to: {log_file}")
        
        print(f"{Fore.CYAN}==============================================={Style.RESET_ALL}")
    
    def print_error(self, message: str) -> None:
        """Print error message
        
        Args:
            message: Error message to display
        """
        print(f"{Fore.RED}ERROR: {message}{Style.RESET_ALL}")
    
    def print_warning(self, message: str) -> None:
        """Print warning message
        
        Args:
            message: Warning message to display
        """
        print(f"{Fore.YELLOW}WARNING: {message}{Style.RESET_ALL}")
    
    def print_access_check(self, access_results: Dict[str, bool]) -> None:
        """Print system access check results
        
        Args:
            access_results: Dictionary of resource names and access status
        """
        print(f"{Fore.YELLOW}System Access Check:{Style.RESET_ALL}")
        
        for resource, access in access_results.items():
            status = f"{Fore.GREEN}OK{Style.RESET_ALL}" if access else f"{Fore.RED}FAILED{Style.RESET_ALL}"
            print(f"  {resource.capitalize()} access: {status}")
        
        print("")
    
    def _signal_handler(self, sig, frame) -> None:
        """Handle keyboard interrupt (Ctrl+C)
        
        Args:
            sig: Signal number
            frame: Current stack frame
        """
        print(f"\n{Fore.YELLOW}Exiting...{Style.RESET_ALL}")
        self.exit_requested = True
    
    def should_exit(self) -> bool:
        """Check if user has requested to exit
        
        Returns:
            True if exit requested, False otherwise
        """
        return self.exit_requested
