"""
TODOs 

1. Add class for extracting PDFs

2. For DOCX read heading of file

3. For PPTX add logic to extract finer paragraphs
    from shapes in slides
    
4. Replace naive tokenizer with RegEx based tockenizer
   Ref - https://stackoverflow.com/questions/3845423/remove-empty-strings-from-a-list-of-strings
"""


# url = "https://en.wikipedia.org/wiki/Information_retrieval"
# html = urlopen(url).read()

# soup = BeautifulSoup(open(generate_filename('html')), "html.parser")
# txtFileObj = soup.get_text('\n')

# print(txtFileObj)

# # importing required modules
# import PyPDF2
 
# # creating a pdf file object
# pdfFileObj = open('samples/sample_2_pdf.pdf', 'rb')
 
# # creating a pdf reader object
# pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
 
# # printing number of pages in pdf file
# print(pdfReader.numPages)
 
# # creating a page object
# pageObj = pdfReader.getPage(0)
 
# # extracting text from page
# text = pageObj.extractText()
# print(text)
# print(type(text))
 
# # closing the pdf file object
# pdfFileObj.close()