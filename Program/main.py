import os
import fitz  
import re
import requests
import configparser

list = []

def initial_check():
    # Ελέγχει αν τα θεματα υπαρχουν
    if not os.path.exists(r"PDFs\B"):
        print("Required libraries were not found. Downloading..")
    # PDF (Θεματα) Version Check
    git_config_file = "https://raw.githubusercontent.com/sharl16/Trapeza_Thematwn_Searcher/refs/heads/main/Program/config.json"
    response = requests.get(git_config_file)
    if response.status_code == 200: # 200: OK
        config = configparser.ConfigParser()
        config.read('config.ini')
        remote_config = configparser.ConfigParser()
        remote_config.read_string(response.text)
        local_ver = config['ALL']['pdf_version']
        remote_ver = remote_config['ALL']['pdf_version']
        if local_ver != remote_ver:
            user_response = input("PDFs are out of date! Update? (new: " + remote_ver + ", old: " + local_ver + ") (y/n): ").lower()
            if user_response == "y":
                print("Downloading new PDFs..")
            else:
                print("Skipped update. Using older version: "+local_ver)



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