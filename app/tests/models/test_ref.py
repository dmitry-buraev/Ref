from app.tests import GaeFlaskTestCase
from google.appengine.ext import ndb

from app.models.ref import Ref

class RefTestCase(GaeFlaskTestCase):
    def test_ref(self):
        profs = Ref(name=u'Professions')
        profs_k = profs.put()
        it_profs = Ref(name=u'IT', ancestors=[profs_k])
        it_profs_k = it_profs.put()

        #get root refs
        self.assertTrue(Ref.query(Ref.level == 0).count() == 1)
        it_profs_q = Ref.query(Ref.ancestors == profs_k)
        #get all children of ref
        self.assertEquals(it_profs_q.count(), 1)
        #get level
        self.assertEquals(profs.level, 0)
        #get parent
        self.assertEquals(it_profs_q.get().parent, profs_k)

        ed_profs = Ref(name=u'Education')
        ed_profs.set_parent(it_profs)
        ed_profs.put()
        self.assertEquals(ed_profs.parent, it_profs_k)

        #get children
        self.assertEquals(len(profs.children), 1)

        m_profs = Ref(name=u'Music')
        m_profs.set_parent(profs)
        m_profs.put()
        #get descedants
        self.assertEquals(len(profs.descedants), 3)

