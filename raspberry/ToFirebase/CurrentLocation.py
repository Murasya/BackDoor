import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import sys

args = sys.argv

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': "testfirebase-b8a5f",
})

db = firestore.client()

doc_ref = db.collection(u'CurrentLocation').document(u'AndroidUser')
doc_ref.set({
    u'latitude': float(args[1]),
    u'longitude': float(args[2]),
    u'time': args[3]
})