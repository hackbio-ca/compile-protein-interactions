import spacy
import scispacy
import requests
import xml.etree.ElementTree as ET
import json

# Read abstract data
with open('pmid_to_abstract_updated.json', 'r') as f:
    data = json.load(f)

# Load model
nlp = spacy.load("en_ner_jnlpba_md")
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

cells_pmid = []
# label = dict.fromkeys(ids)
unique_cells = {} # unique cell names

f = open('cells_to_pmid.csv','w')

for id in ids:
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

            f.write(f'{cell_name_clean}, {id}\n') 

f.close()

# print(cells_pmid)
# cells_pmid.append((cell_name_clean, id))
# label[id] = [(ent.label_ , ent.text) for ent in doc.ents if ent.label_ in entity_types]
# print(label)

# cell, pmid
# make lowercase
# replace space with underscore
# find and keep unique types
# each unique cell gets a unique ID

# for id in ids:

#     print(id)
#     abstract = get_abstract(str(id))
#     print(abstract)
#     doc = nlp(abstract)
#     print([(ent.text, ent.label_) for ent in doc.ents])

# # abstract = "The Keap1-Nrf2 pathway has been established as a therapeutic target for Alzheimer's disease (AD). Directly inhibiting the protein-protein interaction (PPI) between Keap1 and Nrf2 has been reported as an effective strategy for treating AD. Our group has validated this in an AD mouse model for the first time using the inhibitor 1,4-diaminonaphthalene NXPZ-2 with high concentrations. In the present study, we reported a new phosphodiester containing diaminonaphthalene compound, POZL, designed to target the PPI interface using a structure-based design strategy to combat oxidative stress in AD pathogenesis. Our crystallographic verification confirms that POZL shows potent Keap1-Nrf2 inhibition. Remarkably, POZL showed its high in vivo anti-AD efficacy at a much lower dosage compared to NXPZ-2 in the transgenic APP/PS1 AD mouse model. POZL treatment in the transgenic mice could effectively ameliorate learning and memory dysfunction by promoting the Nrf2 nuclear translocation. As a result, the oxidative stress and AD biomarker expression such as BACE1 and hyperphosphorylation of Tau were significantly reduced, and the synaptic function was recovered. HE and Nissl staining confirmed that POZL improved brain tissue pathological changes by enhancing neuron quantity and function. Furthermore, it was confirmed that POZL could effectively reverse Aβ-caused synaptic damage by activating Nrf2 in primary cultured cortical neurons. Collectively, our findings demonstrated that the phosphodiester diaminonaphthalene Keap1-Nrf2 PPI inhibitor could be regarded as a promising preclinical candidate of AD."
# # doc = nlp("Primary human astrocytes were co-cultured with HeLa cells.")

# doc = nlp(abstract)

# # print(f'{[(ent.text, ent.label_) for ent in doc.ents]}')

# def get_abstract(pmid: str) -> str:
#     url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
#     params = {
#         "db": "pubmed",
#         "id": pmid,
#         "retmode": "xml"
#     }
#     resp = requests.get(url, params=params)
    
#     root = ET.fromstring(resp.text)
#     abstract_texts = root.findall(".//AbstractText")
    
#     abstract = " ".join([t.text for t in abstract_texts if t.text])
#     return abstract.strip()

# abstract = get_abstract("40912354")
# ids = ["40910579", "40915260"]