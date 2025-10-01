"""
dataset_module.py

This module handles loading and preprocessing the stroke dataset.
It reads the data from a CSV file, cleans it, and converts values to appropriate data types.
"""


def _convert_to_appropriate_type(value_str):
    """
    Helper function to convert a string value to its correct data type:
    - Returns None for missing or 'N/A' values.
    - Preserves 'Unknown' as a string.
    - Attempts to convert to int, then float; otherwise returns as string.
    """
    value_str = value_str.strip()

    if value_str in ('N/A', ''):
        return None
    if value_str == 'Unknown':
        return 'Unknown'

    try:
        return int(value_str)
    except ValueError:
        try:
            return float(value_str)
        except ValueError:
            return value_str


def load_data(filepath):
    """
    Loads and parses the stroke dataset from a CSV file.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        tuple:
            - data (list of dict): List of records with properly typed values.
            - header (list of str): List of column names.

    Raises:
        FileNotFoundError: If the file does not exist.
        Exception: For any other errors during file reading or parsing.
    """
    data = []
    header = []

    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            # Read the first line to get column headers
            header_line = file.readline()
            if not header_line:
                return [], []

            header = [h.strip() for h in header_line.strip().split(',')]
            expected_columns = len(header)

            # Read and process each subsequent line
            for line in file:
                if not line.strip():
                    continue  # Skip empty lines

                values = [v.strip() for v in line.strip().split(',')]

                if len(values) == expected_columns:
                    record = {
                        header[i]: _convert_to_appropriate_type(values[i])
                        for i in range(expected_columns)
                    }
                    data.append(record)

    except FileNotFoundError:
        raise FileNotFoundError(f"Dataset file not found at: {filepath}")
    except Exception as e:
        raise Exception(f"An error occurred while reading the dataset: {e}")

    return data, header

