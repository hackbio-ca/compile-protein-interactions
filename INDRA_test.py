from indra.sources import trips
import pandas as pd
import json

# Open the JSON file in read mode
with open('/Users/pamalamilla/Desktop/pmid_to_abstract.json', 'r') as file:
    # Load the JSON data into a Python dictionary
    data = json.load(file)

# 2m 8.5s
abs0 = list(data.values())[0] # Grab first value in dict
abs0_tp = trips.process_text(abs0)
abs0_tp.extracted_events
abs0_tp.statements

# 11.9s
sentence = "Tafamidis inhibits the breast cancer resistance protein (BCRP), raising concern for drug-drug interactions, particularly with rosuvastatin."
sen_tp = trips.process_text(sentence)
sen_tp.statements