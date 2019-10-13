from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer


def createPDFDoc(fpath):
    fp = open(fpath, 'rb')
    parser = PDFParser(fp)
    document = PDFDocument(parser, password='')
    # Check if the document allows text extraction. If not, abort.
    if not document.is_extractable:
        raise Exception("Not extractable")
    else:
        return document


def createDeviceInterpreter():
    rsrcmgr = PDFResourceManager()
    laparams = LAParams()
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    return device, interpreter


def parse_obj(objs):
    i=0
    for obj in objs:
        if isinstance(obj, pdfminer.layout.LTTextBox):
            print("Block:",i,obj.get_text())

            for o in obj._objs:
                if isinstance(o,pdfminer.layout.LTTextLine):
                    #print('Object',o)
                    #print('Line',i,o.get_text())
                    text=o.get_text()
                    if text.strip():
                        #print(o.get_font())
                        for c in  o._objs:
                            if isinstance(c, pdfminer.layout.LTChar):
                                #print(c,"fontname %s"%c.fontname)
                                break
            i += 1
        # if it's a container, recurse
        elif isinstance(obj, pdfminer.layout.LTFigure):
            parse_obj(obj._objs)
        else:
            pass

path = "/home/pavan/Downloads/Test2.pdf"
document=createPDFDoc(path)
device,interpreter=createDeviceInterpreter()
pages=PDFPage.create_pages(document)
interpreter.process_page(pages.next())
#layout = device.get_result()

for page in PDFPage.get_pages(open(path,'rb'), set(), maxpages=0,password="",caching=True,check_extractable=True):
    interpreter.process_page(page)
    layout = device.get_result()
    parse_obj(layout._objs)
#input('------------------------------------------------------')
