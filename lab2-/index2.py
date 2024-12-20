import re
import csv
import json
from collections import defaultdict

# File paths
ACCESS_LOG_FILE = "access_log.txt"
THREAT_FEED_FILE = "threat_feed.txt"  # Updated to use plain text for threat feed
URL_STATUS_REPORT = "url_status_report.txt"
MALWARE_CANDIDATES_CSV = "malware_candidates.csv"
ALERT_JSON = "alert.json"
SUMMARY_REPORT_JSON = "summary_report.json"
THREAT_IPS_JSON = "threat_ips.json"  # New file for threat IPs
COMBINED_SECURITY_DATA_JSON = "combined_security_data.json"  # New file for combined data

# Regex for log file parsing
LOG_PATTERN = r'"(?:GET|POST|PUT|DELETE|HEAD) (?P<url>[^ ]+) HTTP/1.1" (?P<status>\d+)'  

# Functions
def parse_access_logs(log_file):
    """Parses access logs and extracts URLs and status codes."""
    log_data = []
    with open(log_file, "r") as file:
        for line in file:
            match = re.search(LOG_PATTERN, line)
            if match:
                log_data.append(match.groupdict())
    return log_data

def analyze_404_urls(log_data):
    """Identifies URLs with 404 status and counts occurrences."""
    url_404_counts = defaultdict(int)
    for entry in log_data:
        if entry["status"] == "404":
            url_404_counts[entry["url"]] += 1
    return url_404_counts

def load_blacklist_domains(file_path):
    """Loads blacklist domains from a plain text file."""
    with open(file_path, "r") as file:
        return [line.strip() for line in file if line.strip()]

def match_blacklist_urls(log_data, blacklist_domains):
    """Matches log URLs against blacklist domains."""
    alerts = []
    for entry in log_data:
        for domain in blacklist_domains:
            if domain in entry["url"]:
                alerts.append({"url": entry["url"], "status": entry["status"]})
    return alerts

def save_to_txt(log_data, filename):
    """Saves URL and status codes to a text file."""
    with open(filename, "w") as file:
        for entry in log_data:
            file.write(f"{entry['url']}: {entry['status']}\n")

def save_to_csv(data, filename):
    """Saves URL and 404 counts to a CSV file."""
    with open(filename, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "404 Count"])
        for url, count in data.items():
            writer.writerow([url, count])

def save_to_json(data, filename):
    """Saves data to a JSON file."""
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def create_summary_report(log_data, url_404_counts, alerts, filename):
    """Creates a summary report and saves to JSON."""
    summary = {
        "total_requests": len(log_data),
        "total_404_urls": len(url_404_counts),
        "total_alerts": len(alerts),
    }
    save_to_json(summary, filename)

def generate_combined_data(alerts, blacklist_domains, filename):
    """Combines alerts and blacklist data and saves to JSON."""
    combined_data = {
        "alerts": alerts,
        "blacklist_domains": blacklist_domains
    }
    save_to_json(combined_data, filename)

def main():
    # Parse access logs
    log_data = parse_access_logs(ACCESS_LOG_FILE)

    # Analyze 404 URLs
    url_404_counts = analyze_404_urls(log_data)

    # Save URL and status codes to TXT
    save_to_txt(log_data, URL_STATUS_REPORT)

    # Save 404 URL counts to CSV
    save_to_csv(url_404_counts, MALWARE_CANDIDATES_CSV)

    # Load blacklist domains
    blacklist_domains = load_blacklist_domains(THREAT_FEED_FILE)

    # Match URLs against blacklist
    alerts = match_blacklist_urls(log_data, blacklist_domains)

    # Save alerts to JSON
    save_to_json(alerts, ALERT_JSON)

    # Save threat IPs to JSON (dummy implementation for now)
    threat_ips = {"ips": [entry["url"] for entry in alerts]}
    save_to_json(threat_ips, THREAT_IPS_JSON)

    # Generate and save combined security data
    generate_combined_data(alerts, blacklist_domains, COMBINED_SECURITY_DATA_JSON)

    # Create and save summary report
    create_summary_report(log_data, url_404_counts, alerts, SUMMARY_REPORT_JSON)

if __name__ == "__main__":
    main()
