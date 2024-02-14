import streamlit as st
import pandas as pd
import base64,random
import time,datetime
import spacy
nlp = spacy.load('en_core_web_md')
from pyresparser import ResumeParser
from pdfminer3.layout import LAParams, LTTextBox
from pdfminer3.pdfpage import PDFPage
from pdfminer3.pdfinterp import PDFResourceManager
from pdfminer3.pdfinterp import PDFPageInterpreter
from pdfminer3.converter import TextConverter
import io,random
from streamlit_tags import st_tags
from PIL import Image
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer 
import plotly.express as px 
import nltk
nltk.download('stopwords')


def pdf_reader(file):
    resource_manager = PDFResourceManager()
    fake_file_handle = io.StringIO()
    converter = TextConverter(resource_manager, fake_file_handle, laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)
    with open(file, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)
            print(page)
        text = fake_file_handle.getvalue()

    converter.close()
    fake_file_handle.close()
    return text

def show_pdf(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
   
    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
    st.markdown(pdf_display, unsafe_allow_html=True)


import os

folder_path = r'C:\Users\pratistha\Downloads\resume-20240212T152443Z-001\resume\Uploaded_Resumes'
job_description=pdf_reader(r'C:\Users\pratistha\Downloads\resume-20240212T152443Z-001\resume\job_description.pdf')
similarities={}
for file_name in os.listdir(folder_path):
    file_path = os.path.join(folder_path, file_name)
    if os.path.isfile(file_path):
        print(file_path)
 
        with open(file_path, 'r') as f:
            
            a=pdf_reader(file_path)


            # content = [job_description, a]
            # cv = CountVectorizer() 
            # count_matrix = cv.fit_transform(content)
            # mat = cosine_similarity(count_matrix) 
            # pdf_display = F'<h3>{file_path}</h3><br><p>{a}</p><p>{mat}</p> <p>resume Matches by:<b>{str(mat[1][0]*100) + '%'}</b></p>'
            
            
            doc1 = nlp(job_description)
            doc2 = nlp(a)
            similarity = doc1.similarity(doc2) 
            similarities[file_name]=similarity
            # Create web page with CSS
            html = '<html><head><style>.match-score{font-size:24px;font-weight:bold;color:#488f31;}.content{padding:20px;}</style></head><div class="content"><h2>Resume Matching</h2><div><b>Resume:</b>' + file_path + '</div><p>' + a[:500] + '...</p><div class="match-score">Match Score: ' + str(int(similarity*100)) + '%</div></div></html>'
            st.markdown(html, unsafe_allow_html=True)

sorted_sim = []

for k, v in similarities.items():
  sorted_sim.append((v, k)) 
   
for i in range(len(sorted_sim)):
  for j in range(len(sorted_sim)-i-1):
    if sorted_sim[j][0] < sorted_sim[j + 1][0]:
      temp = sorted_sim[j]
      sorted_sim[j]= sorted_sim[j + 1]
      sorted_sim[j + 1]= temp

# Display overall table
rows = ""   
for score, file_path in sorted_sim:
    rows += f"<tr><td>{file_path}</td><td>{score*100}%</td></tr>"

table_html = """
<table>
<tr><th>Resume</th><th>Match %</th></tr>
{0}  
</table> 
""".format(rows)
   
st.markdown(table_html, unsafe_allow_html=True)
