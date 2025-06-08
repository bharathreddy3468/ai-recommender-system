import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableMap

groq_api_key = os.getenv("GROQ_API_KEY")

llm1 = ChatGroq(groq_api_key=groq_api_key,model_name="gemma2-9b-it")
llm2=ChatGroq(groq_api_key=groq_api_key,model_name="Llama3-70b-8192")

prompt_template1 = """
You are an expert in anime recommendation systems and Neo4j graph databases. Your task is to deeply understand the user query and design a **single best hybrid recommendation approach** using a combination of:
- Content-based filtering (e.g., genres, type)
- Collaborative filtering (e.g., user behavior)
- Property-based similarity (e.g., shared attributes)

You must first **internally consider multiple possible approaches** to answer the query effectively, then select and return **only the most relevant and optimized strategy**. 

Use the format and structure of the examples below to guide your thinking.

---
Your final output must:
- Include **only** the selected best hybrid approach (no explanations or alternatives).
- Follow the format: `approach: ...`
- Be concise, relevant, and implementable.
---

**Examples**

Example 1:
user input: I like action and comedy  
approach: Find the top 10 animes by average rating where Genres contain action or comedy

Example 2:
user input: user id 7  
approach: -> Find the animes that are rated >= 8 by this user.  
          -> Then find the animes that are related to those animes using properties.  
          -> Find the users who also rated the same animes as this user. Then get the animes rated by related users  
             which are not rated by the given user.

Example 3:
user input: name of the anime : Inyouchuu The Animation  
approach: Find the users who rated this anime highly and return other animes that are also highly rated by those similar users.

---

user input: {user_query}
"""

prompt_template2 = """
You are an expert Cypher query writer working with a Neo4j graph database containing anime and user nodes. 
You will be given a recommendation approach in English. Your task is to read the **entire input carefully** 
and generate a **syntactically correct, logically sound, and optimized Cypher query**.

### Database Schema:
- Nodes:
    - (:anime) → properties: Name (String), Genres (List<String>), Type (String)
    - (:user) → properties: user_id (Integer)
- Relationships:
    - (:user)-[:rated]->(:anime)

### Query Requirements:
1. Use **lowercase labels and properties** exactly as shown above (e.g., `a:anime`, `u:user`, `a.Genres`, etc.).
2. Do not use ambiguous variable names. Use clear aliases like `a` for anime, `u` for user, `r` for rating.
3. Always **alias return values** using `AS` for readability.
4. Use `CONTAINS` for checking substring or tag matches in lists (e.g., genres).
5. When using multiple `WITH` clauses, **always pass forward all variables needed later**.
6. Ensure **`toFloat()` is used** for numeric division to avoid integer errors.
7. If averaging ratings or filtering by rating counts, ensure filters are logically ordered.
8. Limit the result to max 20 records

### Examples:

**Example 1**  
Approach: Find the top 10 animes by average rating where Genres contain action or comedy  
Cypher:  
```cypher
MATCH (a:anime)<-[r:rated]-()
WHERE a.Genres CONTAINS "Action" OR a.Genres CONTAINS "Comedy"
WITH a, AVG(r.rating) AS avg_rating, COUNT(r) AS rating_count
WHERE rating_count >= 100
RETURN a.Name AS Name, a.Genres AS Genres, a.Type AS Type, 
       ROUND(avg_rating, 2) AS AvgRating, rating_count
ORDER BY AvgRating DESC
LIMIT 10

approach : {approach}
"""


# Create LangChain prompt templates
strategy_prompt = PromptTemplate.from_template(template=prompt_template1)
cypher_prompt = PromptTemplate.from_template(template=prompt_template2)

# Define chains
strategy_chain = strategy_prompt | llm1 | StrOutputParser()
cypher_chain = cypher_prompt | llm2 | StrOutputParser()

# Combine into a sequential chain
full_chain = (
    RunnablePassthrough()
    | RunnableMap({"approach": lambda x: strategy_chain.invoke({"user_query": x["user_query"]})})
    | RunnableMap({"cypher": lambda x: cypher_chain.invoke({"approach": x["approach"]})})
)

# Function to generate cypher query
def generate_response(user_query):
    # Step 1: Generate strategy
    strategy = strategy_chain.invoke({"user_query": user_query})
    print("\n🔍 Strategy from LLM1:\n", strategy)  # Show in console

    # Step 2: Generate Cypher
    cypher_output = cypher_chain.invoke({"approach": strategy.strip()})

    print('\n cypher query \n', cypher_output)

    # Extract only the Cypher query block if wrapped in markdown
    import re
    match = re.search(r"```(?:cypher)?\n(.*?)```", cypher_output, re.DOTALL)
    if match:
        cypher_query = match.group(1).strip()
    else:
        # fallback: return full response if no fenced block
        cypher_query = cypher_output.strip()
    

    return cypher_query
# Example use
# query = "I watched Fullmetal Alchemist: Brotherhood"

# final_query = generate_response(query)

# print("\n✅ Final Cypher Query:\n", final_query)

# records = database(final_query)


# print('\n final result \n', [i['Name'] for i in records])