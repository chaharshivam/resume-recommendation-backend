import sys
import io
import os
incomingFileName = sys.argv[1]
filePath = os.path.dirname(os.path.abspath(__file__)) + "/incomingFile/" + incomingFileName
fileNameWithoutExtension = incomingFileName.split(".", 1)[0]
saveFilePath = os.path.dirname(os.path.abspath(__file__)) + "/extractedText/" + fileNameWithoutExtension + ".txt"
import PyPDF2

with open(filePath, 'rb') as pdf_file, io.open(saveFilePath, 'w', encoding="utf-8") as text_file:
    read_pdf = PyPDF2.PdfFileReader(pdf_file)
    number_of_pages = read_pdf.getNumPages()
    for page_number in range(number_of_pages):  # use xrange in Py2
        page = read_pdf.getPage(page_number)
        page_content = page.extractText()
        text_file.write(page_content)
        print(page_content)
