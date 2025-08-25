
from dotenv import load_dotenv
load_dotenv()

from get_data import get_state_of_union_addresses
from prepare_data import prepare_data
from load import load_index

# gather the state of the union addresses from Obama and Trump
results = get_state_of_union_addresses(['Obama', 'Trump'])
print(len(results), "results found")

# now we want to prepare the data for storage to Azure Search Index
results = prepare_data(results)
print(len(results), "prepared results ready")

# now add to the index
load_index(results)
print("Data loaded to Azure Search Index successfully.")