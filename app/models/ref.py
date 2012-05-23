from google.appengine.ext import ndb

class Ref(ndb.Model):
    name = ndb.StringProperty(required=True)
    ancestors = ndb.KeyProperty('Ref', repeated=True)

    level = ndb.ComputedProperty(lambda self: len(self.ancestors))
    parent = ndb.ComputedProperty(
            lambda self: self.ancestors[-1:][0] if self.level > 0 else None)

    @property
    def children(self):
        return self.query(Ref.parent == self.key).fetch()

    @property
    def descedants(self):
        return self.query(Ref.ancestors == self.key).fetch()

    def set_parent(self, parent):
        if not (isinstance(parent, Ref) or (
                isinstance(parent, ndb.Key) and parent.kind() == 'Ref')):
            raise TypeError('Parent must be Ref instance or Key of Ref')
        p = parent.get() if isinstance(parent, ndb.Key) else parent
        self.ancestors = p.ancestors[:] + [p.key]
