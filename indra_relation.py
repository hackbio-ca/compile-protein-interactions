from indra.sources import trips
import pandas as pd
import json
import re

# Open the JSON file in read mode
with open('pmid_to_abstract_updated.json', 'r') as file:
    data = json.load(file)

# 2m 8.5s
# abs0 = list(data.values())[0] # Grab first value in dict
# abs0_tp = trips.process_text(abs0)
# abs0_tp.extracted_events
# abs0_tp.statements

ids=["40973402", 
     "40973401", 
     "40966293",
     "40676669",
     "40927314",
     "40915373",
     "40587559",
     "40913132",
     "40551140",
     "40818508",
     "40815569",
     "40758965"]

# print(data[ids[0]])
ppi_terms = ["binds", "associates with", "interacts with", "activates", "inhibits", "interact with"]

def find_key_sentences(abstract, ppi_terms):

    if "protein" in abstract:
        # Find sentences containing any PPI keyword
        sentences = re.split(r'(?<=[.!?])\s+', abstract)
        matched_sentences = [
            sentence for sentence in sentences
            if re.search(r"\b(" + "|".join(ppi_terms) + r")\b", sentence, re.IGNORECASE)
        ]

        return matched_sentences

id = "40973402"
key_sentences = find_key_sentences(data[id], ppi_terms)

# print(data[ids[1]])
# print(key_sentences)

if not key_sentences: # if list is empty
    tp = trips.process_text(data[id])
    print(tp.statements)
else:
    for s in key_sentences:
        tp = trips.process_text(s)
        print(tp.statements)

interactions = [str(i) for i in tp.statements]

f = open('test_protein_to_hypernode.csv','w')

# Get protein a and protein b of each interaction
for i in interactions:
    a_start = i.find('(')
    a_end = i.find('(', a_start + 1) 

    b_start = i.find(',')
    b_end = i.find('(', b_start+1)

    protein_a = i[a_start+1:a_end] 
    protein_b = i[b_start+2:b_end]

    protein_a = protein_a.lower()
    protein_b = protein_b.lower()

    print(f'A: {protein_a} B:{protein_b}')

    hypernode = f'{protein_a}-{protein_b}-{id}'

    f.write(f'{protein_a}, {hypernode}\n') 
    f.write(f'{protein_b}, {hypernode}\n')

f.close()


# text = 'The extracellular Tau oligomers were found to interact with microglial purinergic receptor P2Y12 which then led to microglial migration, activation and phagocytosis via various remodeled actin structure.'
# tp = trips.process_text(text)
# print(tp.statements)
# tp = trips.process_text(data[ids[0]])
# print(tp.statements)

# print(abs0_tp.statements)

# 11.9s
# sentence = "Tafamidis inhibits the breast cancer resistance protein (BCRP), raising concern for drug-drug interactions, particularly with rosuvastatin."
# sen_tp = trips.process_text(sentence)
# sen_tp.statements