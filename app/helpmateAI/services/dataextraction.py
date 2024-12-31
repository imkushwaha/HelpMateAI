import pdfplumber
import pandas as pd
from operator import itemgetter
import json



# Function to check whether a word is present in a table or not for segregation of regular text and tables

def check_bboxes(word, table_bbox):

    """
    Checks whether the bounding box of a word is inside the bounding box of a table.

    Args:
    word (Dict[str, float]): A dictionary representing the word's bounding box with keys 'x0', 'top', 'x1', 'bottom'.
    table_bbox (Tuple[float, float, float, float]): A tuple representing the table's bounding box as (x0, top, x1, bottom).
    bool: True if the word's bounding box is inside the table's bounding box, False otherwise.
    """
    # Check whether word is inside a table bbox.

    l = word['x0'], word['top'], word['x1'], word['bottom']
    r = table_bbox

    return l[0] > r[0] and l[1] > r[1] and l[2] < r[2] and l[3] < r[3]





def extract_text_from_pdf(single_pdf_path):

    """
    Extracts both textual content and table data from a PDF file and organizes it into a pandas DataFrame.

    The function processes each page in the provided PDF, extracting the text outside of any tables, 
    as well as the table content. It clusters words and table data vertically based on their position 
    and returns a DataFrame where each row corresponds to a page, with the page number and 
    corresponding text/table content.

    Args:
    single_pdf_path (str): The file path of the PDF from which text and table data should be extracted.

    Returns:
    pd.DataFrame: A DataFrame with two columns:
                  - `page_number`: The page number (e.g., 'Page 1', 'Page 2', etc.)
                  - `page_context`: A concatenated string of extracted text and JSON-encoded table data for each page.
    """


    p = 0
    full_text = []


    with pdfplumber.open(single_pdf_path) as pdf:
        for page in pdf.pages:
            page_no = f"Page {p+1}"
            text = page.extract_text()

            tables = page.find_tables()
            table_bboxes = [i.bbox for i in tables]
            tables = [{'table': i.extract(), 'top': i.bbox[1]} for i in tables]
            non_table_words = [word for word in page.extract_words() if not any(
                [check_bboxes(word, table_bbox) for table_bbox in table_bboxes])]
            lines = []

            for cluster in pdfplumber.utils.cluster_objects(non_table_words + tables, itemgetter('top'), tolerance=5):

                if 'text' in cluster[0]:
                    try:
                        lines.append(' '.join([i['text'] for i in cluster]))
                    except KeyError:
                        pass

                elif 'table' in cluster[0]:
                    lines.append(json.dumps(cluster[0]['table']))


            full_text.append([page_no, " ".join(lines)])
            p +=1
        dataframe = pd.DataFrame(full_text, columns=["page_number", "page_context"])

    return dataframe

















