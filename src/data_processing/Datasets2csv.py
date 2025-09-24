import pandas as pd
from collections import defaultdict

def parse_all_file(file_path):
    """
    Parse a .ALL file (e.g., carn.ALL) and convert it to a DataFrame.
    
    Parameters:
        file_path (str): Path to the .ALL file
    
    Returns:
        pd.DataFrame: DataFrame with columns ['DocID', 'Title', 'Author', 'Source', 'Text']
    """
    docs = []
    current_doc = defaultdict(str)
    current_field = None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('.I'):
                    # Save previous document if exists
                    if current_doc['DocID']:
                        docs.append(current_doc)
                    # Start new document
                    current_doc = defaultdict(str)
                    current_doc['DocID'] = int(line.split()[1])  # 0-based indexing
                elif line.startswith('.T'):
                    current_field = 'Title'
                elif line.startswith('.A'):
                    current_field = 'Author'
                elif line.startswith('.B'):
                    current_field = 'Source'
                elif line.startswith('.W'):
                    current_field = 'Text'
                elif current_field and line:
                    current_doc[current_field] += ' ' + line
            # Append the last document
            if current_doc['DocID']:
                docs.append(current_doc)
    
        # Convert to DataFrame
        df = pd.DataFrame(docs)
        df['DocID'] = df['DocID'].astype(int)
        # Ensure all expected columns exist
        for col in ['DocID', 'Title', 'Author', 'Source', 'Text']:
            if col not in df:
                df[col] = ''
        return df[['DocID', 'Title', 'Author', 'Source', 'Text']]
    
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return pd.DataFrame()

def parse_rel_file(file_path):
    """
    Parse a .REL file (e.g., carn.REL) and convert it to a DataFrame.
    
    Parameters:
        file_path (str): Path to the .REL file
    
    Returns:
        pd.DataFrame: DataFrame with columns ['QueryID', 'DocID', 'Relevance']
    """
    qrels = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                parts = line.strip().split()
                if len(parts) >= 2:  # Ensure valid line
                    query_id = int(parts[0])
                    doc_id = int(parts[1])
                    relevance = int(parts[2]) if len(parts) > 2 else 1  # Default relevance to 1 if not specified
                    qrels.append({'QueryID': query_id, 'DocID': doc_id, 'Relevance': relevance})
        
        # Convert to DataFrame
        df = pd.DataFrame(qrels)
        return df[['QueryID', 'DocID', 'Relevance']]
    
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return pd.DataFrame()

def convert_to_csv(input_file, output_file, file_type='ALL'):
    """
    Convert a .ALL or .REL file to CSV.
    
    Parameters:
        input_file (str): Path to input file
        output_file (str): Path to output CSV file
        file_type (str): 'ALL' for documents or 'REL' for relevance judgments
    """
    if file_type == 'ALL':
        df = parse_all_file(input_file)
    elif file_type == 'REL':
        df = parse_rel_file(input_file)
    elif file_type == 'QRY':
        df = parse_qry_file(input_file)
    else:
        raise ValueError("file_type must be 'ALL' or 'REL'")
    
    if not df.empty:
        df.to_csv(output_file, index=False)
        print(f"Successfully converted {input_file} to {output_file}")
    else:
        print(f"No data to save for {input_file}")

def parse_qry_file(file_path):
    """Parse a .QRY file and convert it to a DataFrame."""
    queries = []
    current_query = defaultdict(str)
    current_field = None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line.startswith('.I'):
                    if current_query['QueryID']:
                        queries.append(current_query)
                    current_query = defaultdict(str)
                    current_query['QueryID'] = int(line.split()[1])
                elif line.startswith('.W'):
                    current_field = 'Text'
                elif current_field and line:
                    current_query[current_field] += ' ' + line
            if current_query['QueryID']:
                queries.append(current_query)
        
        df = pd.DataFrame(queries)
        df['QueryID'] = df['QueryID'].astype(int)
        return df[['QueryID', 'Text']]
    
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return pd.DataFrame()


# Example usage for multiple datasets
datasets = ['cran', 'CISI', 'MED']  # List of dataset prefixes
base_path = './collections'  # Update with actual path to files

for dataset in datasets:
    # Convert .ALL file
    all_file = f"{base_path}/{dataset}/{dataset}.ALL"
    convert_to_csv(all_file, f"{base_path}/{dataset}_docs.csv", file_type='ALL')
    
    # Convert .REL file
    rel_file = f"{base_path}/{dataset}/{dataset}.REL"
    convert_to_csv(rel_file, f"{base_path}/{dataset}_qrels.csv", file_type='REL')

    qry_file = f"{base_path}/{dataset}/{dataset}.QRY"
    convert_to_csv(qry_file, f"{base_path}/{dataset}_queries.csv", file_type='QRY')