# import parser object from tike
from tika import parser
import tika
import os
from decouple import config



def extract_text_from_pdf(file_path):
    """
    Extracts text from a PDF file using Apache Tika.

    Args:
        file_path (str): The path to the PDF file.
    Returns: tuple (str, dict, int)
    """
    parsed_pdf = parser.from_file(file_path, config('TIKA_SERVER_ENDPOINT'))
    data = parsed_pdf['content'] 
    metadata = parsed_pdf['metadata']
    status = parsed_pdf["status"]
    return data, metadata, status



content, metadata, status = extract_text_from_pdf('doc.pdf')
print(content)