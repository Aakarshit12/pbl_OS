import sys
import argparse
from typing import Tuple, List

def parse_args() -> Tuple[int, int, bool, List[str], bool]:
    """
    Parse command line arguments with improved validation.
    Returns: (interval, duration, log_only, drives, show_progress)
    """
    parser = argparse.ArgumentParser(
        description="System Resource Monitor",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        "--interval",
        type=int,
        default=2,
        help="Sampling interval in seconds"
    )
    
    parser.add_argument(
        "--duration",
        type=int,
        default=10,
        help="Monitoring duration in seconds"
    )
    
    parser.add_argument(
        "--log-only",
        action="store_true",
        help="Only log data without displaying"
    )
    
    parser.add_argument(
        "--drives",
        type=str,
        default="C:",
        help="Comma-separated list of drives to monitor (e.g., 'C:,D:')"
    )
    
    parser.add_argument(
        "--show-progress",
        action="store_true",
        help="Show progress bar during monitoring"
    )
    
    args = parser.parse_args()
    
    # Validate arguments
    if args.interval < 1:
        print("Error: Interval must be at least 1 second")
        sys.exit(1)
        
    if args.duration < args.interval:
        print("Error: Duration must be greater than or equal to interval")
        sys.exit(1)
        
    # Parse drives
    drives = [drive.strip().upper() for drive in args.drives.split(",")]
    for drive in drives:
        if not drive.endswith(":"):
            print(f"Error: Invalid drive format '{drive}'. Use format 'X:'")
            sys.exit(1)
    
    return args.interval, args.duration, args.log_only, drives, args.show_progress
