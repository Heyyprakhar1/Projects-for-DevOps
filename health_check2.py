#!/usr/bin/env python3

import subprocess
import datetime
import os
import sys

# Configuration
LOG_FILE = "system_health.log"
ERROR_LOG = "system_health_errors.log"

def log_message(message):
    """Log messages to file"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(LOG_FILE, 'a') as f:
        f.write(f"{timestamp} - {message}\n")

def log_error(message):
    """Log errors to file"""
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(ERROR_LOG, 'a') as f:
        f.write(f"{timestamp} - ERROR: {message}\n")
    print(f"ERROR: {message}", file=sys.stderr)

def run_command(cmd):
    """Execute a shell command and return the output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        log_error(f"Command failed: {cmd} - {e}")
        return None

def print_section(title):
    """Print a section header"""
    print(f"\n=== {title} ===")

def main():
    # Header
    print("=" * 50)
    print("     SYSTEM HEALTH CHECK REPORT (PYTHON)")
    print("=" * 50)
    print(f"Generated on: {datetime.datetime.now()}")
    print(f"Hostname: {run_command('hostname') or 'Unknown'}")
    print(f"Log File: {LOG_FILE}")
    print("=" * 50)
    
    log_message("Starting system health check")
    
    # CPU Information
    print_section("CPU USAGE")
    cpu_info = run_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d'%' -f1")
    if cpu_info:
        print(f"CPU Usage: {cpu_info}%")
        log_message(f"CPU Usage: {cpu_info}%")
    else:
        print("CPU Usage: Unable to determine")
    
    # Memory Information
    print_section("MEMORY USAGE")
    memory_info = run_command("free -h | grep Mem")
    if memory_info:
        parts = memory_info.split()
        total_mem = parts[1]
        used_mem = parts[2]
        print(f"Used Memory: {used_mem} / {total_mem}")
        log_message("Memory check completed")
    else:
        print("Memory Info: Unable to determine")
    
    # Disk Information
    print_section("DISK USAGE")
    disk_info = run_command("df -h | grep -v tmpfs")
    if disk_info:
        print(disk_info)
        log_message("Disk check completed")
    else:
        print("Disk Info: Unable to determine")
    
    # System Uptime
    print_section("SYSTEM UPTIME")
    uptime_info = run_command("uptime -p")
    boot_time = run_command("uptime -s")
    if uptime_info and boot_time:
        print(f"Uptime: {uptime_info}")
        print(f"System booted: {boot_time}")
        log_message(f"System uptime: {uptime_info}")
    else:
        print("Uptime: Unable to determine")
    
    print("\n" + "=" * 50)
    print("         END OF REPORT")
    print("=" * 50)
    
    log_message("System health check completed successfully")
    print(f"Report saved to: {LOG_FILE}")
    print(f"Errors logged to: {ERROR_LOG}")

if __name__ == "__main__":
    main()
