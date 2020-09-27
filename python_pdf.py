import fitz
import re
import os

current_path = os.path.dirname(os.path.abspath(__file__))

def get_sensitive_data(lines,text_to_remove):
    """
    Finds the text that needs to replaced from the original PDF

    Parameters
    ----------
    lines : str
        string data from the pdf
    text_to_remove : str
        string that needs to be removed
    """
    for line in lines:
        if re.search(text_to_remove, line, re.IGNORECASE):
            search = re.search(text_to_remove, line, re.IGNORECASE)
            yield search.group()

def replace_text(file1_path,file2_path,header_string,bill_to_string):

    """
    Takes the input strings and replaces them with Page Header and 'Bill to: Name' of invoice.
    Also merges with the second PDF file

    Parameters
    ----------
    file1_path     : str
        file path of the pdf whose text is to be replaced
    file2_path     : str
        file path of the pdf which is to be merged with the first pdf
    header_string  : Str
        header to be replaced with old header
    bill_to_string : str
        new name of the person in 'Bill To Address'

    """

    doc = fitz.open(os.path.join(current_path,file1_path))
    doc2 = fitz.open(os.path.join(current_path,file2_path))
    for page in doc:
        page._wrapContents()
        sensitive_header = get_sensitive_data(page.getText("text").split('\n'),'TUSCARORA HARDWOODS, INC.')
        sensitive_bill_to = get_sensitive_data(page.getText("text").split('\n'),'Bill To: ')
        for data in sensitive_header:
            areas = page.searchFor(data)
            #adding the text-annot ABOVE the given text input
            [page.addFreetextAnnot(area, header_string, fontsize=12, fontname="helv", text_color=0, fill_color=1, rotate=0,align =1) for area in areas]
        for data in sensitive_bill_to:
            areas = page.searchFor(data)
            bill_areas = []
            for ara in areas:
                #adding the text-annot AFTER the given string input
                bill_areas.append(fitz.Rect(ara.top_right,ara.bottom_right + fitz.Point(200,0)))
            [page.addFreetextAnnot(area, bill_to_string, fontsize=9, fontname="helv", text_color=0, fill_color=1, rotate=0) for area in bill_areas]
        page.apply_redactions()
    doc.insertPDF(doc2)
    doc.save('output.pdf')
    print("Successfully replaced text and merged PDFs")

#EXAMPLE
#replace_text('Python- 01.pdf','Python-02.pdf','Netzary Infodynamics','Prinjal Boruah')
