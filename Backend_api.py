from fastapi import FastAPI, UploadFile, File, Query
import csv, re, requests
from neo4j import GraphDatabase
from io import StringIO

# ---------------- Neo4j Setup ----------------
URI = "neo4j+s://1e571eb8.databases.neo4j.io"
AUTH = ("neo4j", "WGKngG-v3kxygx6oNyLUoT9JbP1ep4wTbcvcvmTqV5o")
driver = GraphDatabase.driver(URI, auth=AUTH)

# ---------------- PPI Keywords ----------------
PPI_TERMS = ["binds", "associates with", "interacts with", "activates", "inhibits"]

def find_key_sentences(abstract: str):
    if "protein" not in abstract.lower():
        return []
    sentences = re.split(r'(?<=[.!?])\s+', abstract)
    return [
        s for s in sentences
        if re.search(r"\b(" + "|".join(PPI_TERMS) + r")\b", s, re.IGNORECASE)
    ]

def process_row(row):
    protein_ids = [row["proteinA"], row["proteinB"]]
    abstract = row["abstract"]
    sentences = find_key_sentences(abstract) or [abstract]

    neo4j_entries = []
    for sentence in sentences:
        interaction_id = f"{protein_ids[0]}_{protein_ids[1]}_{abs(hash(sentence))}"
        neo4j_entries.append({
            "proteinA": protein_ids[0],
            "proteinB": protein_ids[1],
            "interaction": interaction_id,
            "sentence": sentence,
            "abstract": abstract
        })
    return neo4j_entries

# ---------------- FastAPI Setup ----------------
app = FastAPI(title="Protein Interaction API")

# -------- CSV Upload Endpoint --------
@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    contents = await file.read()
    decoded = contents.decode("utf-8").splitlines()
    reader = csv.DictReader(decoded)

    with driver.session() as session:
        for row in reader:
            entries = process_row(row)
            for e in entries:
                session.run("""
                MERGE (p1:Protein {id: $proteinA})
                MERGE (p2:Protein {id: $proteinB})
                CREATE (i:Interaction {id: $interaction})
                MERGE (s:Sentence {text: $sentence})
                MERGE (a:Abstract {text: $abstract})
                MERGE (p1)-[:PARTICIPANT]->(i)<-[:PARTICIPANT]-(p2)
                MERGE (i)-[:DESCRIBED_IN]->(s)-[:PART_OF]->(a)
                """, **e)

    return {"status": "✅ CSV uploaded and graph updated"}

# -------- Fetch CSV from URL Endpoint --------
@app.get("/fetch-data")
async def fetch_data(url: str = Query(..., description="URL to CSV file")):
    response = requests.get(url)
    response.raise_for_status()
    decoded = response.content.decode("utf-8").splitlines()
    reader = csv.DictReader(decoded)

    with driver.session() as session:
        for row in reader:
            entries = process_row(row)
            for e in entries:
                session.run("""
                MERGE (p1:Protein {id: $proteinA})
                MERGE (p2:Protein {id: $proteinB})
                CREATE (i:Interaction {id: $interaction})
                MERGE (s:Sentence {text: $sentence})
                MERGE (a:Abstract {text: $abstract})
                MERGE (p1)-[:PARTICIPANT]->(i)<-[:PARTICIPANT]-(p2)
                MERGE (i)-[:DESCRIBED_IN]->(s)-[:PART_OF]->(a)
                """, **e)

    return {"status": "✅ Data fetched and graph updated"}

# -------- Query PPI --------
@app.get("/ppi/{protein_id}")
async def get_ppi(protein_id: str):
    with driver.session() as session:
        results = session.run("""
        MATCH (p:Protein {id: $protein_id})-[:PARTICIPANT]->(i:Interaction)<-[:PARTICIPANT]-(other:Protein)
        OPTIONAL MATCH (i)-[:DESCRIBED_IN]->(s:Sentence)-[:PART_OF]->(a:Abstract)
        RETURN other.id AS interacting_protein, s.text AS sentence, a.text AS abstract
        """, protein_id=protein_id)

        interactions = []
        for record in results:
            interactions.append({
                "interacting_protein": record["interacting_protein"],
                "sentence": record["sentence"],
                "abstract": record["abstract"]
            })
    return {"protein": protein_id, "interactions": interactions}
