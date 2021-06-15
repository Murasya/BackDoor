import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import sys
import os
from datetime import datetime

args = sys.argv

# Use the application default credentials
cred = credentials.ApplicationDefault()
firebase_admin.initialize_app(cred, {
  'projectId': "testfirebase-b8a5f",
})

db = firestore.client()

lats, longs, times = list(), list(), list()
fname = '/home/pi/BackDoor/raspberry/Log/'+args[1]+'.csv'

if os.path.exists(fname):
  f = open(fname, mode='r')
  for line in f.readlines():
    lst = line.split(',')
    lats.append(float(lst[0]))
    longs.append(float(lst[1]))
    times.append(datetime.strptime(lst[2].strip(), '%Y-%m-%d %H:%M:%S.%f'))
  f.close()

f = open(fname, mode='a')

now = datetime.now()
lats.append(float(args[2]))
longs.append(float(args[3]))
times.append(now)

f.write(','.join([args[2], args[3], str(now)]) + '\n')

doc_ref = db.collection(u'CurrentLocation').document(args[1])
doc_ref.set({
    u'latitude': lats,
    u'longitude': longs,
    u'time': times
})

f.close()