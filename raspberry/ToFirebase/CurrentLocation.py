import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore



# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': "testfirebase-b8a5f",
})

db = firestore.client()

doc_ref = db.collection(u'CurrentLocation')
doc_ref.add({
    u'latitude': 33.44444444,
    u'longitude': 135.0000000,
    u'time': 1998
})
