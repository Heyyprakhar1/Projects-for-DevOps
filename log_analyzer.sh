#!/bin/bash

# Configuration
LOG_FILE="${1:-system_health.log}"
REPORT_FILE="log_analysis_report.txt"

# Function to analyze log file
analyze_logs() {
    echo "==========================================" > "$REPORT_FILE"
    echo "     LOG ANALYSIS REPORT" >> "$REPORT_FILE"
    echo "==========================================" >> "$REPORT_FILE"
    echo "Analyzed file: $LOG_FILE" >> "$REPORT_FILE"
    echo "Generated on: $(date)" >> "$REPORT_FILE"
    echo "==========================================" >> "$REPORT_FILE"
    
    # Total log entries
    total_entries=$(grep -c "" "$LOG_FILE")
    echo "" >> "$REPORT_FILE"
    echo "=== SUMMARY ===" >> "$REPORT_FILE"
    echo "Total log entries: $total_entries" >> "$REPORT_FILE"
    
    # Count by type
    echo "" >> "$REPORT_FILE"
    echo "=== ENTRY TYPES ===" >> "$REPORT_FILE"
    info_count=$(grep -c "Starting system health check\|check completed\|completed successfully" "$LOG_FILE")
    error_count=$(grep -c "ERROR" "$LOG_FILE")
    echo "Info entries: $info_count" >> "$REPORT_FILE"
    echo "Error entries: $error_count" >> "$REPORT_FILE"
    
    # Recent activities
    echo "" >> "$REPORT_FILE"
    echo "=== RECENT ACTIVITIES (Last 5) ===" >> "$REPORT_FILE"
    tail -5 "$LOG_FILE" >> "$REPORT_FILE"
    
    # Error details (if any)
    if [ $error_count -gt 0 ]; then
        echo "" >> "$REPORT_FILE"
        echo "=== ERROR DETAILS ===" >> "$REPORT_FILE"
        grep "ERROR" "$LOG_FILE" >> "$REPORT_FILE"
    fi
    
    # CPU Usage trends (simplified)
    echo "" >> "$REPORT_FILE"
    echo "=== CPU USAGE SAMPLES ===" >> "$REPORT_FILE"
    grep "CPU Usage" "$LOG_FILE" | tail -3 >> "$REPORT_FILE"
}

# Main execution
if [ ! -f "$LOG_FILE" ]; then
    echo "Error: Log file '$LOG_FILE' not found!"
    echo "Please run the health checker first to generate logs."
    exit 1
fi

echo "Analyzing log file: $LOG_FILE"
analyze_logs
echo "Analysis complete! Report saved to: $REPORT_FILE"

# Display summary
echo ""
echo "=== QUICK SUMMARY ==="
echo "Total entries: $(grep -c "" "$LOG_FILE")"
echo "Info entries: $(grep -c "Starting system health check\|check completed\|completed successfully" "$LOG_FILE")"
echo "Error entries: $(grep -c "ERROR" "$LOG_FILE")"
