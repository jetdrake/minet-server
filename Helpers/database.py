import firebase_admin
import google.cloud
from firebase_admin import credentials, firestore
import json

class db:
    cred = credentials.Certificate("firebase/serviceAccountKey.json")
    app = firebase_admin.initialize_app(cred)
    store = firestore.client()
    Documents=''
    root=''

    #initializes class with a default or specified root
    def __init__(self, collection=root):
        self.root = collection

    #returns the authorized store
    def getStore(self):
        return self.store

    def setRoot(self, collection):
        self.root = collection

    #gets colleciton default or specified path, with a default of 10 results
    def getCollection(self, collection=None, results=10):
        path = self.root + collection

        print(u'Checking path: {}'.format(path))
        doc_ref = self.store.collection(u'{}'.format(path)).limit(results)

        try:
            docs = doc_ref.get()
            self.Documents = docs
            data = []
            for doc in docs:
                data.append(doc.to_dict())
            return data
        except google.cloud.exceptions.NotFound:
            print(u'Missing data')

    #gets collection and writes it to a file
    def GetCollectionAndWriteDocumentsToFile(self, collection, limit, fileName):
        docs = self.getCollection(collection, limit)
        local = open(fileName, 'w')
        local.write(json.dumps(docs))
        local.close()

    #if getCollection has already been used, there is no need to read from db again
    def writeDocumentsToFile(self, fileName):
        local = open(fileName, 'w')
        local.write(json.dumps(self.Documents))
        local.close()

    
        
    

