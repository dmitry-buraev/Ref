from google.appengine.ext import ndb

class Ref(ndb.Expando):
    name = ndb.StringProperty(required=True)
    ancestors = ndb.KeyProperty('Ref', repeated=True)

    level = ndb.ComputedProperty(lambda self: len(self.ancestors))
    parent = ndb.ComputedProperty(
            lambda self: self.ancestors[-1:][0] if self.level > 0 else None)

    @property
    def children(self):
        return self.query(Ref.parent == self.key).fetch()

    def get_descedants(self, depth=None):
        if depth == 0:
            raise Exception('Depth must be greater then 0 or None')
        if depth:
            l = self.level + 1
            level_range = range(l, l + depth)
            q = self.query(
                    Ref.ancestors == self.key, Ref.level.IN(level_range))
        else:
            q = self.query(Ref.ancestors == self.key)
        return q.fetch()

    def set_parent(self, parent):
        if not (isinstance(parent, Ref) or (
                isinstance(parent, ndb.Key) and parent.kind() == 'Ref')):
            raise TypeError('Parent must be Ref instance or Key of Ref')
        p = parent.get() if isinstance(parent, ndb.Key) else parent
        self.ancestors = p.ancestors[:] + [p.key]
