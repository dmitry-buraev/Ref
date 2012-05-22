"""
Base classes to store graph by adjacency lists model.
"""
from google.appengine.datastore import entity_pb
from google.appengine.ext import ndb

class EdgeTo(ndb.Expando):
    """EdgeTo object consists of Key of instance where we reference to
    and extra information about relation (label, weight)"""
    key = ndb.KeyProperty(required=True)
    label = ndb.StringProperty(required=True)
    weight = ndb.IntegerProperty(default=0)

    def __eq__(self, other):
        return (self.key == other.key and self.label == other.label)

from google.appengine.ext.ndb.polymodel import PolyModel
class Vertex(PolyModel):
    """Vertex provide graph interface to base Model class"""
    edges = ndb.StructuredProperty(EdgeTo, repeated=True)

    def add_edge_to(self, label, vertex, **kwargs):
        if not isinstance(vertex, Vertex):
            raise TypeError('Vertex argument must be subclass of Vertex')
        edge_to = EdgeTo(label=label, key=vertex.key, **kwargs)
        self.edges.append(edge_to)

    def remove_edge_to(self, label, vertex):
        if not isinstance(vertex, Vertex):
            raise TypeError('Vertex argument must be subclass of Vertex')
        try:
            self.edges.remove(EdgeTo(label=label, key=vertex.key))
        except ValueError:
            pass

    def get_out_v(self, label=None):
        if label:
            return ndb.get_multi([e.key for e in self.edges if e.label==label])
        return ndb.get_multi([e.key for e in self.edges])

    def get_in_v(self, label=None):
        if label is not None:
            q = self.query(ndb.AND(
                Vertex.edges.key == self.key, Vertex.edges.label == label))
        else:
            q = self.query(Vertex.edges.key == self.key)

        return [v for v in q]

class Graph(ndb.Model):
    """For work with App Engine Datastore as regular graph database"""
    @classmethod
    def add_edge(cls, v_from, label, v_to, **kwargs):
        if not (isinstance(v_from, Vertex) or isinstance(v_to, Vertex)):
            raise TypeError(
                    'v_from and v_to arguments must be instance of Vertex')
        v_from.add_edge_to(label, v_to, **kwargs)

    @classmethod
    def remove_edge(cls, v_from, label, v_to):
        if not (isinstance(v_from, Vertex) or isinstance(v_to, Vertex)):
            raise TypeError(
                    'v_from and v_to arguments must be instance of Vertex')
        v_from.remove_edge_to(label, v_to)
