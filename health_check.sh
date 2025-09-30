#!/bin/bash

# Configuration
LOG_FILE="system_health.log"
ERROR_LOG="system_health_errors.log"

# Function to log messages
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Function to log errors
log_error() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ERROR: $1" >> "$ERROR_LOG"
    echo "ERROR: $1" >&2
}

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
echo "Log File: $LOG_FILE"
echo "=========================================="

# Log the start of health check
log_message "Starting system health check"

# CPU Information
print_section "CPU USAGE"
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk '{print 100 - $1}')
if [ -n "$CPU_USAGE" ]; then
    echo "CPU Usage: ${CPU_USAGE}%"
    log_message "CPU Usage: ${CPU_USAGE}%"
else
    log_error "Failed to get CPU usage"
    echo "CPU Usage: Unable to determine"
fi

# Memory Information
print_section "MEMORY USAGE"
MEMORY_INFO=$(free -h 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "$MEMORY_INFO" | awk '
    NR==1{print}
    NR==2{print "Used Memory: " $3 " / " $2 " (" $3/$2*100 "%)"}
    '
    log_message "Memory check completed"
else
    log_error "Failed to get memory information"
    echo "Memory Info: Unable to determine"
fi

# Disk Information
print_section "DISK USAGE"
DISK_INFO=$(df -h 2>/dev/null | grep -v tmpfs)
if [ $? -eq 0 ]; then
    echo "$DISK_INFO"
    log_message "Disk check completed"
else
    log_error "Failed to get disk information"
    echo "Disk Info: Unable to determine"
fi

# System Uptime
print_section "SYSTEM UPTIME"
UPTIME_INFO=$(uptime 2>/dev/null)
if [ $? -eq 0 ]; then
    echo "$UPTIME_INFO"
    log_message "System uptime: $(uptime -p)"
else
    log_error "Failed to get uptime information"
    echo "Uptime: Unable to determine"
fi

echo ""
echo "=========================================="
echo "         END OF REPORT"
echo "=========================================="

log_message "System health check completed successfully"
echo "Report saved to: $LOG_FILE"
echo "Errors logged to: $ERROR_LOG"
