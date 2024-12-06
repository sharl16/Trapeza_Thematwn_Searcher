import os
import fitz
import re
import requests
import json
import urllib

list = []


def download_pdf():
    drive_pdf_link = "https://drive.google.com/drive/folders/19HQd-G7Iat0jhmIIv9KSazv6mdHt_ZdW?usp=sharing"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pdfs_dir = os.path.join(current_dir, '..', '..')
    if os.path.exists(f"{pdfs_dir}/PDFs"):
        print("Deleting old libraries..")
        os.rmdir(f"{pdfs_dir}/PDFs")
        
    output = os.path.join(pdfs_dir, 'PDFs')
    
    try:
        response = requests.get(drive_pdf_link, stream=True)
        response.raise_for_status()
        with open(output, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        print("New library has finished downloading..")
    except requests.exceptions.RequestException as e:
        print(f"Failed to download libraries: {e}")


def initial_check():
    # Ελέγχει αν τα θεματα υπαρχουν
    if not os.path.exists(r"PDFs\B"):
        print("Required libraries were not found. Downloading..")
    # PDF (Θεματα) Version Check
    git_config_file = "https://raw.githubusercontent.com/sharl16/Trapeza_Thematwn_Searcher/refs/heads/main/Program/config.json"
    try:
        response = requests.get(git_config_file, stream=True).json()
        local_json = None
        with open(r'Program\config.json') as f:
            local_json = json.load(f)
            print(local_json)
        online_json = response
        print(local_json, online_json)
        if local_json != online_json:
            user_response = input("Libraries are out of date! Update? (y/n)").lower()
            if user_response == "y":
                print("Downloading new libraries..")
                download_pdf()
            else:
                print("Skipped update. Using older version: ")
        else:
            print("PDFs up to date!")
    except requests.exceptions.RequestException as e:
        print(f"Failed to check for updates: {e}")

initial_check()

def normalize_text(text):
    text = re.sub(r'\s+', ' ', text)  
    text = text.strip()  
    return text

def index_in_pdf(file_path, filename, word_to_find):
    print(f"Searching in: {filename}")
    with fitz.open(file_path) as pdf_document:
                for page_num in range(pdf_document.page_count):
                    page = pdf_document.load_page(page_num)  
                    text = page.get_text()  
                    
                    if text:
                        normalized_text = normalize_text(text.lower())
                        if word_to_find in normalized_text:
                            list.insert(len(filename), filename)
                            break

def index_frontend(folder_path, word_to_find):
    word_to_find = normalize_text(word_to_find.lower())

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
            index_in_pdf(file_path, filename, word_to_find) 

subject = input('Επιλογή Μαθήματος (ΦΥΣΙΚΗ ΘΕΤΙΚΗ/ ΜΑΘΗΜΑΤΙΚΑ ΘΕΤΙΚΗ/ ΑΛΓΕΒΡΑ/ ΓΛΩΣΣΑ)')
print("Επιλέχθηκε: "+subject)
segment = input('Επιλογή εκφώνησης')

if subject == 'ΦΥΣΙΚΗ ΘΕΤΙΚΗ':
    index_frontend(r'PDFs\B\Fysikh', segment)
elif subject == "ΜΑΘΗΜΑΤΙΚΑ ΘΕΤΙΚΗ":
    index_frontend(r'Mathimata\B\Math_Kateuth', segment)
elif subject == "ΑΛΓΕΒΡΑ":
    index_frontend(r'Mathimata\B\Algebra', segment)
elif subject == "ΓΛΩΣΣΑ":
    index_frontend(r'Mathimata\B\Glwssa', segment)
else:
    print("Δεν υπάρχει το μάθημα: "+subject)

if list == []:
    print("Δεν βρέθηκαν αποτελέσματα.")
else:
    print(list)

end = input('Press any key to close..')