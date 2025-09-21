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
ids=["40973402"]#, 
    #  "40973401", 
    #  "40966293",
    #  "40676669",
    #  "40927314",
    #  "40915373",
    #  "40587559",
    #  "40913132",
    #  "40551140",
    #  "40818508",
    #  "40815569",
    #  "40758965"]

cells_pmid = []
unique_cells = {} # unique cell names

f = open('data.csv','w')

for id in ids:
    
    # Run Relation Extraction
    ppi_terms = ["binds", "associates with", "interacts with", "activates", "inhibits", "interact with"]
    key_sentences = find_key_sentences(data[id], ppi_terms)

    if not key_sentences: # if list is empty
        tp = trips.process_text(data[id])
        print(tp.statements)
    else:
        for s in key_sentences:
            tp = trips.process_text(s)
            print(tp.statements)

    interactions = [str(i) for i in tp.statements]

    # f = open('test_protein_to_hypernode.csv','w')

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

        # f.write(f'{protein_a}, {hypernode}\n') 
        # f.write(f'{protein_b}, {hypernode}\n')


    # Run NER
    abstract = data[id]
    doc = nlp(abstract)
    entity_types = ['CELL_LINE', 'CELL_TYPE']

    for ent in doc.ents:
        if ent.label_ in entity_types:

            cell_name = ent.text

            # Make lowercase and replace space with underscore
            cell_name_clean = cell_name.lower().replace(" ", "_")

            if cell_name_clean in unique_cells:
                unique_cells.add(cell_name_clean)

            # f.write(f'{cell_name_clean}, {id}\n') 


f.close()