import pandas as pd
import os
import json

# Directory settings
directory = "Belediye Başkanlığı"  # Other options include "Büyükşehir Belediye Başkanlığı", "Belediye Başkanlığı", "İl Genel Meclis Üyeliği"
dir_2014 = f'/Users/selimgul/Desktop/ens492/{directory}/2014'
dir_2019 = f'/Users/selimgul/Desktop/ens492/{directory}/2019'

# Initialize a list to track the removed lines' information
removed_lines_info = []
# Initialize a list to track the removed rows due to "ceza" related keywords
ceza_removed_info = []

# Function to process the files in each directory
def process_election_results(dir_path):
    city_dataframes = {}
    for filename in os.listdir(dir_path):
        if filename.endswith(".xlsx"):
            city_name = filename.replace("_Summed_Up_Results_", "").replace(".xlsx", "")
            df = pd.read_excel(os.path.join(dir_path, filename), engine='openpyxl')
            city_dataframes[city_name] = df
    return city_dataframes

# Process the excel files in each directory
data_2014 = process_election_results(dir_2014)
data_2019 = process_election_results(dir_2019)

# Function to filter rows based on keywords in "Mahalle/Köy"
def filter_ceza_rows(df, city_name, year):
    keywords = ['ceza', 'ceza evi', 'cezaevi']
    initial_count = df.shape[0]
    df_filtered = df[~df['Mahalle/Köy'].str.contains('|'.join(keywords), case=False, na=False)]
    filtered_count = df_filtered.shape[0]
    # Calculate removed rows and append to ceza_removed_info
    rows_removed = initial_count - filtered_count
    if rows_removed > 0:
        ceza_removed_info.append({
            'City': city_name,
            'Year': year,
            'Rows Removed': rows_removed
        })
    return df_filtered

# Function to collect information on removed rows
def collect_removed_rows_info(df_old, df_new, city_name, year_old, year_new):
    # Compare the old and new dataframes and find non-matching rows
    in_old_not_in_new = pd.merge(df_old, df_new[['İlçe Adı', 'Mahalle/Köy']], on=['İlçe Adı', 'Mahalle/Köy'], how='left', indicator=True)
    removed_from_old = in_old_not_in_new[in_old_not_in_new['_merge'] == 'left_only']
    
    in_new_not_in_old = pd.merge(df_new, df_old[['İlçe Adı', 'Mahalle/Köy']], on=['İlçe Adı', 'Mahalle/Köy'], how='left', indicator=True)
    removed_from_new = in_new_not_in_old[in_new_not_in_old['_merge'] == 'left_only']
    
    for _, row in removed_from_old.iterrows():
        removed_lines_info.append({
            'City': city_name,
            'Year': year_old,
            'İlçe Adı': row['İlçe Adı'],
            'Mahalle/Köy': row['Mahalle/Köy']
        })
    for _, row in removed_from_new.iterrows():
        removed_lines_info.append({
            'City': city_name,
            'Year': year_new,
            'İlçe Adı': row['İlçe Adı'],
            'Mahalle/Köy': row['Mahalle/Köy']
        })

# Compare and keep data from both years only for matching rows
for city in data_2014:
    if city in data_2019:
        # Collect info about removed rows before filtering
        collect_removed_rows_info(data_2014[city], data_2019[city], city, '2014', '2019')
        
        # Filter out rows containing specific keywords before the inner join
        data_2014[city] = filter_ceza_rows(data_2014[city], city, '2014')
        data_2019[city] = filter_ceza_rows(data_2019[city], city, '2019')

        # Perform an inner join to get rows present in both years
        common_rows_2014 = pd.merge(data_2014[city], data_2019[city][['İlçe Adı', 'Mahalle/Köy']], on=['İlçe Adı', 'Mahalle/Köy'], how='inner')
        common_rows_2019 = pd.merge(data_2019[city], data_2014[city][['İlçe Adı', 'Mahalle/Köy']], on=['İlçe Adı', 'Mahalle/Köy'], how='inner')

        # Save the cleaned data for each year
        common_rows_2014.to_excel(f'/Users/selimgul/Desktop/ens492/{directory}/{city}_2014_Cleaned_Results.xlsx', index=False)
        common_rows_2019.to_excel(f'/Users/selimgul/Desktop/ens492/{directory}/{city}_2019_Cleaned_Results.xlsx', index=False)

# Write the removed lines info to a JSON file
with open(f'/Users/selimgul/Desktop/ens492/{directory}/removed_lines_info.json', 'w') as f:
    json.dump(removed_lines_info, f, ensure_ascii=False, indent=4)

# Write the ceza removed info to a separate JSON file
with open(f'/Users/selimgul/Desktop/ens492/{directory}/*removed_cezaevi_info.json', 'w') as f:
    json.dump(ceza_removed_info, f, ensure_ascii=False, indent=4)

# Output file paths for created files
output_files = os.listdir(f'/Users/selimgul/Desktop/ens492/{directory}')
created_files = [file for file in output_files if file.endswith("_Cleaned_Results.xlsx")]
created_files_paths = [f'/Users/selimgul/Desktop/ens492/{directory}/{file}' for file in created_files]

# Display paths to user
created_files_paths
