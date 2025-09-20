# connections.py
import os
from neo4j import GraphDatabase

# Load credentials from environment variables
URI = os.getenv("NEO4J_URI")
USERNAME = os.getenv("NEO4J_USERNAME")
PASSWORD = os.getenv("NEO4J_PASSWORD")

if not all([URI, USERNAME, PASSWORD]):
    raise Exception("Please set NEO4J_URI, NEO4J_USERNAME, and NEO4J_PASSWORD environment variables.")

# Connect to Neo4j
driver = GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD))

def test_connection():
    with driver.session() as session:
        result = session.run("RETURN 'Connection Successful!' AS msg")
        for record in result:
            print(record["msg"])

if __name__ == "__main__":
    test_connection()

