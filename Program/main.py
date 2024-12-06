import os
import fitz  
import re
import requests
import json

list = []

def initial_check():
    # Ελέγχει αν τα θεματα υπαρχουν
    if not os.path.exists(r"PDFs\B"):
        print("Required libraries were not found. Downloading..")
    # PDF (Θεματα) Version Check
    git_config_file = "https://raw.githubusercontent.com/sharl16/Trapeza_Thematwn_Searcher/refs/heads/main/Program/config.ini"
    response = requests.get(git_config_file)
    response_data = response.json()
    local_json = None
    online_json = None
    if response.status_code == 200: # 200: OK
        with open('config.json') as f:
            local_json = json.load(f)
        with open(response_data) as j:
            online_json = json.load(j)
        print(local_json, online_json)
        if local_json != online_json:
            user_response = input("PDFs are out of date! Update? (y/n)").lower()
            if user_response == "y":
                print("Downloading new PDFs..")
            else:
                print("Skipped update. Using older version: ")
        else:
            print("PDFs up to date!")
    else:
        print("Failed to get response from remote server: "+str(response.status_code))

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