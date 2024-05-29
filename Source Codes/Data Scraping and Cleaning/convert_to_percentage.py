import pandas as pd
import os

base_dir = '/Users/selimgul/Desktop/ens492/İl Genel Meclis Üyeliği/cleaned results' # burayı değiştir cleaned değil ve il genel değil,path'i ayarlarsın

def votes_to_percentage(df, party_columns):
    for party in party_columns:
        df[party] = (df[party] / df["Toplam Geçerli Oy"]).round(5)
    return df

def process_files(directory):
    for filename in os.listdir(directory):
        if filename.endswith("_Cleaned_Results.xlsx"): # bunu değiş
            city_year = filename.replace("_Cleaned_Results.xlsx", "") # bunu değil
            df = pd.read_excel(os.path.join(directory, filename), engine='openpyxl')

            # Aşağıdakilerin aynı olması lazım
            non_party_columns = ['İlçe Adı', 'Mahalle/Köy', 'Kayıtlı Seçmen Sayısı', 'Oy Kullanan Seçmen Sayısı', 'İtirazsız Geçerli Oy Sayısı', 'İtirazlı Geçerli Oy Sayısı', 'Toplam Geçerli Oy', 'Toplam Geçersiz Oy']
            party_columns = [col for col in df.columns if col not in non_party_columns]

            df = votes_to_percentage(df, party_columns)

            # Bu aşağı da path'i ayarlarsın
            output_filename = f'{city_year}_Percentage_Results.xlsx'
            df.to_excel(os.path.join("/Users/selimgul/Desktop/ens492/İl Genel Meclis Üyeliği/percentage results", output_filename), index=False)

# Process all Excel files in the directory
process_files(base_dir)
