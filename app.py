import json
from collections import Counter
from flask import Flask, jsonify, request, send_from_directory
app=Flask(__name__,static_folder='.',static_url_path='')
def load(f): return json.load(open(f))
@app.get('/')
def idx(): return send_from_directory('.','index.html')
@app.get('/api/data/ekspedisi')
def data():
    d=load('ekspedisi_east.geojson'); p=request.args.get('penyedia'); k=request.args.get('pickup')
    d['features']=[f for f in d['features'] if (not p or f['properties']['penyedia']==p) and (not k or f['properties']['pickup']==k)]
    return jsonify(d)
@app.get('/api/stats/penyedia')
def stats():
    return jsonify(Counter(f['properties']['penyedia'] for f in load('ekspedisi_east.geojson')['features']))
@app.post('/api/feature/zona')
def zona():
    feat=request.get_json()
    if not feat or feat.get('type')!='Feature' or feat['geometry']['type']!='Polygon': return jsonify(error='Butuh Feature Polygon'),400
    d=load('zona_logistik.geojson'); d['features'].append(feat); json.dump(d,open('zona_logistik.geojson','w'))
    return jsonify(ok=True,total=len(d['features'])),201
if __name__=='__main__': app.run(debug=True)
