#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
QRadar Metrics Fetcher (QRadarHealth)

 Copyright 2024 Pascal Weber (zoldax) / Abakus Sécurité

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.

This script retrieves and displays metrics from the QRadar API endpoint
'/api/health/metrics/qradar_metrics'. It is designed to connect to the QRadar
system, query its health metrics, and optionally filter these metrics based on
a provided MBean name.
This script is a draft designed to retrieve additional metric information via the API for monitoring purposes, complementing the data available through SNMP.

Purpose:
---------
The script:
1. Reads QRadar configuration and authentication details from a custom library.
2. Fetches QRadar health metrics using the API.
3. Filters and displays the metrics, logging any errors or warnings.
4. Allows optional filtering of metrics based on an MBean name query.

Usage:
---------
This script can be run from the command line with optional arguments:
- `--debug`: Enables debug-level logging, which provides detailed output for troubleshooting.
- `--querymbean <MBean name>`: Filters the metrics based on a specified MBean name.

Inputs:
---------
1. **Command-line arguments:**
   - `--debug`: (optional) Enables detailed logging.
   - `--querymbean <MBean name>`: (optional) Filters metrics by MBean name.

2. **Configuration:**
   - The QRadar IP address and authentication headers are retrieved from the `qradarzoldaxlib` library.

Outputs:
---------
1. **Printed Output:**
   - Displays the fetched QRadar metrics, including:
     - `Component Type`
     - `Metric ID`
     - `Time Resolution`
     - `Component Name`
     - `Enabled` status
   - Filters results if a specific MBean query is provided.

2. **Log File:**
   - Writes logs (errors, warnings, and debug information) to the file `error.log`,
     including API responses, status codes, and any issues encountered during execution.

"""

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

def get_qradar_metrics(logger, mbean_query=None):
    """
    Fetch and display metrics from the QRadar API endpoint '/api/health/metrics/qradar_metrics'.
    :param logger: Logger instance for logging information.
    :param mbean_query: Optional string to filter metrics by MBean name.
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

                    # Filter by MBean name if query is specified and metric_id is not None
                    if mbean_query and metric_id and mbean_query not in metric_id:
                        continue

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
    parser.add_argument('--querymbean', type=str, help="Filter metrics by MBean name")
    args = parser.parse_args()

    # Set up logging based on the debug parameter
    logger = setup_logging(debug=args.debug)

    # Fetch and display QRadar metrics
    get_qradar_metrics(logger, mbean_query=args.querymbean)

