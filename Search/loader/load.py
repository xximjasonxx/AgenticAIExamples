
from typing import List
import os
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

search_client = SearchClient(
    endpoint=os.environ["AZURE_SEARCH_ENDPOINT"],
    index_name="sotu-trump-obama-v1",
    credential=AzureKeyCredential(os.environ["AZURE_SEARCH_ADMIN_KEY"])
)

def load_index(results: List[dict]) -> None:
    for doc in results:
        search_client.upload_documents(documents=[doc])