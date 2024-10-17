# QRadar Metrics Fetcher

This Python script fetches and displays metrics from the QRadar API endpoint `/api/health/metrics/qradar_metrics`. It connects to a QRadar instance, retrieves health metrics, and optionally filters them based on a provided MBean name.
This script is a draft designed to retrieve additional metric information via the API for monitoring purposes, complementing the data available through SNMP

## Features

- **Fetch QRadar Metrics**: Retrieve and display health metrics from a QRadar instance via its API.
- **Logging Support**: Logs errors and debugging information to a file for troubleshooting.
- **Optional MBean Filtering**: Filter metrics by providing a specific MBean name.
- **Command-line Options**: Enable debug mode and MBean filtering with easy-to-use command-line arguments.

## Requirements

- Python 3.x
- `qradarzoldaxlib` (a custom library for QRadar integration)
- `requests` library

To install the `requests` library, run:

```
pip install requests
```

## Setup

Before running the script, make sure that:
1. You have the `qradarzoldaxlib` library installed and properly configured with your QRadar system's IP address and authentication details.
2. The script can access your QRadar instance via the API.

## Usage

The script can be executed directly from the command line with the following options:

### Basic Usage

```
python qradar_metrics_fetcher.py
```

### Enable Debug Logging

To enable debug logging, which provides detailed information about the script's execution:

```
python qradar_metrics_fetcher.py --debug
```

### Filter Metrics by MBean Name

To filter the metrics by a specific MBean name, use the `--querymbean` option:

```
python qradar_metrics_fetcher.py --querymbean <MBean_name>
```

### Combined Usage

You can combine the `--debug` and `--querymbean` options:

```
python qradar_metrics_fetcher.py --debug --querymbean <MBean_name>
```

## Command-line Arguments

- `--debug`: Enables debug-level logging to assist in troubleshooting.
- `--querymbean <MBean_name>`: Filters the fetched metrics by the specified MBean name.

## Logging

Logs are stored in the `error.log` file in the script's directory. Depending on the logging level, the log file will contain detailed debug information or only error messages.

## Example Output

After running the script, you'll see the QRadar metrics data printed in the terminal, similar to the following:

```
QRadar Metrics Data:
Component Type: example_type, Metric ID: example_id, Time Resolution: 5min, Component Name: example_name, Enabled: true
Component Type: example_type, Metric ID: another_id, Time Resolution: 5min, Component Name: another_name, Enabled: false
```

## Error Handling

The script handles various types of errors, including:
- Failed API requests
- JSON parsing issues
- Missing or invalid QRadar configuration

All errors are logged to `error.log`.

## License

This project is licensed under the Apache2 License. See the [LICENSE](LICENSE) file for details.

## Contributions

Feel free to contribute to this project by submitting issues or pull requests. All contributions are welcome!

## Author

[Your Name](https://github.com/your-github-username)

``````

This version of the README.md file uses ````` instead of the usual code block syntax.

