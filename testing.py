from neo4j import GraphDatabase

# Neo4j AuraDB connection
URI = "neo4j+s://1e571eb8.databases.neo4j.io"
USERNAME = "1e571eb8"
PASSWORD = "WGKngG-v3kxygx6oNyLUoT9JbP1ep4wTbcvcvmTqV5o"

# Connect and verify
with GraphDatabase.driver(URI, auth=(USERNAME, PASSWORD)) as driver:
    try:
        driver.verify_connectivity()
        print("✅ Connected to Neo4j successfully!")
    except Exception as e:
        print("❌ Connection failed:", e)
