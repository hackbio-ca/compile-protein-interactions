from indra.sources import trips
import pandas as pd
import json
import re
import spacy
import scispacy
import requests
import xml.etree.ElementTree as ET
import json

def find_key_sentences(abstract, ppi_terms):

    if "protein" in abstract:

        # Find sentences containing any PPI keyword
        sentences = re.split(r'(?<=[.!?])\s+', abstract)
        matched_sentences = [
            sentence for sentence in sentences
            if re.search(r"\b(" + "|".join(ppi_terms) + r")\b", sentence, re.IGNORECASE)
        ]
        
        return matched_sentences
    
# Read abstract data
with open('pmid_to_abstract_updated.json', 'r') as f:
    data = json.load(f)

# Load model
nlp = spacy.load("en_ner_jnlpba_md")


ids=["40973402", 
     "40973401", 
     "40966293",
     "40915373",
     "40587559",
     "40913132",
     "40758965",
     "40752663",
     "40742404",
     "40721030",
     "40713730",
     "40707822",
     "40448625",
     "40358171",
     "40347153",
     "40340056",
     "40296620",
     "39695808",
     "39680531"
]

# Removed
    #  "40676669",
    #  "40927314",
    #  "40551140",
    #  "40818508",
    #  "40815569",
    #  "40441521",
    #  "40373772",
    #  "40362335",
    #  "40247363",
    #  "40223243",
    #  "40212965",
    #  "40205047",
    #  "40183841",
    #  "40176187",
    #  "40175501",
    #  "40131356",
#      "40301248",
#      "40318722",
#      "40337095",
#      "40337551",
    #  "40081988"]

cells_pmid = []

f = open('data_new.csv','w')

for id in ids:
    
    # Run Relation Extraction
    ppi_terms = ["binds", "associates with", "interacts with", "activates", "inhibits", "interact with", "strong binding"]
    key_sentences = find_key_sentences(data[id], ppi_terms)

    if not key_sentences:
        print("Couldn't find any key sentences")
        continue
    else:
        print(key_sentences)

    for s in key_sentences:
        tp = trips.process_text(s)

        # Find first protein interaction
        if tp.statements:

            interactions = [str(i) for i in tp.statements]
            print(tp.statements)
            break

        else:
            interactions=[]


    if not interactions:
        # Didn't find any protein-protein interactions
        print("Couldn't find any ppis")
        continue

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

    # Run NER
    abstract = data[id]
    doc = nlp(abstract)
    entity_types = ['CELL_LINE', 'CELL_TYPE']
    unique_cells = set() # unique cell names

    for ent in doc.ents:
        if ent.label_ in entity_types:

            cell_name = ent.text

            # Make lowercase and replace space with underscore
            cell_name_clean = cell_name.lower().replace(" ", "_")

            # If you found a new cell for ppi, add; otherwise, discard
            if cell_name_clean not in unique_cells:
                
                unique_cells.add(cell_name_clean)
                hypernode = f'{protein_a}-{protein_b}-{id}'
                f.write(f'{protein_a},{protein_b}, {key_sentences[0]}, {cell_name_clean},{id},{hypernode}\n') 


f.close()