#!/usr/bin/env python3

import subprocess
import datetime
import os

def run_command(cmd):
    """Execute a shell command and return the output"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return f"Error: {e}"

def print_section(title):
    """Print a section header"""
    print(f"\n=== {title} ===")

def main():
    # Header
    print("=" * 50)
    print("     SYSTEM HEALTH CHECK REPORT (PYTHON)")
    print("=" * 50)
    print(f"Generated on: {datetime.datetime.now()}")
    print(f"Hostname: {run_command('hostname')}")
    print("=" * 50)
    
    # CPU Information
    print_section("CPU USAGE")
    cpu_info = run_command("top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d'%' -f1")
    print(f"CPU Usage: {cpu_info}%")
    
    load_avg = run_command("uptime | awk -F'load average:' '{print $2}'")
    print(f"Load Average: {load_avg}")
    
    # Memory Information
    print_section("MEMORY USAGE")
    memory_info = run_command("free -h | grep Mem")
    if memory_info and not memory_info.startswith("Error"):
        parts = memory_info.split()
        total_mem = parts[1]
        used_mem = parts[2]
        print(f"Used Memory: {used_mem} / {total_mem}")
    
    # Disk Information
    print_section("DISK USAGE")
    disk_info = run_command("df -h | grep -v tmpfs")
    print(disk_info)
    
    # Top Processes by CPU
    print_section("TOP PROCESSES BY CPU")
    top_processes = run_command("ps aux --sort=-%cpu | head -6")
    print(top_processes)
    
    # System Uptime
    print_section("SYSTEM UPTIME")
    uptime_info = run_command("uptime -p")
    boot_time = run_command("uptime -s")
    print(f"Uptime: {uptime_info}")
    print(f"System booted: {boot_time}")
    
    print("\n" + "=" * 50)
    print("         END OF REPORT")
    print("=" * 50)

if __name__ == "__main__":
    main()
