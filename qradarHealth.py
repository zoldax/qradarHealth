import qradarzoldaxlib

# Ensure config is read
config = qradarzoldaxlib.read_config()

def get_qradar_metrics():
    """
    Fetch and display metrics from the QRadar API endpoint '/health/metrics/qradar_metrics'.
    """
    # Construct the URL for the QRadar metrics API endpoint
    base_url = f"https://{config['ip_QRadar']}"
    endpoint = "/health/metrics/qradar_metrics"
    url = f"{base_url}{endpoint}"
    
    # Fetch the metrics data
    metrics_data = qradarzoldaxlib.make_request(url)
    
    # Check if the request was successful
    if not metrics_data:
        print("Failed to fetch QRadar metrics.")
        return
    
    # Display the fetched metrics data
    print("QRadar Metrics Data:")
    for metric in metrics_data:
        print(f"{metric}: {metrics_data[metric]}")

if __name__ == "__main__":
    get_qradar_metrics()

