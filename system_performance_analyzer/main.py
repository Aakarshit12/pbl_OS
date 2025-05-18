#!/usr/bin/env python3
"""
System Performance Analyzer
Main entry point that orchestrates all components
"""
import time
import sys
import os
from datetime import datetime

# Import components
from src.collector import SystemDataCollector
from src.processor import DataProcessor
from src.visualizer import SystemVisualizer
from src.logger import DataLogger
from src.error_handler import ErrorHandler
from src.cli import CommandInterface


def main():
    """Main entry point for the System Performance Analyzer"""
    # Initialize command interface
    cli = CommandInterface()
    cli.print_welcome()
    
    # Parse command-line arguments
    config = cli.parse_arguments()
    
    # Initialize error handler
    error_handler = ErrorHandler()
    
    # Validate configuration
    validated_config = error_handler.validate_configuration(config)
    if not validated_config['is_valid']:
        for error in validated_config['errors']:
            cli.print_warning(error)
    
    # Replace config with validated config
    for key, value in validated_config.items():
        if key not in ['is_valid', 'errors']:
            config[key] = value
    
    # Print current configuration
    cli.print_configuration(config)
    
    # Check system access
    access_results = error_handler.check_system_access()
    cli.print_access_check(access_results)
    
    # Initialize components
    collector = SystemDataCollector()
    processor = DataProcessor()
    visualizer = SystemVisualizer(max_data_points=config.get('max_points', 60))
    logger = DataLogger()
    
    # Start logging if needed
    if config['output'] in ['log', 'both']:
        logger.start_logging(processor)
    
    # Main monitoring loop
    start_time = time.time()
    iteration = 0
    
    try:
        while True:
            # Check if duration limit reached
            current_time = time.time()
            elapsed_time = current_time - start_time
            
            if config['duration'] > 0 and elapsed_time >= config['duration']:
                break
            
            # Check if user requested exit
            if cli.should_exit():
                break
            
            # Collect all metrics
            raw_data = collector.collect_all()
            
            # Process the raw data
            processed_data = processor.process_all(raw_data)
            
            # Display metrics
            if config['output'] in ['live', 'both']:
                if config.get('gui', False):
                    # GUI display
                    visualizer.display_gui(processed_data)
                else:
                    # Terminal display
                    visualizer.display_terminal(processed_data)
            
            # Log data
            if config['output'] in ['log', 'both']:
                logger.log_data(processor, processed_data)
            
            # Sleep for the interval
            iteration += 1
            
            # Calculate precise sleep time to maintain interval
            next_iteration_time = start_time + (iteration * config['interval'])
            sleep_time = max(0, next_iteration_time - time.time())
            
            if sleep_time > 0:
                time.sleep(sleep_time)
    
    except KeyboardInterrupt:
        pass
    except Exception as e:
        error_handler.handle_error(e, 'MainLoop')
    
    finally:
        # Clean up
        end_time = time.time()
        total_duration = end_time - start_time
        
        # Close logger and get log file path
        log_file = logger.close()
        
        # Close visualizer if using GUI
        if config.get('gui', False):
            visualizer.close_gui()
        
        # Print summary
        cli.print_summary(total_duration, log_file)


if __name__ == '__main__':
    main()
