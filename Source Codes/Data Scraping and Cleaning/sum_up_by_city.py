import os
from pathlib import Path
import pandas as pd

def process_all_cities(directory, header_row_number):
    # Identify all files in the directory
    all_files = [f for f in os.listdir(directory) if f.endswith('.xlsx')]

    # Extract unique city names from the file names
    cities = set()
    for file in all_files:
        city = file.split('-')[0]
        cities.add(city)

    # Process files for each city
    for city in cities:
        # Filter files for the current city
        city_files = [f for f in all_files if f.startswith(city)]
        summed_results = pd.DataFrame()

        # Process each file
        for file in city_files:
            file_path = os.path.join(directory, file)
            df = pd.read_excel(file_path, header=header_row_number)
            # Assume the party columns start after 'Sandık No'
            party_start_index = df.columns.tolist().index('Sandık No') + 1
            party_columns = df.columns[party_start_index:]
            df_grouped = df.groupby(['İlçe Adı', 'Mahalle/Köy'])[party_columns].sum().reset_index()
            summed_results = pd.concat([summed_results, df_grouped], ignore_index=True)

        # Group by district and neighborhood again to sum up results
        final_results = summed_results.groupby(['İlçe Adı', 'Mahalle/Köy']).sum().reset_index()

        # Create the output file with a '*' prefix
        output_file = os.path.join(directory, f'*Summed_Up_Results_{city}.xlsx')
        final_results.to_excel(output_file, index=False)

        print(f"Processed files for {city}. Results saved to {output_file}")

# Call the function with the correct header_row_number
directory = '/Users/selimgul/Projects/ens491-webscraping/Data/2019-İstanbul'
process_all_cities(directory, header_row_number=10)
