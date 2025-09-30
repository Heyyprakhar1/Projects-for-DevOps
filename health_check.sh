#!/bin/bash

# Function to print section headers
print_section() {
    echo ""
    echo "=== $1 ==="
}

# Header
echo "=========================================="
echo "     SYSTEM HEALTH CHECK REPORT (BASH)"
echo "=========================================="
echo "Generated on: $(date)"
echo "Hostname: $(hostname)"
echo "=========================================="

# CPU Information
print_section "CPU USAGE"
echo "CPU Load:"
top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print "CPU Usage: " 100 - $1 "%"}'
echo "Load Average: $(uptime | awk -F'load average:' '{print $2}')"

# Memory Information
print_section "MEMORY USAGE"
free -h | awk '
NR==1{print}
NR==2{print "Used Memory: " $3 " / " $2 " (" $3/$2*100 "%)"}
'

# Disk Information
print_section "DISK USAGE"
df -h | grep -v tmpfs | awk '
NR==1{print}
NR>1{print $1 " - " $5 " used (" $3 " / " $2 ") - Mount: " $6}
'

# Top Processes by CPU
print_section "TOP PROCESSES BY CPU"
ps aux --sort=-%cpu | head -6 | awk '
NR==1{printf "%-8s %-8s %s\n", "USER", "CPU%", "COMMAND"}
NR>1{printf "%-8s %-8s %s\n", $1, $3, $11}
'

# System Uptime
print_section "SYSTEM UPTIME"
uptime -p
echo "System booted: $(uptime -s)"

echo ""
echo "=========================================="
echo "         END OF REPORT"
echo "=========================================="
