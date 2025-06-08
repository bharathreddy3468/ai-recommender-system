from neo4j import GraphDatabase
import os

# Replace with your actual Aura DB credentials
uri = "neo4j+s://54cfbb3b.databases.neo4j.io"
username = os.getenv("neo_username")
password = os.getenv("neo_password")

# Create the driver
driver = GraphDatabase.driver(uri, auth=(username, password))

def database(query, driver=driver):

    # Define a sample query function
    def get_results(tx):
        result = tx.run(query)
        return [record for record in result]

    # Run the query
    with driver.session() as session:
        data = session.execute_read(get_results)
        driver.close()
    return data
    # Close the driver
    

# query = """MATCH (u:user) 
# WITH u
# ORDER BY u.user_id ASC
# LIMIT 3
# MATCH (u)-[r:rated]->(a:anime)
# RETURN u.user_id AS user_id, collect({anime_id: a.anime_id, name: a.Name, rating: r.rating}) AS animes
# ORDER BY u.user_id ASC"""
# print(database(query))