# Abstract
Protein-protein interactions (PPIs) are often highly specific to the conditions in which they occur, including cell type, development stage, and disease state. However, most large PPI databases remain agnostic to these key nuances, reporting interactions without indicating the biological context. This gap limits researchers' ability to understand how molecular networks very across biological systems. Much of this context-specific information resides in the scientific literature, where it is difficult to access at scale. Natural language processing (NLP) offers a powerful solution by mining PPIs directly from publications while retaining the surrounding contextual information, such as the cell type in which the interaction was observed.

Our project, COMPILE (Context-aware Mapping of Protein Interactions from Literature Evidence), will develop a user-friendly web platform to make this information accessible. Using context-aware NLP pipelines, we will extract protein-protein interactions from the literature, annotate them with detailed biological context, and link each interaction to the exact supporting sentence in the source paper. The results will be stored in an interactive knowledge graph, where proteins are nodes, interactions are edges, and contextual attributes are embedded as metadata. By combining literature mining with rich graphical visualization, COMPILE will allow researchers to easily identify PPIs relevant to their biological system of interest and explore protein networks across different cellular contexts. This tool will bridge the gap between unstructured text and actionable, evidence-linked PPI data, accelerating hypothesis generation in molecular biology.

## Environment Setup

```js

python3.12 -m venv env
source env/bin/activate

pip install scispacy
pip install spacy
pip install re
pip install neo4j
pip install indra
pip install \ https://s3-us-west-2.amazonaws.com/ai2-s2-scispacy/releases/v0.5.4/en_ner_jnlpba_md-0.5.4.tar.gz


```



