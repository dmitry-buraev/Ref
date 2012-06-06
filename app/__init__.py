from flask import Flask, session, g
import settings

app = Flask(__name__)
app.config.from_object('settings')

import views.ref

#from google.appengine.ext import ndb
#from app.models.ref import Ref
##0 level
#root_key = ndb.Key(Ref, 'root')
#root_ref = Ref(key=root_key, name='Refs', is_group=True)
#root_ref.put()
##1
#profs = Ref(name=u'Professions',
        #description=u'Contains grouped professions',
        #is_group=True)
#profs.set_parent(root_ref)
#profs.put()
##2
#it = Ref(name=u'IT', code='100E', is_group=True)
#it.set_parent(profs)
#it_k = it.put()
##3
#web_programmist = Ref(name=u'Web programmist', code='101B',
        #skills=['Python', 'Javascript', 'HTML'])
#web_programmist.set_parent(it)
#wp_k = web_programmist.put()
#system_programmist = Ref(name=u'System programmist', code='101B',
        #skills=['C', 'C++', 'GTK'])
#system_programmist.set_parent(it)
#system_programmist.put()
##2
#edu = Ref(name=u'Education', code='200C', is_group=True)
#edu.set_parent(profs)
#edu.put()
