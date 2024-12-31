import pandas as pd
from typing import Tuple

def top_3_relevant_documents(
    cross_rerank_scores: list[float], 
    result_df: pd.DataFrame
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Reranks the documents in the DataFrame based on the provided rerank scores and returns the top 3 most relevant documents.

    The function expects the DataFrame to have two columns: 'Documents' and 'Metadatas'. If these columns
    are missing or incorrectly named, an error is raised.

    Args:
        cross_rerank_scores (list[float]): A list of reranking scores corresponding to each document in the DataFrame.
        result_df (pd.DataFrame): A pandas DataFrame containing at least two columns:
                                  'Documents' and 'Metadatas' for the documents and their metadata.

    Returns:
        Tuple[pd.DataFrame, pd.DataFrame]:
            - A DataFrame containing the top 3 most relevant documents and their metadata.
            - A DataFrame containing all the documents sorted by their reranked scores.
    
    Raises:
        ValueError: If the DataFrame does not have the required columns ('Documents' and 'Metadatas').
    """
    
    # Ensure the DataFrame contains the required columns
    if 'Documents' not in result_df.columns or 'Metadatas' not in result_df.columns:
        raise ValueError("The DataFrame must contain 'Documents' and 'Metadatas' columns.")

    # Store the rerank scores in the DataFrame
    result_df['Reranked_scores'] = cross_rerank_scores

    # Sort the DataFrame by rerank scores in descending order
    reranker_df = result_df.sort_values(by='Reranked_scores', ascending=False)

    # Return the top 3 documents along with their metadata
    top_3_RAG = reranker_df[["Documents", "Metadatas"]].head(3)

    return top_3_RAG, reranker_df