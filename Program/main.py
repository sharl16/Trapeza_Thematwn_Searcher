import os
import fitz
import re
import requests
import json
import shutil
import zipfile
from clint.textui import progress

list = []


def download_pdf():
    drive_pdf_link = "https://drive.usercontent.google.com/download?id=1i9G7jwnOA66tgBqc54f-cRh7t4Yvmhqh&export=download&authuser=0&confirm=t&uuid=04e9c882-615b-4eb0-859e-34423d71a931&at=APvzH3qY6_v6jfnozoMeH-hNYr0e%3A1734253857478"
    if os.path.exists(r"PDFs"):
        shutil.rmtree(r"PDFs")
    
    output = os.path.join(r"PDFs")
    
    try:
        print("Downloading new PDFs..")
        response = requests.get(drive_pdf_link, stream=True, timeout=(10, 30))
        response.raise_for_status()
        with open(output, 'wb') as file:
            total_length = int(response.headers.get('content-length'))
            for chunk in progress.bar(response.iter_content(chunk_size=16384), expected_size=(total_length/16384) + 1):
                file.write(chunk)

        print("Extracting PDFs.zip..")
        with zipfile.ZipFile(r"PDFs", 'r') as zip_ref:
            zip_ref.extractall()
        os.remove(r"PDFs")
                
    except requests.exceptions.RequestException as e:
        print(f"Failed to download libraries: {e}")


def initial_check():
    # Ελέγχει αν τα θεματα υπαρχουν
    if not os.path.exists(r"B"):
        print("Required libraries were not found. Downloading..")
    # PDF (Θεματα) Version Check
    git_config_file = "https://raw.githubusercontent.com/sharl16/Trapeza_Thematwn_Searcher/refs/heads/main/PDFs/version.json"
    print("Verifying with server..")
    try:
        session = requests.session()
        response = session.get(git_config_file, stream=True, timeout=(10, 30)).json()
        local_json = None
        with open(r'version.json') as f:
            local_json = json.load(f)
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

# initial_check()
download_pdf()

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
    index_frontend(r'B\Fysikh', segment)
elif subject == "ΜΑΘΗΜΑΤΙΚΑ ΘΕΤΙΚΗ":
    index_frontend(r'B\Math_Kateuth', segment)
elif subject == "ΑΛΓΕΒΡΑ":
    index_frontend(r'B\Algebra', segment)
elif subject == "ΓΛΩΣΣΑ":
    index_frontend(r'B\Glwssa', segment)
else:
    print("Δεν υπάρχει το μάθημα: "+subject)

if list == []:
    print("Δεν βρέθηκαν αποτελέσματα.")
else:
    print(list)

end = input('Press any key to close..')