import os
import json

from typing import List
from openai import AzureOpenAI

client = AzureOpenAI(
    api_version="2024-12-01-preview",
      azure_endpoint=os.environ["AZURE_FOUNDRY_ENDPOINT"],
    api_key=os.environ["AZURE_FOUNDRY_API_KEY"],
)

def get_keywords(text: str) -> List[str]:
    try:
        response = client.chat.completions.create(
          model="gpt-4.1-mini-deployment",
          messages=[
            {
              "role": "user",
              "content": f"""
              Given the following text, extract at most three keywords.
              Each keyword should be a single word with no spaces.
              Focus on legal, policy, or societal issues that are implied or discussed.
              Avoid using graphic, violent, or emotionally charged terms in the output or do not return keywords for these concepts.
              If no suitable keywords are found, return [].
              Return only the entries in JSON array format.

              {text}
              """
            }
          ]
        )
    except Exception as e:
      print(text)
      raise

    # Process the response to extract keywords
    raw_content = response.choices[0].message.content
    if raw_content is None:
        return []
    try:
        keywords = json.loads(raw_content)
        if isinstance(keywords, list):
            return [str(k) for k in keywords]
        else:
            return []
    except Exception:
        return []
