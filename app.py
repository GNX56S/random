from pymongo import MongoClient
from flask import Flask, render_template,request,redirect
from bson import ObjectId
import datetime


app = Flask(__name__)

server = MongoClient('mongodb://localhost:27017/')
db = server['minimarket']
col = db['item']
order = db['transaksi']


# @app.route('/insert',methods=['POST','GET'])
@app.route('/insert',methods=['POST'])
def insert():
    # if request.method=='POST':
    nama = request.form.get("nama")
    tipe = request.form.get('tipe')
    harga = int(request.form.get("harga"))
    jumlah = int(request.form.get("jumlah"))

    now = datetime.datetime.now()
    data = {
        "nama": nama,
        "tipe":tipe,
        "harga": harga,
        "jumlah":jumlah,
        "waktu": now.strftime('%x')
    }
    col.insert_one(data)
    return redirect('/')
    # else:
    #     return render_template('insert.html')

@app.route('/')
def tampilkan_data():
    data = col.find()
    return render_template('stok.html', XD = data)

@app.route('/edit/<string:_id>',methods=['GET','POST'])
def edit(_id):
    if request.method =='GET':
        return render_template('edit.html',_id=_id)
    else:
        nama = request.form.get("nama")
        tipe = request.form.get('tipe')
        harga = int(request.form.get("harga"))
        jumlah = int(request.form.get("jumlah"))

        data = {
            "nama": nama,
            "tipe":tipe,
            "harga": harga,
            "jumlah":jumlah
        }
        now = datetime.datetime.now()
        col.update_one({
            '_id': ObjectId(_id)},
            {
                "$set":{
                    "nama": nama,
                    "tipe":tipe,
                    "harga": harga,
                    "jumlah":jumlah,
                    "waktu": now.strftime('%x')
                }
            })
        return redirect('/')

@app.route('/hapus/<string:_id>',methods=['GET'])
def hapus(_id):
    col.delete_one({
        '_id': ObjectId(_id)
        })
    return redirect('/')

#proses pembelian
@app.route('/beli')
def beli():
    cek = col.find()
    data = col.find()
    riwayat = order.find()
    return render_template('beli.html',XD = data,cek = cek,RY = riwayat)

@app.route('/beli',methods=['POST'])
def proses_beli():
    nama = request.form.get("nama")
    tipe = request.form.get('tipe')
    jumlah = int(request.form.get("jumlah"))
    data = col.find_one({'nama':nama})

    # if data['jumlah'] < jumlah:
    #     return 'stock habis'
    
    # else:
    jumlah_baru = data.get('jumlah') - jumlah
    tipe = data.get('tipe')
    harga = data.get('harga') * jumlah
    col.update_one({'nama':nama},{'$set':{'jumlah':jumlah_baru}})
    now = datetime.datetime.now()
    baru = {
        "nama": nama,
        "tipe":tipe,
        "harga": harga,
        "jumlah":jumlah,
        "waktu": now.strftime('%x')
    }
    order.insert_one(baru)

    return redirect('/beli')
