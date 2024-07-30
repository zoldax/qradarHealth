#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import qradarzoldaxlib
import requests
import logging
import argparse

# Set up logging
LOG_FILENAME = 'error.log'

def setup_logging(debug=False):
    """
    Set up logging configuration.
    :param debug: Boolean indicating whether to enable debug level logging.
    """
    log_level = logging.DEBUG if debug else logging.ERROR
    logging.basicConfig(filename=LOG_FILENAME, level=log_level,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    return logger

def get_qradar_metrics(logger):
    """
    Fetch and display metrics from the QRadar API endpoint '/api/health/metrics/qradar_metrics'.
    :param logger: Logger instance for logging information.
    """
    # Ensure config is read
    config = qradarzoldaxlib.read_config()

    # Construct the URL for the QRadar metrics API endpoint
    base_url = f"https://{config.get('ip_QRadar', '')}"
    endpoint = "/api/health/metrics/qradar_metrics"
    url = f"{base_url}{endpoint}"

    try:
        headers = qradarzoldaxlib.get_qradar_headers()
        response = requests.get(url, headers=headers, verify=qradarzoldaxlib.get_verify_option())

        logger.debug(f"Status Code: {response.status_code}")
        logger.debug(f"Response Headers: {response.headers}")

        if response.status_code == 200:
            try:
                metrics_data = response.json()

                if not metrics_data:
                    logger.error("No data received.")
                    return

                # Display the fetched metrics data
                print("QRadar Metrics Data:")
                for metric in metrics_data:
                    component_type = metric.get('component_type', 'N/A')
                    metric_id = metric.get('metric_id', 'N/A')
                    time_resolution = metric.get('time_resolution', 'N/A')
                    component_name = metric.get('component_name', 'N/A')
                    enabled = metric.get('enabled', 'N/A')
                    print(f"Component Type: {component_type}, Metric ID: {metric_id}, "
                          f"Time Resolution: {time_resolution}, Component Name: {component_name}, Enabled: {enabled}")
            except ValueError as e:
                logger.error(f"Error parsing JSON response: {e}")
        else:
            logger.error(f"Error: Received non-200 status code {response.status_code}")
            logger.debug(f"Response Content: {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Request failed: {e}")

if __name__ == "__main__":
    # Argument parser for command-line options
    parser = argparse.ArgumentParser(description="Fetch QRadar metrics data.")
    parser.add_argument('--debug', action='store_true', help="Enable debug logging")
    args = parser.parse_args()

    # Set up logging based on the debug parameter
    logger = setup_logging(debug=args.debug)

    # Fetch and display QRadar metrics
    get_qradar_metrics(logger)

