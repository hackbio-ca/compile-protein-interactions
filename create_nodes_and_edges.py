import pandas as pd

# Read in CSV file
csv = "/Users/pamalamilla/Desktop/data_new.csv"
df = pd.read_csv(csv, header = None)

# Assign column names
df.columns = ["proteinAName", "proteinBName", "sentence", "cellType", "pmid", "ppiId"]

# Make protein nodes
df["proteinAName"] = df["proteinAName"].str.replace('"','') # Fix: remove double quotations
df["proteinAName"] = (df["proteinAName"].str.strip()) # Fix: Remove blank spaces
proteins_uniq_df = pd.concat([df["proteinAName"], df["proteinBName"]])
proteins_uniq_df.drop_duplicates(inplace=True)
proteins_uniq_df.to_csv("./files_for_graph/protein_nodes.csv",
                        header=["proteinName"], 
                        index= False)

# Make cell nodes
cells_uniq_df = df["cellType"].drop_duplicates()
cells_uniq_df.to_csv("./files_for_graph/cell_nodes.csv", 
                     header=["cellType"], 
                     index= False)

# Make paper nodes
papers_uniq_df = df[["pmid","sentence"]]
papers_uniq_df.to_csv("./files_for_graph/paper_nodes.csv", 
                      header=["pmid", "sentence"],
                      index= False)

# Make PPI nodes
ppis_uniq_df = df["ppiId"].drop_duplicates()
ppis_uniq_df.to_csv("./files_for_graph/ppi_nodes.csv", 
                    header=["ppiId"],
                    index= False)

# Make protein-to-PPI edges
protein_ppi_df_1 = df[["proteinAName","ppiId"]]
protein_ppi_df_1.columns= ["protein","ppiId"] # Rename columns

protein_ppi_df_2 = df[["proteinBName","ppiId"]]
protein_ppi_df_2.columns= ["protein","ppiId"] # Rename columns

protein_ppi_df = pd.concat([protein_ppi_df_1, protein_ppi_df_2], ignore_index=True)
protein_ppi_df.drop_duplicates(inplace= True)
protein_ppi_df.to_csv("./files_for_graph/protein_ppi_edges.csv", 
                      header=["proteinName","ppiId"],
                      index= False)

# Make PPI-to-cell edges
ppi_cell_df = df[["ppiId", "cellType"]].drop_duplicates()
ppi_cell_df.to_csv("./files_for_graph/ppi_cell_edges.csv", 
                   header=["ppiId", "cellType"],
                   index= False)

# Make PPI-to-paper edges
ppi_paper_df = df[["ppiId", "pmid"]].drop_duplicates()
ppi_paper_df.to_csv("./files_for_graph/ppi_paper_edges.csv", 
                    header=["ppiId", "pmid"],
                    index= False)
