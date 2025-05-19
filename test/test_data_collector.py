import sys
import os
import unittest

# Add the parent directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_collector import get_cpu_usage, get_memory_info, get_disk_info

class TestDataCollector(unittest.TestCase):

    def test_cpu_usage(self):
        cpu_usage = get_cpu_usage()
        self.assertIsInstance(cpu_usage, float)

    def test_memory_info(self):
        memory_info = get_memory_info()
        self.assertIn("Total Memory (MB)", memory_info)

    def test_disk_info(self):
        disk_info = get_disk_info()
        self.assertIn("Total Disk Space (MB)", disk_info)

if __name__ == "__main__":
    unittest.main()
