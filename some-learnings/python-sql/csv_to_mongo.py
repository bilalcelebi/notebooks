import pandas as pd
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

def get_data(data_path):

    data = pd.read_csv(data_path)
    data.dropna(inplace = True)

    return data


def get_collection(database_name, collection_name):

    database = client[database_name]
    collection = database[collection_name]

    return collection
   

def main():
    
    data_path = '/home/bilalcelebi/Workspace/notebooks/data/youtube-data/channels.csv'
    data = get_data(data_path)
    name = data_path.split('/')
    name = name[-1]
    name = name.split('.')
    name = name[0]

    records = []

    for idx,row in data.iterrows():
        
        pair = dict()
        
        for col in data.columns:

            pair[col] = row[col]


        records.append(pair)

    collection = get_collection('my_database',name)
    rec = collection.insert_many(records)
    print(rec)

if __name__ == '__main__':

    main()
