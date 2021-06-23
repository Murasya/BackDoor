import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import storage
from google.cloud import storage


# cred = credentials.ApplicationDefault()
# firebase_admin.initialize_app(cred, {
#   'storageBucket': 'testfirebase-b8a5f.appspot.com'
# })

cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred,{'storageBucket':'testfirebase-b8a5f.appspot.com'})
#bucket = storage.bucket()



def download_blob(source_blob_name, destination_file_name):
    storage_client = storage.Client()
    bucket = storage_client.bucket('testfirebase-b8a5f.appspot.com')
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(
        "Blob {} downloaded to {}.".format(
            source_blob_name, destination_file_name
        )
    )
    return 

download_blob('IMG_0076.png','202003/a.png')