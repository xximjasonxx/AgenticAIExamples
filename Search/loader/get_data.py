
import requests
from typing import List

def get_state_of_union_addresses(speakers: List[str]) -> List[dict]:
    endpoint = "https://api.millercenter.org/speeches"
    results = []

    r = requests.post(url=endpoint)
    data = r.json()

    while 'LastEvaluatedKey' in data:
      for item in data['Items']:
        if (
          any(speaker in item['president'] for speaker in speakers)
          and 'State of the Union Address' in item.get('title', '')
        ):
          results.append(item)

      parameters = {"LastEvaluatedKey": data['LastEvaluatedKey']['doc_name']}
      r = requests.post(url = endpoint, params = parameters)
      data = r.json()
    
    # Process the final batch of data
    for item in data['Items']:
      if (
        any(speaker in item['president'] for speaker in speakers)
        and 'State of the Union Address' in item.get('title', '')
      ):
        results.append(item)
    
    return results