from app.tests import GaeFlaskTestCase

from app.models.graph import Vertex, EdgeTo, Graph
from google.appengine.ext import ndb


class User(Vertex):
    name = ndb.StringProperty()

class Group(Vertex):
    name = ndb.StringProperty()

class GraphTestCase(GaeFlaskTestCase):
    def setUp(self):
        super(GraphTestCase, self).setUp()

    def testEdgeToProperty(self):
        john_key = User(name='John').put()
        mary_key = User(name='Mary').put()
        edge_to_john = EdgeTo(label='knows', key=john_key)
        edge_to_mary = EdgeTo(label='knows', key=mary_key)
        mike = User(name='Mike', edges=[edge_to_john, edge_to_mary])
        mike.put()

        mike = User.query(User.name == 'Mike').get()
        self.assertEquals(len(mike.edges), 2)
        to_john = mike.edges[0]
        self.assertEquals(to_john.key, john_key)
        self.assertEquals(to_john.label, 'knows')
        self.assertEquals(to_john.weight, 0)

    def testVertex(self):
        mike = User(name='Mike')
        mike.put()
        lisa = User(name='Lisa')
        lisa.put()
        anna = User(name='Anna')
        anna.put()
        matrix_fun = Group(name='Matrix fun')
        matrix_fun.put()

        mike.add_edge_to(label='knows', weight=1, vertex=lisa)
        mike.add_edge_to(label='knows', vertex=anna)
        mike.add_edge_to(label='members', vertex=matrix_fun)
        mike.put()
        anna.add_edge_to(label='knows', vertex=mike)
        anna.put()
        lisa.add_edge_to(label='likes', vertex=mike)
        lisa.put()

        self.assertEquals(len(mike.get_out_v(label='knows')), 2)

        mike.remove_edge_to(label='knows', vertex=lisa)
        self.assertEquals(len(mike.get_out_v(label='knows')), 1)

        self.assertEquals(len(mike.get_in_v(label='knows')), 1)

    def testGraph(self):
        mike = User(name='Mike')
        mike.put()
        lisa = User(name='Lisa')
        lisa.put()
        Graph.add_edge(mike, 'likes', lisa)
        Graph.add_edge(lisa, 'likes', mike)
        self.assertEquals(len(mike.get_out_v('likes')), 1)

        self.assertEquals(len(lisa.get_out_v('likes')), 1)
        Graph.remove_edge(lisa, 'likes', mike)
        self.assertEquals(len(lisa.get_out_v('likes')), 0)
