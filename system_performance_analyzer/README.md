# System Performance Analyzer

A lightweight system monitoring tool for educational and practical purposes that collects, processes, visualizes, and logs system performance metrics.

## Features

- Real-time system metrics collection (CPU, memory, disk I/O)
- Data processing and formatting
- Live visualization of system metrics
- Historical data logging for trend analysis
- Error detection and handling
- Flexible command-line interface

## Installation

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

Run the analyzer with default settings:
```
python main.py
```

Customize monitoring options:
```
python main.py --interval 2 --duration 60 --output live --metrics cpu,memory,disk
```

Available options:
- `--interval`: Time between measurements (seconds)
- `--duration`: Total monitoring duration (seconds, 0 for continuous)
- `--output`: Output format (live, log, both)
- `--metrics`: Metrics to monitor (cpu, memory, disk)
- `--log-file`: Custom log file path

## Components

1. **System Data Collection**: Uses psutil to gather system metrics
2. **Data Processing**: Formats raw data into usable metrics
3. **Visualization**: Displays metrics in real-time using matplotlib
4. **Data Logging**: Records metrics with timestamps for trend analysis
5. **Error Handling**: Manages exceptions and access issues
6. **CLI**: Provides a flexible interface for configuration

## Example Output

The tool provides both terminal-based and graphical visualization of system metrics, along with CSV logs for further analysis.

## License

Open source for educational purposes.
