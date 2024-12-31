import chromadb
from chromadb.utils import embedding_functions
import pandas as pd
from typing import Dict
from typing import Any



def initialize_cache_chromadb(chromadb_name: str, 
                            db_path: str) -> chromadb.Collection:
    """
    Initializes and returns a ChromaDB collection to store cached data.

    This function creates a ChromaDB client and initializes (or retrieves) a collection 
    for caching, using the provided name and embedding function.

    Args:
        chromadb_name (str): The name of the ChromaDB collection to use for caching.
        db_path (str): The path to the ChromaDB database.

    Returns:
        chromadb.Collection: The ChromaDB collection created or retrieved for caching purposes.
    """
    
    # Initialize the embedding function
    embeddings_fu = embedding_functions.DefaultEmbeddingFunction()

    # Initialize the ChromaDB client
    client = chromadb.PersistentClient(path=db_path)

    # Get or create the cache collection
    cache_collection = client.get_or_create_collection(
        name=chromadb_name,
        embedding_function=embeddings_fu
    )

    return cache_collection





def generate_cache_initialized_dataframe(query: str,
                                        threshold: float,
                                        cache_query_results: Dict[str, Any],
                                        chromadb_obj: Any,
                                        cache_collector_obj: Any
                                        ) -> pd.DataFrame:
    """
    Generates a DataFrame based on whether the query results are found in cache or need to be fetched 
    from the main ChromaDB collection.

    This function first checks if the cached results meet a given threshold. If not, it queries the 
    main ChromaDB collection, stores the results in the cache, and returns a DataFrame. If the 
    cached results meet the threshold, it returns the cached data.

    Args:
        query (str): The query string to search for.
        threshold (float): The threshold distance to determine if cached results are acceptable.
        cache_query_results (dict): Cached query results with distances, documents, and metadata.
        chromadb_obj (Any): The main ChromaDB object for querying.
        cache_collector_obj (Any): The ChromaDB object used to store cache results.

    Returns:
        pd.DataFrame: A DataFrame containing the top 10 results, including metadata, documents, 
                      distances, and IDs.
    """
    
    # Initialize lists to store results
    ids = []
    documents = []
    distances = []
    metadatas = []
    
    # Create an empty DataFrame to hold the results
    results_df = pd.DataFrame()

    # Check if the cache results are empty or don't meet the threshold
    if cache_query_results["distances"][0] == [] or cache_query_results['distances'][0][0] > threshold:
        # Query the main ChromaDB collection if cache results are not suitable
        results = chromadb_obj.query(
            query_texts=query,
            n_results=10
        )

        # Add results to cache if they are not found in cache
        keys = []
        values = []
        for key, val in results.items():
            if val is None:
                continue
            for i in range(10):
                keys.append(f"{key}{i}")
                values.append(f"{val}{i}")

        # Store the query and its results in the cache
        cache_collector_obj.add(
            documents=[query],
            ids=[query],  # Use the query string as the ID or integer IDs can be assigned
            metadatas=dict(zip(keys, values))
        )

        print("Not found in cache. Found in main collections")

        # Create a DataFrame with the results
        result_dict = {
            "Metadatas": results["metadatas"][0],
            "Documents": results["documents"][0],
            "Distances": results["distances"][0],
            "IDs": results["ids"][0]
        }
        results_df = pd.DataFrame(result_dict)

    # If the cached result's distance is below the threshold, use cache data
    elif cache_query_results['distances'][0][0] <= threshold:
        cache_result_dict = cache_query_results["metadatas"][0][0]

        # Extract data from the cache result dictionary
        for key, val in cache_result_dict.items():
            if "ids" in key:
                ids.append(val)
            elif "documents" in key:
                documents.append(val)
            elif "distances" in key:
                distances.append(val)
            else:
                metadatas.append(val)

        print("Found in cache!")

        # Create a DataFrame with the cache results
        result_dict = {
            "Metadatas": metadatas,
            "Documents": documents,
            "Distances": distances,
            "IDs": ids
        }
        results_df = pd.DataFrame(result_dict)

    # Return the DataFrame with the top 10 results
    return results_df






