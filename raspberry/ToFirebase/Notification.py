import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore



# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': "testfirebase-b8a5f",
})

db = firestore.client()

doc_ref = db.collection(u'Notification')
doc_ref.add({
    u'notification':1
})