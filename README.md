# System Resource Monitor

A Python-based system monitoring tool that tracks and logs CPU usage, memory consumption, disk space, and process information in real-time.

## Features

- Real-time monitoring of system resources:
  - CPU usage
  - Memory usage and availability
  - Disk space utilization
  - Top memory-consuming processes
- Configurable monitoring intervals and duration
- Progress bar visualization
- Data logging to CSV format
- Command-line interface with multiple options

## Requirements

- Python 3.x
- Windows operating system
- Required Python packages:
  - psutil
  - typing

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Aakarshit12/pbl_OS.git
cd pbl_OS
```

2. Install required dependencies:
```bash
pip install psutil
```

## Usage

Run the script with default settings:
```bash
python main.py
```

### Command Line Options

- `--interval`: Sampling interval in seconds (default: 2)
- `--duration`: Monitoring duration in seconds (default: 10)
- `--log-only`: Only log data without displaying
- `--drives`: Comma-separated list of drives to monitor (default: "C:")
- `--show-progress`: Show progress bar during monitoring

### Examples

Monitor system for 30 seconds with 5-second intervals:
```bash
python main.py --interval 5 --duration 30
```

Monitor multiple drives:
```bash
python main.py --drives "C:,D:"
```

Log data without displaying:
```bash
python main.py --log-only
```

## Project Structure

- `main.py`: Main application entry point
- `cli.py`: Command-line interface implementation
- `data_collector.py`: System metrics collection
- `data_processor.py`: Data processing and formatting
- `logger.py`: Logging functionality
- `utils.py`: Utility functions
- `visualizer.py`: Data visualization components
- `performance_log.csv`: Logged performance data

## Output

The tool provides real-time display of:
- CPU usage percentage
- Memory usage and available memory
- Disk space information for specified drives
- Top memory-consuming processes

All data is also logged to `performance_log.csv` for later analysis.

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is open source and available under the MIT License. 