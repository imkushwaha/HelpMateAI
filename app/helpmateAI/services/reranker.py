import pandas as pd
from sentence_transformers import CrossEncoder


def sentence_cross_encoder(
    result_dataframe: pd.DataFrame, 
    query: str
) -> list[float]:
    """
    Reranks the documents in the result dataframe based on the query using a sentence-level CrossEncoder.

    This function uses a pre-trained CrossEncoder model (`cross-encoder/ms-marco-MiniLM-L-6-v2`) to
    compute relevance scores between the query and each document in the `result_dataframe`. The results
    are used to rerank the documents based on their relevance to the query.

    Args:
        result_dataframe (pd.DataFrame): A pandas DataFrame containing the documents to be ranked. 
                                         It should have a column 'Documents' with the text of the documents.
        query (str): The query string used to rerank the documents.

    Returns:
        list[float]: A list of relevance scores corresponding to each document in the `result_dataframe`,
                     where a higher score indicates higher relevance.
    """
    
    # Initialize the CrossEncoder model for sentence-level ranking
    cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

    # Create input pairs: each document paired with the query
    cross_inputs = [[query, response] for response in result_dataframe['Documents']]

    # Predict the reranking scores using the CrossEncoder model
    cross_rerank_scores = cross_encoder.predict(cross_inputs)

    # Return the reranking scores
    return cross_rerank_scores
