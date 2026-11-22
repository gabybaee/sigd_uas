import random, csv, json
random.seed(5)
P=['Pos','JNE','J&T','SiCepat','Anteraja']; L=['Reguler','Express','Kargo']
C=(-0.030,109.360)
rows=[]
for i in range(36):
    p=P[i%5]
    rows.append(dict(nama=f"{p} Pontianak Timur {i+1:02d}",penyedia=p,
      latitude=round(C[0]+random.uniform(-.012,.012),6),longitude=round(C[1]+random.uniform(-.012,.012),6),
      layanan=random.choice(L),jam_operasional='24 Jam' if i%6==0 else '08.00-17.00',pickup='Ya' if i%3 else 'Tidak'))
with open('ekspedisi_east.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['nama','penyedia','latitude','longitude','layanan','jam_operasional','pickup']); w.writeheader(); w.writerows(rows)
feats=[]
for r in rows:
    r['kode_ekspedisi']=r['penyedia'][:3].upper()+'_'+r['layanan']
    feats.append({"type":"Feature","geometry":{"type":"Point","coordinates":[r['longitude'],r['latitude']]},
      "properties":{k:v for k,v in r.items() if k not in('latitude','longitude')}})
json.dump({"type":"FeatureCollection","features":feats},open('ekspedisi_east.geojson','w'))
def poly(n,x,y,d=.006): return {"type":"Feature","properties":{"nama":n},"geometry":{"type":"Polygon","coordinates":[[[x-d,y-d],[x+d,y-d],[x+d,y+d],[x-d,y+d],[x-d,y-d]]]}}
json.dump({"type":"FeatureCollection","features":[poly("Zona Logistik A",C[1]-.006,C[0]+.005),poly("Zona Logistik B",C[1]+.007,C[0]-.006)]},open('zona_logistik.geojson','w'))
print(len(feats),'fitur')
