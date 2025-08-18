
from typing import List
import uuid

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

      # Chunk the transcript
      chunks = [transcript[i:i + 300] for i in range(0, len(transcript), 300)]
      for chunk in chunks:
        chunked_results.append({
          "id": str(uuid.uuid5(uuid.NAMESPACE_DNS, doc_name)),
          "doc_name": doc_name,
          "date": date,
          "title": title,
          "president": president,
          "chunk_text": chunk
        })
    
    # Return the prepared data
    return chunked_results