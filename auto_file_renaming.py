# pip install pdfminer.six
# pip install PyMuPDF

import os
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
import fitz


# getting the text of the first pdf-pdfpage


def first_page_str(og_filename):
    """ takes a pdf-file
        and returns a string with the text on the first page
    """
    output_string = StringIO()

    with open(og_filename, "rb") as in_file:
        parser = PDFParser(in_file)
        doc = PDFDocument(parser)
        rsrcmgr = PDFResourceManager()
        device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.create_pages(doc):
            interpreter.process_page(page)

        text = output_string.getvalue()
        text_pages = text.split("\x0c")
        new_filename = text_pages[0].strip()

    return new_filename


# creating a new file / deleting the first page of a pdf-file

def delete_page(og_filename, new_filename):
    doc = fitz.open(og_filename)
    num_pages = doc.pageCount
    keep = list(range(num_pages))[1:]
    doc.select(keep)
    doc.save(new_filename+".pdf")

    return True


# removing the redundant file

def remove_og(og_filename):
    os.remove(og_filename)

    return True


# automating file renameing

def magic_entry(og_filename):
    new_filename = first_page_str(og_filename)
    delete_page(og_filename, new_filename)
    remove_og(og_filename)

    return True


# magic_entry("00035.pdf")
