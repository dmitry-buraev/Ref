from google.appengine.ext import ndb
from flask.views import MethodView
from flask import render_template, jsonify, json, Response
from app import app
from app.models.ref import Ref
import re

@app.route('/')
def root():
    return render_template('main.html')

class RefREST(MethodView):
    def get(self, id=None):
        if id is None:
            refs = Ref.query(Ref.level == 1).fetch()
            res = [to_dict(r, False) for r in refs]
        else:
            #Id may have int type for automatically assigned keys
            #and str type for explicity created keys such as for Root Ref
            id = int(id) if re.match(r'\d+',id) else id
            r = Ref.get_by_id(id)
            res = to_dict(r) if r is not None else None
        return Response(json.dumps(res), mimetype='application/json')

ref_view = RefREST.as_view('ref_rest')
app.add_url_rule('/refs/', view_func=ref_view, methods=['GET',])
app.add_url_rule('/refs/', view_func=ref_view, methods=['POST',])
app.add_url_rule('/refs/<id>', view_func=ref_view,
        methods=['GET', 'PUT', 'DELETE'])


from google.appengine.ext import ndb
def to_dict(ref, full=True, depth=0):
    """ Convert object itself and its direct children"""
    depth = depth + 1
    result = { 'id': ref.key.id(), 'name': ref.name, 'is_leaf': ref.is_leaf }
    if full:
        for k, v in ref._properties.iteritems():
            if (isinstance(v, ndb.GenericProperty) and
                    not isinstance(v, ndb.ComputedProperty)):
                result[k] = v._get_user_value(ref)
    if depth < 2:
        if not ref.is_leaf:
            result['children'] = [
                    to_dict(r, False, depth) for r in ref.children]

    return result
