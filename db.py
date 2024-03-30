from dotenv import load_dotenv
import os
import pymongo
load_dotenv()

class mongo:
        
        def __init__(self,dbname):
            pymongodb=os.getenv("pymongodb")
            self.mongoclient = pymongo.MongoClient(pymongodb)
            return self.mongoclient
        
        def connectdb(self,dbname,collectionm):
            # Select database (create it if it doesn't exist) username is dbname
            db = self.mongoclient[os.getenv('pymongodbname')]
            # Select collection (create it if it doesn't exist) username is collection
            self.collection = db[collectionm]
            return self.collection
        

             
        

                

   

