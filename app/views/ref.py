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
    """ Convert object itself and its direct children """
    depth = depth + 1
    result = { 'id': ref.key.id(), 'name': ref.name,
            'is_group': ref.is_group, 'level': ref.level,
            'structure': ref.structure }
    if full:
        for k, v in ref._properties.iteritems():
            if (isinstance(v, ndb.GenericProperty) and
                    not isinstance(v, ndb.ComputedProperty)):
                result[k] = v._get_user_value(ref)
    if depth < 2:
        if ref.is_group:
            result['children'] = [
                    to_dict(r, False, depth) for r in ref.children]

    return result


from google.appengine.api import urlfetch
import urllib2
import zipfile
from dbfpy import dbf

from types import StringType

@app.route('/post_index_ref')
def post_index():
    #url = 'http://info.russianpost.ru/database/PIndx10.zip'
    #f = urllib2.urlopen(url).read()
    #d = dbf.Dbf(f)
    #f = open('PIndx10.zip', 'r')
    #zf = zipfile.ZipFile(f)
    #filename = zf.namelist()[0]
    #a = zf.open(filename)

    def get_records_from_dbf(filename):
        db = dbf.Dbf(filename, 'r')
        records = []
        for r in db:
            rec = r.asDict()
            record = {}
            for key in rec:
                v = rec[key]
                value = unicode(v, 'cp866') if type(v) is StringType else v
                record[key] = value
            records.append(record)
        return records

    records = get_records_from_dbf('PIndx10.dbf')


    return render_template('post_index.html', records=records)
