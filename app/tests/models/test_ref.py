from app.tests import GaeFlaskTestCase
from google.appengine.ext import ndb

from app.models.ref import Ref

class RefTestCase(GaeFlaskTestCase):
    def setUp(self):
        super(RefTestCase, self).setUp()
        #0 level
        profs = Ref(name=u'Professions',
                description=u'Contains grouped professions')
        self.profs_k = profs.put()
        #1
        it = Ref(name=u'IT', code='100E')
        it.set_parent(profs)
        self.it_k = it.put()
        #2
        web_programmist = Ref(name=u'Web programmist', code='101B',
                skills=['Python', 'Javascript', 'HTML'], is_leaf=True)
        web_programmist.set_parent(it)
        self.web_programmist_k = web_programmist.put()
        system_programmist = Ref(name=u'System programmist', code='101B',
                skills=['C', 'C++', 'GTK'], is_leaf=True)
        system_programmist.set_parent(it)
        self.system_programmist_k = system_programmist.put()
        #1
        edu = Ref(name=u'Education', code='200C')
        edu.set_parent(profs)
        self.edu_k = edu.put()

    def test_get_children(self):
        p = self.profs_k.get()
        self.assertEquals(len(p.children), 2)

    def test_get_descedants(self):
        p = self.profs_k.get()
        self.assertEquals(len(p.get_descedants()), 4)

        self.assertEquals(len(p.get_descedants(depth=1)), 2)
