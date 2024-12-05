import os
import fitz  
import re

list = []

def normalize_text(text):
    text = re.sub(r'\s+', ' ', text)  
    text = text.strip()  
    return text

def index_pdf(folder_path, word_to_find):
    word_to_find = normalize_text(word_to_find.lower())

    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            file_path = os.path.join(folder_path, filename)
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

subject = input('Επιλογή Μαθήματος (ΦΥΣΙΚΗ ΘΕΤΙΚΗ/ ΜΑΘΗΜΑΤΙΚΑ ΘΕΤΙΚΗ/ ΑΛΓΕΒΡΑ/ ΓΛΩΣΣΑ)')
print("Επιλέχθηκε: "+subject)
segment = input('Επιλογή εκφώνησης')

if subject == 'ΦΥΣΙΚΗ ΘΕΤΙΚΗ':
    index_pdf(r'Mathimata\B\Fysikh', segment)
elif subject == "ΜΑΘΗΜΑΤΙΚΑ ΘΕΤΙΚΗ":
    index_pdf(r'Mathimata\B\Math_Kateuth', segment)
elif subject == "ΑΛΓΕΒΡΑ":
    index_pdf(r'Mathimata\B\Algebra', segment)
elif subject == "ΓΛΩΣΣΑ":
    index_pdf(r'Mathimata\B\Glwssa', segment)
else:
    print("Δεν υπάρχει το μάθημα: "+subject)

if list == []:
    print("Δεν βρέθηκαν αποτελέσματα.")
else:
    print(list)

end = input('Press any key to close..')