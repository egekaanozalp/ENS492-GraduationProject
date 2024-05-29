from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os
import time
import shutil

start_time = time.time()
download_dir = "/Users/selimgul/Projects/ens491-webscraping/"  # Change this to your desired download path
download_prefs = {"download.default_directory": download_dir,
                  "download.prompt_for_download": False,
                  "download.directory_upgrade": True,
                  "safebrowsing.enabled": True}
chrome_options = Options()
chrome_options.add_experimental_option("prefs", download_prefs)

# Initialize the WebDriver with the specified options
driver = webdriver.Chrome(executable_path='/Users/selimgul/Downloads/chromedriver-mac-arm64/chromedriver', options=chrome_options)

driver.get('https://sonuc.ysk.gov.tr/sorgu')


def secim_choice(driver):
    global secim_no
    global secim_yili
    dropdown = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "ng-select[formcontrolname='secim'] .ng-select-container"))
    )
    dropdown.click()
    secim = input("Type 1 for 30 March 2014 elections, 2 for 31 March 2019 elections: ")
    if (secim == "1"):
        secim_no = "1"
        secim_yili = "2014"
        option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '30 MART 2014 MAHALLİ İDARELER GENEL SEÇİMİ')]"))
    )
    elif (secim == "2"):
        secim_no = "2"
        secim_yili = "2019"
        option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '31 MART 2019 MAHALLİ İDARELER GENEL SEÇİMİ')]"))
    )
    elif (secim == "3"):
        secim_no = "3"
        secim_yili = "2024"
        option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), '31 MART 2024 MAHALLİ İDARELER GENEL SEÇİMİ')]"))
    )
    else:
        print("Invalid input, please try again.")
        secim_choice(driver)
    driver.execute_script("arguments[0].click();", option)

def secim_turu_choice(driver):
    global secim_turu_no
    global secim_turu_adi
    dropdown = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "ng-select[formcontrolname='secimTuru'] .ng-select-container"))
    )
    dropdown.click()
    secim_turu = input("Type 1 for BELEDİYE BAŞKANLIĞI SEÇİMLERİ, 2 for BELEDİYE MECLİSİ SEÇİMLERİ, 3 for BÜYÜKŞEHİR BELEDİYE BAŞKANLIĞI SEÇİMLERİ, 4 for İL GENEL MECLİS ÜYELİĞİ SEÇİMLERİ: ")
    if (secim_turu == "1"):
        secim_turu_no = "1"
        secim_turu_adi = "Belediye Başkanlığı Seçimleri"
        option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ng-option') and .//span[contains(@class, 'ng-option-label') and contains(text(), 'BELEDİYE BAŞKANLIĞI SEÇİMLERİ')]]"))
    )
    elif (secim_turu == "2"):
        secim_turu_no = "2"
        secim_turu_adi = "Belediye Meclisi Üyeliği Seçimleri"
        option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ng-option') and .//span[contains(@class, 'ng-option-label') and contains(text(), 'BELEDİYE MECLİSİ ÜYELİĞİ SEÇİMLERİ')]]"))
    )
    elif (secim_turu == "3"):
        secim_turu_no = "3"
        secim_turu_adi = "Büyükşehir Belediye Başkanlığı Seçimleri"
        option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ng-option') and .//span[contains(@class, 'ng-option-label') and contains(text(), 'BÜYÜKŞEHİR BELEDİYE BAŞKANLIĞI SEÇİMLERİ')]]"))
    )
    elif (secim_turu == "4"):
        secim_turu_no = "4"
        secim_turu_adi = "İl Genel Meclisi Üyeliği Seçimleri"
        option = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'ng-option') and .//span[contains(@class, 'ng-option-label') and contains(text(), 'İL GENEL MECLİS ÜYELİĞİ SEÇİMLERİ')]]"))
    )
    else:
        print("Invalid input, please try again.")
        secim_turu_choice(driver)
    driver.execute_script("arguments[0].click();", option)

def download_data_by_ilce(driver, city, secim_yili, secim_turu_adi):
    dropdown = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "ng-select[formcontrolname='secimCevresi'] .ng-select-container"))
    )
    dropdown.click()

    options = WebDriverWait(driver, 20).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ng-dropdown-panel .ng-option"))
    )

    for index, option in enumerate(options):
        dropdown = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "ng-select[formcontrolname='secimCevresi'] .ng-select-container"))
        )
        dropdown.click()

        WebDriverWait(driver, 20).until(
            EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "ng-dropdown-panel .ng-option"))
        )

        options = driver.find_elements(By.CSS_SELECTOR, "ng-dropdown-panel .ng-option")

        text = options[index].text

        driver.execute_script("arguments[0].click();", options[index])

        time.sleep(2)

        sorgula_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-success') and contains(text(), 'Sorgula')]")))
        sorgula_button.click()

        time.sleep(5)

        save_table_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-primary') and contains(text(), 'Tabloyu Kaydet')]"))
        )

        save_table_button.click()

        time.sleep(1)

        accept_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-success') and contains(text(), 'Kabul Ediyorum')]"))
        )

        accept_button.click()

        known_file_prefix = 'Yurt-İçi'

        new_name = f'{city}-{text}.xlsx'

        wait_for_download_and_rename(download_dir, known_file_prefix, new_name, secim_yili, secim_turu_adi)

        time.sleep(2)

def sanitize_filename(filename):
    return filename.replace('/', '_')

def wait_for_download_and_rename(download_dir, file_prefix, new_full_name, secim_yili, secim_turu_adi):
    downloaded_file = None
    while not downloaded_file:
        time.sleep(1)
        for f in os.listdir(download_dir):
            if f.startswith(file_prefix) and f.endswith('.xlsx'):
                downloaded_file = f
                break

    if downloaded_file:
        old_file_path = os.path.join(download_dir, downloaded_file)
        sanitized_new_full_name = sanitize_filename(new_full_name)
        new_file_path = os.path.join(download_dir, sanitized_new_full_name)
        os.rename(old_file_path, new_file_path)
        destination = f"/Users/selimgul/Projects/ens491-webscraping/Data/{secim_yili}/{secim_turu_adi}"
        final_destination = os.path.join(destination, sanitized_new_full_name)
        os.makedirs(os.path.dirname(final_destination), exist_ok=True)
        shutil.move(new_file_path, final_destination)
    else:
        print("No file found to rename")

def check_if_downloaded(city, secim_yili, secim_turu_adi):
    destination = f"/Users/selimgul/Projects/ens491-webscraping/Data/{secim_yili}/{secim_turu_adi}/"
    if (os.path.exists(destination)):
        for file in os.listdir(destination):
            if (file.startswith(city)):
                return True

buttons = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "button"))
    )

driver.execute_script("arguments[0].click();", buttons[4])

time.sleep(3)

secim_choice(driver)

time.sleep(3)

secim_turu_choice(driver)

time.sleep(2)

submit_button = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'btn-success') and contains(text(), 'Devam Et')]"))
)
driver.execute_script("arguments[0].click();", submit_button)

time.sleep(3)

dropdown = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "ng-select[formcontrolname='il'] .ng-select-container"))
    )
dropdown.click()

options = WebDriverWait(driver, 20).until(
    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "ng-dropdown-panel .ng-option"))
)

for index, option in enumerate(options):
    dropdown = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "ng-select[formcontrolname='il'] .ng-select-container"))
    )
    dropdown.click()

    WebDriverWait(driver, 20).until(
        EC.visibility_of_all_elements_located((By.CSS_SELECTOR, "ng-dropdown-panel .ng-option"))
    )

    options = driver.find_elements(By.CSS_SELECTOR, "ng-dropdown-panel .ng-option")

    city = options[index].text

    driver.execute_script("arguments[0].click();", options[index])

    time.sleep(2)
    if (check_if_downloaded(city, secim_yili, secim_turu_adi) == True):
        print(f"{city} already downloaded.")
        continue

    download_data_by_ilce(driver, city, secim_yili, secim_turu_adi)

print("Done!")
time.sleep(3)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"Elapsed time: {elapsed_time} seconds")
