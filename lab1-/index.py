import re
import json
import csv
from collections import defaultdict

# Regex for log file parsing
LOG_PATTERN = r'(?P<ip>\d+\.\d+\.\d+\.\d+) - - \[(?P<date>.*?)\] \"(?P<method>\w+).*?" (?P<status>\d+)'  

# File paths
LOG_FILE = "server_logs.txt"
FAILED_LOGINS_JSON = "failed_logins.json"
THREAT_IPS_JSON = "threat_ips.json"
COMBINED_SECURITY_JSON = "combined_security_data.json"
LOG_ANALYSIS_TXT = "log_analysis.txt"
LOG_ANALYSIS_CSV = "log_analysis.csv"

# Load threat intelligence data (sample data)
threat_ips = ["192.168.1.10", "203.0.113.1"]  # Sample threat IPs

def parse_logs(log_file):
    """Parses log file and extracts required fields."""
    log_data = []
    with open(log_file, "r") as file:
        for line in file:
            match = re.search(LOG_PATTERN, line)
            if match:
                log_data.append(match.groupdict())
    return log_data

def analyze_failed_logins(log_data):
    """Analyzes failed logins and extracts IPs with more than 5 failures."""
    failed_attempts = defaultdict(int)
    for entry in log_data:
        if entry["status"] == "401":  # Assuming 401 is the failed login status
            failed_attempts[entry["ip"]] += 1
    return {ip: count for ip, count in failed_attempts.items() if count > 5}

def save_to_json(data, filename):
    """Saves data to a JSON file."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def save_to_txt(failed_attempts, filename):
    """Saves failed login attempts to a text file."""
    with open(filename, "w") as file:
        for ip, count in failed_attempts.items():
            file.write(f"{ip}: {count} failed attempts\n")

def save_to_csv(log_data, filename):
    """Saves log data to a CSV file."""
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["IP Address", "Date", "HTTP Method", "Failed Attempts"])
        for entry in log_data:
            writer.writerow([entry["ip"], entry["date"], entry["method"], entry.get("failures", "")])

def combine_security_data(failed_attempts, threat_ips, output_file):
    """Combines failed attempts and threat IPs into a single JSON."""
    combined_data = {
        "failed_logins": failed_attempts,
        "threat_ips": threat_ips,
    }
    save_to_json(combined_data, output_file)

def main():
    # Parse log file
    log_data = parse_logs(LOG_FILE)

    # Analyze failed logins
    failed_attempts = analyze_failed_logins(log_data)

    # Save failed logins to JSON
    save_to_json(failed_attempts, FAILED_LOGINS_JSON)

    # Save failed logins to TXT
    save_to_txt(failed_attempts, LOG_ANALYSIS_TXT)

    # Add failures to log data for CSV output
    for entry in log_data:
        entry["failures"] = failed_attempts.get(entry["ip"], 0)

    # Save log data to CSV
    save_to_csv(log_data, LOG_ANALYSIS_CSV)

    # Save threat IPs to JSON
    save_to_json(threat_ips, THREAT_IPS_JSON)

    # Combine security data
    combine_security_data(failed_attempts, threat_ips, COMBINED_SECURITY_JSON)

if __name__ == "__main__":
    main()

