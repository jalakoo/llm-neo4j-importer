from .n4j_utils import add_nodes_to_doc
import os
import logging
import pandas as pd

def upload(file: any) -> bool:

    logging.debug(f'upload_called')

    url = os.getenv("NEO4J_URI")
    username = os.getenv("NEO4J_USERNAME")
    password = os.getenv("NEO4J_PASSWORD")

    # Get filename
    filename = file.name

    try:
        # Use pandas to quickly read and manipulate csv data
        df = pd.read_csv(file, keep_default_na=False)

        nodes = []

        for index, row in df.iterrows():
            print("Row Index:", index)

            row_pairs = []

            # Iterate over columns
            for column_name, column_value in row.items():
                if column_value is None or column_value == '':
                    continue
                else:
                    print("Column:", column_name, "Value:", column_value)
                    row_pairs.append([column_name, column_value])

            nodes.append(row_pairs)

        # Will build connections between doc, rows, and values but doesn't accurately describe inferred relationships

        add_nodes_to_doc(
            filename,
            nodes,
            url,
            username,
            password,
        )
        return f"Successfully uploaded {filename}"
    
    except Exception as e:
        return f"{e}"

