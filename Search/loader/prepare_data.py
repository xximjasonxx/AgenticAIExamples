
import uuid
from typing import List
from llm import get_keywords, get_embedding

def prepare_data(results: List[dict]) -> List[dict]:
    chunked_results = []

    # we need to go through each result entry
    # extract the doc_name, date, title, president
    # for transcript we need to chunk it with each size being 300 with a 50 character overlap
    # add each entry with its respective chunk to the results array
    for item in results:
      doc_name = item.get("doc_name", "")
      date = item.get("date", "")
      title = item.get("title", "")
      president = item.get("president", "")
      transcript = item.get("transcript", "")

      title_embedding = get_embedding(title) if title else []
      president_embedding = get_embedding(president) if president else []

      # Chunk the transcript
      chunks = [transcript[i:i + 300] for i in range(0, len(transcript), 300)]
      for chunk_index, chunk in enumerate(chunks):
        # generate keywords
        keywords = get_keywords(chunk)
        chunk_text_embedding = get_embedding(chunk) if chunk else []

        # Generate unique ID using doc_name and chunk_index
        id_string = f"{doc_name}_chunk_{chunk_index}"
        
        chunked_results.append({
          "id": str(uuid.uuid5(uuid.NAMESPACE_DNS, id_string)),
          "doc_name": doc_name,
          "date": date,
          "title": title,
          "title_embedding": title_embedding,
          "president": president,
          "president_embedding": president_embedding,
          "chunk_text": chunk,
          "chunk_text_embedding": chunk_text_embedding,
          "chunk_keywords": keywords
        })
    
    # Return the prepared data
    return chunked_results
   