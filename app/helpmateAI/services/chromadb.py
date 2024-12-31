
import chromadb
from chromadb.utils import embedding_functions
from pandas import DataFrame




def create_and_store_chromadb_data(
    chromadb_name: str, 
    db_path: str, 
    dataframe: DataFrame
    ) -> chromadb.Collection:
    """
    Creates a ChromaDB collection and stores data from a given pandas DataFrame.

    This function initializes a ChromaDB client, creates a collection (if it doesn't already exist), 
    and adds documents, metadata, and unique IDs from the provided DataFrame to the collection.

    Args:
        chromadb_name (str): The name of the ChromaDB collection.
        db_path (str): The path to the ChromaDB database.
        dataframe (DataFrame): A pandas DataFrame containing the data to be stored in the ChromaDB collection.
                               It should have at least two columns: 'metadata' and 'page_context'.

    Returns:
        chromadb.Collection: The created ChromaDB collection containing the documents and metadata.
    """
    
    # Initialize the embedding function
    embeddings_fu = embedding_functions.DefaultEmbeddingFunction()

    # Initialize the ChromaDB client
    client = chromadb.PersistentClient(path=db_path)

    # Get or create the collection
    collection = client.get_or_create_collection(name=chromadb_name, embedding_function=embeddings_fu)

    # Generate unique IDs for each document
    ids = [f"ids-{i}" for i in range(len(dataframe))]

    # Extract metadata and documents from the dataframe
    metadata_list = dataframe["metadata"].tolist()
    documents_list = dataframe["page_context"].tolist()

    # Add documents, metadata, and IDs to the collection
    collection.add(
        documents=documents_list,
        metadatas=metadata_list,
        ids=ids
    )

    return collection

