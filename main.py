import pandas as pd
import run_gpt4
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')  
    parser.add_argument('datasource', type=str, help='datasource = saref') 
    args = parser.parse_args()   
    print(args.datasource)


    ontology_file = args.datasource + "/ontology.ttl"
    knowledge_graph_file = args.datasource + "/knowledge_graph.ttl"
    competency_questions_file = args.datasource + "/competency_question.xlsx"
    template_file = args.datasource + "/template.txt"

    f = open(ontology_file, "r")
    ontology = f.read()
    f.close()
    f = open(knowledge_graph_file, "r")
    kg = f.read()
    f.close()
    df = pd.read_excel(competency_questions_file, sheet_name="Sheet1")
    f = open(template_file, "r")
    template = f.read()
    f.close()

    template = template.replace("<ontology>", ontology)
    nlqs = df["Competency Question"]

    queries = run_gpt4.run_nlqs(template, nlqs)
    df["llm_auto_generated_query"] = queries

    results = run_gpt4.call_queries(queries, args.datasource + "/knowledge_graph.ttl")
    df["llm_auto_generated_result"] = results

    df.to_excel(args.datasource + "/output/generated_queries.xlsx")  