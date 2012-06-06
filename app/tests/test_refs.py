from flask import json

from google.appengine.ext import ndb
from app.tests import GaeFlaskTestCase
from app.models.ref import Ref
from app.views.ref import RefREST
from app import app

class RefRestTestCase(GaeFlaskTestCase):
    def fill_datastore(self):
        #0 level
        self.r_k = root_key = ndb.Key(Ref, 'root')
        root_ref = Ref(key=root_key, name='Refs', is_group=True)
        root_ref.put()
        #1
        profs = Ref(name=u'Professions',
                description=u'Contains grouped professions',
                is_group=True)
        profs.set_parent(root_ref)
        profs.put()
        #2
        it = Ref(name=u'IT', code='100E', is_group=True)
        it.set_parent(profs)
        self.it_k = it.put()
        #3
        web_programmist = Ref(name=u'Web programmist', code='101B',
                skills=['Python', 'Javascript', 'HTML'])
        web_programmist.set_parent(it)
        self.wp_k = web_programmist.put()
        system_programmist = Ref(name=u'System programmist', code='101B',
                skills=['C', 'C++', 'GTK'])
        system_programmist.set_parent(it)
        self.sp_k = system_programmist.put()
        #2
        edu = Ref(name=u'Education', code='200C', is_group=True)
        edu.set_parent(profs)
        edu.put()

    def setUp(self):
        super(RefRestTestCase, self).setUp()
        self.fill_datastore()

    def test_to_dict(self):
        from app.views.ref import to_dict
        p = self.it_k.get()
        print(to_dict(p, full=False))
        self.assertEquals(to_dict(p, full=False), {
            'id': p.key.id(),
            'name': p.name,
            'is_group': p.is_group,
            'children': [ to_dict(self.wp_k.get(), False, 1),
                to_dict(self.sp_k.get(), False, 1) ]
        })
        self.assertIn('code', to_dict(p))

    def test_get(self):
        with app.test_request_context():
            #get root element
            r = json.loads(RefREST().get('root').data)
            self.assertEquals(r['name'], 'Refs')
            #get all refs with level 1(Children of root)
            r = json.loads(RefREST().get().data)
            self.assertEquals(len(r), 1)
