"""
Module for querying the loaded stroke dataset.
Provides statistical analysis functions based on assignment requirements,
using header names from the provided preview.
"""

import math
import os
from collections import Counter


# --- Helper Functions ---

def _filter_data(data, conditions):
    """Filter dataset records based on given conditions."""
    if not conditions:
        return data
    filtered = []
    for record in data:
        if all(record.get(key) == value for key, value in conditions.items()):
            filtered.append(record)
    return filtered


def _get_numeric_values(data, feature, conditions=None):
    """Extract numeric values for a feature, optionally filtered."""
    values = []
    for record in _filter_data(data, conditions) if conditions else data:
        value = record.get(feature)
        if isinstance(value, (int, float)):
            values.append(value)
    return values


def _calculate_mean(numbers):
    """Calculate mean of a list of numbers."""
    return round(sum(numbers) / len(numbers), 2) if numbers else None


def _calculate_median(numbers):
    """Calculate median of a list of numbers."""
    if not numbers:
        return None
    numbers = sorted(numbers)
    mid = len(numbers) // 2
    return round((numbers[mid - 1] + numbers[mid]) / 2, 2) if len(numbers) % 2 == 0 else round(numbers[mid], 2)


def _calculate_mode(items):
    """Calculate mode(s) of a list."""
    valid_items = [item for item in items if item is not None]
    if not valid_items:
        return []
    counts = Counter(valid_items)
    max_count = max(counts.values())
    return sorted([item for item, count in counts.items() if count == max_count])


def _calculate_std_dev(numbers, mean_val=None):
    """Calculate sample standard deviation."""
    if not numbers or len(numbers) < 2:
        return None
    mean_val = mean_val if mean_val is not None else _calculate_mean(numbers)
    variance = sum((x - mean_val) ** 2 for x in numbers) / (len(numbers) - 1)
    return round(math.sqrt(variance), 2)


def _calculate_percentile(numbers, percentile):
    """Calculate a specific percentile."""
    if not numbers or not (0 <= percentile <= 100):
        return None
    numbers = sorted(numbers)
    k = (len(numbers) - 1) * (percentile / 100)
    f, c = math.floor(k), math.ceil(k)
    return round(numbers[int(k)], 2) if f == c else round(numbers[f] * (c - k) + numbers[c] * (k - f), 2)


def _format_csv_value(value):
    """Format a value for CSV output."""
    if value is None:
        return ''
    value_str = str(value)
    if any(c in value_str for c in ',\"\n'):
        return f'"{value_str.replace("\"", "\"\"")}"'
    return value_str


def save_results_csv(data_to_save, filename, headers=None):
    """Save data to a CSV file."""
    if not filename.lower().endswith('.csv'):
        filename += '.csv'
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            if isinstance(data_to_save, dict):
                f.write("Metric,Value\n")
                for key, value in data_to_save.items():
                    if isinstance(value, (dict, list)):
                        value = ', '.join(f"{k}: {v}" for k, v in value.items()) if isinstance(value, dict) else str(value)
                    f.write(f"{_format_csv_value(key)},{_format_csv_value(value)}\n")
            elif isinstance(data_to_save, list) and data_to_save:
                if headers is None:
                    if isinstance(data_to_save[0], dict):
                        headers = list(data_to_save[0].keys())
                    else:
                        raise ValueError("Headers must be provided for non-dict data.")
                f.write(','.join(_format_csv_value(h) for h in headers) + '\n')
                for row in data_to_save:
                    row_values = [_format_csv_value(row.get(header) if isinstance(row, dict) else row[i]) for i, header in enumerate(headers)]
                    f.write(','.join(row_values) + '\n')
            else:
                f.write(str(data_to_save) + '\n')
        print(f"Results successfully saved to {os.path.abspath(filename)}")
    except Exception as e:
        print(f"Error saving file {filename}: {e}")


# --- Query Functions (i - xi) ---

def query_smokers_hypertension_stroke(data):
    """i. Age statistics for smokers with hypertension who had a stroke."""
    smoking_statuses = ['Formerly smoked', 'smokes']
    ages = []
    for status in smoking_statuses:
        ages.extend(_get_numeric_values(data, 'Age', {'Hypertension': 1, 'Stroke Occurrence': 1, 'Smoking Status': status}))
    if not ages:
        result = {"message": "No data found for smokers with hypertension who had a stroke"}
    else:
        result = {
            'description': "Smokers with hypertension who had a stroke",
            'count': len(ages),
            'average_age': _calculate_mean(ages),
            'median_age': _calculate_median(ages),
            'modal_age': _calculate_mode(ages)
        }
    save_results_csv(result, "smokers_hypertension_stroke.csv")
    return result


def query_heart_disease_stroke(data):
    """ii. Age and glucose statistics for patients with heart disease who had a stroke."""
    conditions = {'Heart Disease': 1, 'Stroke Occurrence': 1}
    ages = _get_numeric_values(data, 'Age', conditions)
    glucose_levels = _get_numeric_values(data, 'Average Glucose Level', conditions)
    if not ages:
        result = {"message": "No data found for patients with heart disease who had a stroke"}
    else:
        result = {
            'description': "Heart disease patients who had a stroke",
            'count': len(ages),
            'average_age': _calculate_mean(ages),
            'median_age': _calculate_median(ages),
            'modal_age': _calculate_mode(ages),
            'average_glucose_level': _calculate_mean(glucose_levels)
        }
    save_results_csv(result, "heart_disease_stroke_stats.csv")
    return result


def query_hypertension_gender_stroke(data):
    """iii. Age stats by gender for hypertension+stroke vs hypertension+no stroke."""
    genders = {r.get('Gender') for r in data if r.get('Gender') and r.get('Gender') != 'Other'}
    results = {}
    for gender in genders:
        for stroke_status, label in [(1, 'Stroke'), (0, 'NoStroke')]:
            conditions = {'Hypertension': 1, 'Stroke Occurrence': stroke_status, 'Gender': gender}
            ages = _get_numeric_values(data, 'Age', conditions)
            key = f"{gender}_Hypertension_{label}"
            results[key] = {
                'count': len(ages),
                'average_age': _calculate_mean(ages),
                'median_age': _calculate_median(ages),
                'modal_age': _calculate_mode(ages)
            } if ages else {'count': 0, 'message': 'No data'}
    save_results_csv(results, "hypertension_gender_stroke.csv")
    return results


def query_smoking_stroke(data):
    """iv. Age stats for smoking habit -> stroke vs no stroke."""
    smoking_statuses = {r.get('Smoking Status') for r in data if r.get('Smoking Status')}
    results = {}
    for status in smoking_statuses:
        for stroke_status, label in [(1, 'Stroke'), (0, 'NoStroke')]:
            conditions = {'Smoking Status': status, 'Stroke Occurrence': stroke_status}
            ages = _get_numeric_values(data, 'Age', conditions)
            key = f"{status}_{label}"
            results[key] = {
                'count': len(ages),
                'average_age': _calculate_mean(ages),
                'median_age': _calculate_median(ages),
                'modal_age': _calculate_mode(ages)
            } if ages else {'count': 0, 'message': 'No data'}
    save_results_csv(results, "smoking_stroke.csv")
    return results


def query_residence_stroke(data):
    """v. Age stats for Urban vs Rural stroke patients."""
    results = {}
    for residence in ['Urban', 'Rural']:
        ages = _get_numeric_values(data, 'Age', {'Residence Type': residence, 'Stroke Occurrence': 1})
        results[residence] = {
            'description': f"{residence} residents with stroke",
            'count': len(ages),
            'average_age': _calculate_mean(ages),
            'median_age': _calculate_median(ages),
            'modal_age': _calculate_mode(ages)
        } if ages else {'count': 0, 'message': f'No data for {residence}'}
    save_results_csv(results, "residence_stroke.csv")
    return results


def query_dietary_habits_stroke(data):
    """vi. Dietary habits distribution (stroke vs no stroke)."""
    habits_stroke = [r.get('Dietary Habits') for r in _filter_data(data, {'Stroke Occurrence': 1}) if r.get('Dietary Habits')]
    habits_no_stroke = [r.get('Dietary Habits') for r in _filter_data(data, {'Stroke Occurrence': 0}) if r.get('Dietary Habits')]
    result = {
        'description': "Dietary habits distribution",
        'stroke': dict(Counter(habits_stroke)),
        'no_stroke': dict(Counter(habits_no_stroke))
    }
    save_results_csv(result, "dietary_habits_stroke.csv")
    return result


def query_hypertension_stroke_patients(data):
    """vii. Patients whose hypertension resulted in stroke."""
    patients = _filter_data(data, {'Hypertension': 1, 'Stroke Occurrence': 1})
    save_results_csv(patients, "hypertension_stroke_patients.csv")
    return patients


def query_hypertension_stroke_comparison(data):
    """viii. Patients with hypertension who had vs didn't have a stroke."""
    stroke_patients = _filter_data(data, {'Hypertension': 1, 'Stroke Occurrence': 1})
    no_stroke_patients = _filter_data(data, {'Hypertension': 1, 'Stroke Occurrence': 0})
    combined = [{**p, 'Group': 'Stroke'} for p in stroke_patients] + [{**p, 'Group': 'No Stroke'} for p in no_stroke_patients]
    save_results_csv(combined, "hypertension_stroke_comparison.csv")
    return {'hypertension_led_to_stroke': stroke_patients, 'hypertension_did_not_lead_to_stroke': no_stroke_patients}


def query_heart_disease_stroke_patients(data):
    """ix. Patients with heart disease who had a stroke."""
    patients = _filter_data(data, {'Heart Disease': 1, 'Stroke Occurrence': 1})
    save_results_csv(patients, "heart_disease_stroke_patients.csv")
    return patients


def query_descriptive_statistics(data, feature_name, header):
    """x. Descriptive stats for a given numeric feature."""
    if feature_name not in header:
        return f"Error: Feature '{feature_name}' not found."
    numbers = _get_numeric_values(data, feature_name)
    if not numbers:
        result = f"Error: No valid numeric data for '{feature_name}'."
        save_results_csv(result, f"descriptive_stats_{feature_name}.csv")
        return result
    result = {
        'feature': feature_name,
        'count': len(numbers),
        'mean': _calculate_mean(numbers),
        'std_dev': _calculate_std_dev(numbers),
        'min': round(min(numbers), 2),
        '25%': _calculate_percentile(numbers, 25),
        '50% (median)': _calculate_median(numbers),
        '75%': _calculate_percentile(numbers, 75),
        'max': round(max(numbers), 2)
    }
    save_results_csv(result, f"descriptive_stats_{feature_name}.csv")
    return result


def query_average_sleep_hours_stroke(data):
    """xi. Sleep hours stats for stroke vs non-stroke patients."""
    sleep_stroke = _get_numeric_values(data, 'Sleep Hours', {'Stroke Occurrence': 1})
    sleep_no_stroke = _get_numeric_values(data, 'Sleep Hours', {'Stroke Occurrence': 0})
    result = {
        'stroke': {
            'count': len(sleep_stroke),
            'mean': _calculate_mean(sleep_stroke),
            'median': _calculate_median(sleep_stroke),
            'mode': _calculate_mode(sleep_stroke),
            'std_dev': _calculate_std_dev(sleep_stroke),
            'min': round(min(sleep_stroke), 2) if sleep_stroke else None,
            '25%': _calculate_percentile(sleep_stroke, 25),
            '75%': _calculate_percentile(sleep_stroke, 75),
            'max': round(max(sleep_stroke), 2) if sleep_stroke else None
        },
        'no_stroke': {
            'count': len(sleep_no_stroke),
            'mean': _calculate_mean(sleep_no_stroke),
            'median': _calculate_median(sleep_no_stroke),
            'mode': _calculate_mode(sleep_no_stroke),
            'std_dev': _calculate_std_dev(sleep_no_stroke),
            'min': round(min(sleep_no_stroke), 2) if sleep_no_stroke else None,
            '25%': _calculate_percentile(sleep_no_stroke, 25),
            '75%': _calculate_percentile(sleep_no_stroke, 75),
            'max': round(max(sleep_no_stroke), 2) if sleep_no_stroke else None
        }
    }
    save_results_csv(result, "average_sleep_hours_stroke.csv")
    return result