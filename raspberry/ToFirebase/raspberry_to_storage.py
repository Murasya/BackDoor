import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore, storage

# cred = credentials.Certificate('testfirebase-b8a5f-firebase-adminsdk-je938-0a8050ad88.json')
# firebase_admin.initialize_app(cred, {'storageBucket': '<bucket-name>'})

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'storageBucket': 'testfirebase-b8a5f.appspot.com'
})

bucket = storage.bucket()

filename = 'face_image.png'
content_type = 'image/png'
blob = bucket.blob(filename)
with open(filename, 'rb') as f:
    blob.upload_from_file(f, content_type=content_type)