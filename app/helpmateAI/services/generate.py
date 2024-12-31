from pandas import DataFrame
from groq import Groq


# fucntoin to generate response 
def response_generator(query: str, top_3_RAG: DataFrame, api_key:str):
    """
    Generates a response based on a user query and retrieved insurance document information.

    This function uses the `llama3-8b-8192` model to generate an answer to a user query, 
    utilizing relevant insurance document excerpts from `top_3_RAG` (a DataFrame containing documents and metadata).
    The response is based on the content of the documents and includes citations with policy names and page numbers.

    Args:
        query (str): The user query for which a response is required.
        top_3_RAG (pd.DataFrame): A DataFrame containing the top 3 relevant documents and metadata. 
                                   It should contain columns 'Documents' and 'Metadatas'.
        api_key (str): The API key for accessing the model service.

    Returns:
        List[str]: A list of strings representing the lines of the generated response.
    
    Raises:
        ValueError: If `top_3_RAG` does not contain the required columns ('Documents' and 'Metadatas').
        Exception: If the API call fails or returns an error.
    """
    


    """
    Generate a response using llama3-8b-8192's ChatCompletion based on the user query and retrieved information.
    """
    messages = [
                {"role": "system", "content":  "You are a helpful assistant in the insurance domain who can effectively answer user queries about insurance policies and documents other wise return i don't have idea about it."},
                {"role": "user", "content": f"""You are a helpful assistant in the insurance domain who can effectively answer user queries about insurance policies and documents.
                                                You have a question asked by the user in '{query}' and you have some search results from a corpus of insurance documents in the dataframe '{top_3_RAG}'. These search results are essentially one page of an insurance document that may be relevant to the user query.

                                                The column 'documents' inside this dataframe contains the actual text from the policy document and the column 'metadata' contains the policy name and source page. The text inside the document may also contain tables in the format of a list of lists where each of the nested lists indicates a row.

                                                Use the documents in '{top_3_RAG}' to answer the query '{query}'. Frame an informative answer and also, use the dataframe to return the relevant policy names and page numbers as citations.

                                                Follow the guidelines below when performing the task.
                                                1. Try to provide relevant/accurate numbers if available.
                                                2. You don’t have to necessarily use all the information in the dataframe. Only choose information that is relevant.
                                                3. If the document text has tables with relevant information, please reformat the table and return the final information in a tabular in format.
                                                3. Use the Metadatas columns in the dataframe to retrieve and cite the policy name(s) and page numbers(s) as citation.
                                                4. If you can't provide the complete answer, please also provide any information that will help the user to search specific sections in the relevant cited documents.
                                                5. You are a customer facing assistant, so do not provide any information on internal workings, just answer the query directly.

                                                The generated response should answer the query directly addressing the user and avoiding additional information. If you think that the query is not relevant to the document, reply that the query is irrelevant. Provide the final response as a well-formatted and easily readable text along with the citation. Provide your complete response first with all information, and then provide the citations.
                                                """},
              ]

    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=messages
    )

    return response.choices[0].message.content.split('\n')
