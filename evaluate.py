import pandas as pd
from sklearn.metrics import classification_report
import argparse

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')  
    parser.add_argument('datasource', type=str, help='datasource = saref') 
    args = parser.parse_args()   
    print(args.datasource)

    df = pd.read_excel(args.datasource + "/output/generated_queries.xlsx")  

    y_true = list(df["Label"]) 
    y_pred = [True if x != "FALSE" else False for x in list(df["llm_auto_generated_result"]) ]

    target_names = ['invalid question', 'valid question']
    res = classification_report(y_true, y_pred, target_names=target_names)

    print(res)

