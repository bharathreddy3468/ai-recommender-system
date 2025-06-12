# 🎥 AI-Powered Anime Recommender System 🎯

A generative AI-based hybrid recommender system that uses **LLMs**, **Neo4j graph database**, and **LangChain** to generate intelligent, context-aware anime recommendations.

---

## 📌 Overview

This project combines the power of **large language models (LLMs)** and **graph-based data modeling** to dynamically generate personalized anime recommendations from user input. It leverages **Neo4j** for relationship-rich data storage, and **Google Cloud Platform (GCP)** for scalable deployment using **CI/CD pipelines**.

---

## 🧠 Key Features

- 🧩 Uses **Neo4j** to model users and animes as graph nodes with ratings as relationships
- 🧠 Employs two **LLMs**:
  - **Gemma 9B**: Understands user interests and generates a recommendation strategy
  - **LLaMA 70B**: Translates the strategy into executable **Cypher queries**
- 🔗 Powered by **LangChain Expression Language (LCEL)** to chain the LLMs
- 🖥️ Clean and simple frontend built with **HTML/CSS/JavaScript**
- ☁️ Deployed serverlessly via **Docker**, **Cloud Run**, **Cloud Build**, and **Cloud Deploy**

---

## 🗂️ Tech Stack

| Component      | Tools/Frameworks |
|----------------|------------------|
| Backend        | Python, Flask     |
| LLMs           | Google Gemma 9B, Meta LLaMA 70B |
| LangChain      | LCEL              |
| Database       | Neo4j, Cypher     |
| Frontend       | HTML, CSS, JavaScript |
| Deployment     | Docker, GCP (Cloud Run, Cloud Build, Cloud Deploy) |
| DevOps         | GitHub (CI/CD)    |

---

## 🔧 System Architecture

User Input

   ↓
   
Gemma 9B → User Interest + Strategy

   ↓
   
LLaMA 70B → Generates Cypher Query

   ↓
   
Neo4j → Fetch Anime Recommendations

   ↓
   
Frontend UI → Displays Results



## Clone the repo:
git clone https://github.com/yourusername/anime-recommender-ai.git

cd anime-recommender-ai

## Install dependencies
pip install -r requirements.txt

## create a .env file with
NEO4J_URI=URI to your database

NEO4J_USER=username

NEO4J_PASSWORD=your_password

GROQ_API_KEY=your_key

LANGCHAIN_API_KEY=your_key

## run the project
python3 run main.py

## PRoject structure

anime-recommender-ai/

├── anime.ipynb - data preprocessing and merging the datasets

├── app.py - llms and prompts

├── main.py - flask app

├── database.py - connect with neo4j database and querying

├── src/index.html - UI

├── Dockerfile - dockerfile for docker image

├── cloudbuild.yaml - configuration for automated CICD

└── README.md


## sample query
User input: "I like fantasy and adventure anime with strong character development"

Gemma 9B → Strategy: recommend action-fantasy anime based on popularity and rating

LLaMA 70B → Cypher: MATCH ... RETURN anime.name LIMIT 10

## Future Improvements
    Add user authentication and session-based recommendations
    Incorporate feedback loop for active learning
    Add vector-based semantic search using embeddings
