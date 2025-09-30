#!/usr/bin/env python3

import sys
import datetime
import re
from collections import Counter

def analyze_logs(log_file="system_health.log"):
    """Analyze log file and generate report"""
    
    try:
        with open(log_file, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"Error: Log file '{log_file}' not found!")
        print("Please run the health checker first to generate logs.")
        return
    
    # Initialize counters
    report_data = {
        'total_entries': len(lines),
        'info_count': 0,
        'error_count': 0,
        'cpu_usage_samples': [],
        'recent_entries': lines[-5:] if len(lines) >= 5 else lines,
        'error_entries': []
    }
    
    # Analyze each line
    for line in lines:
        if any(keyword in line for keyword in ["Starting system health check", "check completed", "completed successfully"]):
            report_data['info_count'] += 1
        elif "ERROR" in line:
            report_data['error_count'] += 1
            report_data['error_entries'].append(line.strip())
        if "CPU Usage" in line:
            report_data['cpu_usage_samples'].append(line.strip())
    
    # Generate report
    report_file = "log_analysis_report.txt"
    with open(report_file, 'w') as f:
        f.write("==========================================\n")
        f.write("     LOG ANALYSIS REPORT (PYTHON)\n")
        f.write("==========================================\n")
        f.write(f"Analyzed file: {log_file}\n")
        f.write(f"Generated on: {datetime.datetime.now()}\n")
        f.write("==========================================\n\n")
        
        f.write("=== SUMMARY ===\n")
        f.write(f"Total log entries: {report_data['total_entries']}\n\n")
        
        f.write("=== ENTRY TYPES ===\n")
        f.write(f"Info entries: {report_data['info_count']}\n")
        f.write(f"Error entries: {report_data['error_count']}\n\n")
        
        f.write("=== RECENT ACTIVITIES (Last 5) ===\n")
        for entry in report_data['recent_entries']:
            f.write(entry)
        
        if report_data['error_count'] > 0:
            f.write("\n=== ERROR DETAILS ===\n")
            for error in report_data['error_entries']:
                f.write(error + '\n')
        
        if report_data['cpu_usage_samples']:
            f.write("\n=== CPU USAGE SAMPLES ===\n")
            for sample in report_data['cpu_usage_samples'][-3:]:
                f.write(sample + '\n')
    
    print(f"Analysis complete! Report saved to: {report_file}")
    
    # Display quick summary
    print("\n=== QUICK SUMMARY ===")
    print(f"Total entries: {report_data['total_entries']}")
    print(f"Info entries: {report_data['info_count']}")
    print(f"Error entries: {report_data['error_count']}")

if __name__ == "__main__":
    log_file = sys.argv[1] if len(sys.argv) > 1 else "system_health.log"
    analyze_logs(log_file)
