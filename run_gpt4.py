import openai
import rdflib
from rdflib.plugins.sparql import prepareQuery  
import time
import os

def call_queries(queries, kg):
    graph = rdflib.Graph()
    graph = graph.parse(kg)
    results = []
    for query in queries:
        # Prepare and execute the query  
        if query == "not found":
            results.append("FALSE")
        
        else:
            try:
                q = prepareQuery(query)
                result = graph.query(q)  
                results.append(result)                

            except:
                #results.append("broken")
                results.append("not found")
    return results
        
def run_nlqs(template, nlqs):

    queries = []
    for nlq in nlqs:
        prompt = template.replace("<competency_question>", nlq)
        q = call_gpt4(prompt)
        time.sleep(5)
        queries.append(q)
    return queries

def call_gpt4(prompt):
    openai.api_type = "azure"
    openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
    openai.api_version = "2023-07-01-preview"
    openai.api_key = os.getenv("AZURE_OPENAI_KEY")

    message_text = [{"role":"system","content":"You are an AI assistant that helps people find information."},{"role":"user","content":prompt}]

    response = openai.ChatCompletion.create(
    engine="gpt-4",
    messages = message_text,
    temperature=0,
    max_tokens=800,
    top_p=0.95,
    frequency_penalty=0,
    presence_penalty=0,
    stop=None
    )

    s = response["choices"][0]["message"]["content"]
    start = '```sparql'
    end = '```'
    tt0 = s.find(start)
    tt = tt0 + len(start)
    s2 = s[tt:]
    zz = s2.find(end)
    sparql_query = s2[:zz]
    if tt0 == -1 or zz == -1:
        return "not found"
    return sparql_query