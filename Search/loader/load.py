
from typing import List
import os
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

search_client = SearchClient(
    endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
    index_name="sotu-trump-obama-v3",
    credential=AzureKeyCredential(os.environ["AZURE_SEARCH_ADMIN_KEY"])
)

def load_index(results: List[dict]) -> None:
    batch_size = 200
    
    # Process documents in batches of 200
    for i in range(0, len(results), batch_size):
        batch = results[i:i + batch_size]
        search_client.upload_documents(documents=batch)
        print(f"Uploaded batch {i//batch_size + 1}: {len(batch)} documents")