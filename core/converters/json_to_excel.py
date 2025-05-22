import pandas as pd
import json

def flatten_json(y, sep='_'):
    """
    Recursively flattens a nested JSON object, including arrays.
    """
    out = {}

    def flatten(x, name=''):
        if isinstance(x, dict):
            for key in x:
                flatten(x[key], f"{name}{key}{sep}")
        elif isinstance(x, list):
            for i, item in enumerate(x):
                flatten(item, f"{name}{i}{sep}")
        else:
            out[name[:-1]] = x

    flatten(y)
    return out

def process_nested_json(data):
    """
    Processes nested JSON objects and arrays into a flat structure.
    """
    if isinstance(data, list):
        flattened_data = [flatten_json(item) for item in data]
    elif isinstance(data, dict):
        flattened_data = [flatten_json(data)]
    else:
        raise ValueError("Unsupported JSON structure")
    return flattened_data

def convert_json_to_excel(json_file, output_excel_path):
    """
    Converts uploaded JSON file to Excel format after flattening.

    Parameters:
    - json_file: file-like object (e.g., request.FILES['json_file'])
    - output_excel_path: path to save the Excel file
    """
    data = json.load(json_file)
    flattened_data = process_nested_json(data)
    df = pd.DataFrame(flattened_data)
    df.to_excel(output_excel_path, index=False)
