import os
os.getcwd()

os.chdir('D~)
os.listdir()

import fitz
import difflib
import pandas as pd
import re

def normalize_text(text):
    text = re.sub(r'\s+', '', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.lower()
    
def extract_text_only(pdf_path):
    doc = fitz.open(pdf_path)
    text_pages = []
    for page in doc:
        text = ''
        blocks = page.get_text("dict")["blocks"]
        for block in blocks:
            if block["type"] == 0:
                text += ''.join([line["spans"][0]["text"] for line in block["lines"]])+"\n"
        text_pages.append(text)
    doc.close()
    return text_pages
    
def compare_text(text1, text2):
    text1 = normalize_text(text1)
    text2 = normalize_text(text2)
    words1 = text1.split()
    words2 = text2.split()
    s = difflib.SequenceMatcher(None, words1, words2)
    differences = []
    for opcode in s.get_opcodes():
        if opcode[0] == 'replace' or opcode[0] == 'delete' or opcode[0] == insert':
            differences.extend([words2[i] for i in range(opcode[3], opcode[4])])
    return s.get_matching_blocks(), s.ratio(), differences
    
def extract_differences(pdf_path1, pdf_path2):
    texts1 = extract_text_only(pdf_path1)
    texts2 = extract_text_only(pdf_path2)
    results = []
    
    for page_number in range(min(len(texts1), len(texts2))):
        text1 = texts1[page_number]
        text2 = texts2[page_number]
        matching_blocks, similarity, changed_words = compare_texts(text1,text2)
        
        if similarity<1:
            results.append({
            	"File 1 page" : page_number +1,
            	"File 2 page" : page_number +1,
        		"Text from File 1" : text1,
            	"Text from File 2" : text2,
            	"Similarity" : similarity,
        		"Changed Words" : ', '.join(changed_words)
            })
            
    return results
    
def save_result_to_excel(result, output_excel_path):
    print("결과를 엑셀 파일로 저장합니다")
    df = pd.DataFrame(results)
    df.to_excel(output_excel_path, index = False)
    
    
result = extract_differences("D:\\~, "D:\\~)

if results:
    save_result_to_excel(results, "D:\\~))
             


                
                
                
                
                
    
    
    