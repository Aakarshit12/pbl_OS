"""
Error Detection and Handling Module
Manages exceptions and error reporting
"""
import sys
import traceback
import logging
from typing import Callable, Dict, Any, Optional
import colorama
from colorama import Fore, Style


class ErrorHandler:
    """Handles errors and exceptions in the system analyzer"""
    
    def __init__(self, log_file: str = 'system_analyzer_errors.log'):
        """Initialize error handler
        
        Args:
            log_file: Path to error log file
        """
        self.log_file = log_file
        
        # Configure logging
        logging.basicConfig(
            filename=self.log_file,
            level=logging.ERROR,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Initialize colorama for colored terminal output
        colorama.init()
    
    def handle_error(self, error: Exception, component: str, details: Optional[Dict[str, Any]] = None) -> None:
        """Handle and log an error
        
        Args:
            error: The exception object
            component: Component name where the error occurred
            details: Additional details about the context
        """
        # Format the error message
        error_type = type(error).__name__
        error_message = str(error)
        error_traceback = traceback.format_exc()
        
        # Create structured error info
        error_info = {
            'component': component,
            'error_type': error_type,
            'error_message': error_message,
            'traceback': error_traceback
        }
        
        # Add any additional details
        if details:
            error_info.update(details)
        
        # Log the error
        logging.error(f"Error in {component}: {error_type} - {error_message}")
        logging.error(f"Details: {details}")
        logging.error(f"Traceback: {error_traceback}")
        
        # Print to console with color
        print(f"{Fore.RED}ERROR in {component}: {error_type} - {error_message}{Style.RESET_ALL}")
    
    def safe_execute(self, func: Callable, component: str, *args, **kwargs) -> Any:
        """Execute a function with error handling
        
        Args:
            func: Function to execute
            component: Component name for error reporting
            *args: Arguments to pass to the function
            **kwargs: Keyword arguments to pass to the function
            
        Returns:
            Return value of the function or None if an error occurred
        """
        try:
            return func(*args, **kwargs)
        except Exception as e:
            self.handle_error(e, component, {
                'function': func.__name__,
                'args': str(args),
                'kwargs': str(kwargs)
            })
            return None
    
    def check_system_access(self) -> Dict[str, bool]:
        """Check if the program has access to required system resources
        
        Returns:
            Dict of resource names and access status
        """
        import psutil
        
        access_results = {}
        
        # Check CPU access
        try:
            psutil.cpu_percent()
            access_results['cpu'] = True
        except Exception as e:
            self.handle_error(e, 'SystemAccess', {'resource': 'CPU'})
            access_results['cpu'] = False
        
        # Check memory access
        try:
            psutil.virtual_memory()
            access_results['memory'] = True
        except Exception as e:
            self.handle_error(e, 'SystemAccess', {'resource': 'Memory'})
            access_results['memory'] = False
        
        # Check disk access
        try:
            psutil.disk_usage('/')
            access_results['disk'] = True
        except Exception as e:
            self.handle_error(e, 'SystemAccess', {'resource': 'Disk'})
            access_results['disk'] = False
        
        # Check network access
        try:
            psutil.net_io_counters()
            access_results['network'] = True
        except Exception as e:
            self.handle_error(e, 'SystemAccess', {'resource': 'Network'})
            access_results['network'] = False
        
        return access_results
    
    def validate_configuration(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate configuration parameters
        
        Args:
            config: Configuration dictionary
            
        Returns:
            Dict with validation results and corrected values
        """
        validated = {}
        errors = []
        
        # Validate interval
        try:
            interval = float(config.get('interval', 1.0))
            if interval < 0.1:
                errors.append("Interval too small, set to minimum 0.1s")
                interval = 0.1
            validated['interval'] = interval
        except (ValueError, TypeError):
            errors.append("Invalid interval value, using default 1.0s")
            validated['interval'] = 1.0
        
        # Validate duration
        try:
            duration = int(config.get('duration', 0))
            if duration < 0:
                errors.append("Negative duration value, set to 0 (continuous)")
                duration = 0
            validated['duration'] = duration
        except (ValueError, TypeError):
            errors.append("Invalid duration value, using default 0 (continuous)")
            validated['duration'] = 0
        
        # Validate output format
        output = config.get('output', 'live')
        if output not in ['live', 'log', 'both']:
            errors.append(f"Invalid output format '{output}', using default 'live'")
            output = 'live'
        validated['output'] = output
        
        # Validate metrics
        valid_metrics = ['cpu', 'memory', 'disk', 'network']
        metrics = config.get('metrics', valid_metrics)
        
        if isinstance(metrics, str):
            metrics = [m.strip() for m in metrics.split(',')]
        
        filtered_metrics = [m for m in metrics if m in valid_metrics]
        
        if not filtered_metrics:
            errors.append("No valid metrics specified, using all metrics")
            filtered_metrics = valid_metrics
        elif len(filtered_metrics) != len(metrics):
            errors.append("Some invalid metrics were removed")
        
        validated['metrics'] = filtered_metrics
        
        # Add validation results
        validated['is_valid'] = len(errors) == 0
        validated['errors'] = errors
        
        return validated
