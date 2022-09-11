import base64
from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:1234@localhost:5432/coffeeshop?sslmode=disable'

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, index=True, nullable=False, unique=True)
    nama_user = db.Column(db.String(50), nullable=False)
    email_user = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    total_pembelian = db.Column(db.Integer, default=0)

class Item(db.Model):
    item_id = db.Column(db.Integer, primary_key=True, index=True, nullable=False, unique=True)
    nama_item = db.Column(db.String(50), nullable=False)
    deskripsi = db.Column(db.String(200), nullable=False)
    harga_item = db.Column(db.Integer, nullable=False)
    jumlah_item = db.Column(db.Integer, nullable=False)
    jumlah_terbeli = db.Column(db.Integer,default=0)
    # kategori_id = db.Column(db.Integer, db.ForeignKey('kategori.kategori_id'))
    # nama_kategori = db.relationship('Kategori',backref = "item")

class Kategori(db.Model):
    kategori_id = db.Column(db.Integer, primary_key=True, index=True, nullable=False, unique=True)
    nama_kategori = db.Column(db.String(200), nullable=False)
    deskripsi = db.Column(db.String(200), nullable=False)

class Order(db.Model):
    order_id = db.Column(db.Integer, primary_key=True, index=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id',ondelete='CASCADE'))
    username = db.relationship('User',backref = "order")
    order_status = db.Column(db.String(50),nullable=False, default='pending')
    order_date = db.Column(db.DateTime,nullable=False, default=datetime.now())
    jumlah_barang = db.Column(db.Integer)
    total_harga = db.Column(db.Integer)


class Orderdetail(db.Model):
    order_detail_id = db.Column(db.Integer, primary_key=True, index=True, nullable=False, unique=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.order_id',ondelete='CASCADE'))
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id',ondelete='CASCADE'))
    nama_item = db.Column(db.String(200))
    jumlah_subbarang = db.Column(db.Integer,nullable=False)
    subtotal_harga = db.Column(db.Integer,nullable=False)

db.create_all()
db.session.commit()

def BasicAuth() :
    pass_str = request.headers.get('Authorization')     
    pass_bersih = pass_str.replace('Basic ',"")        
    hasil_decode = base64.b64decode(pass_bersih)       
    hasil_decode_bersih = hasil_decode.decode('utf-8')  
    username_aja = hasil_decode_bersih.split(":")[0]    
    pass_aja = hasil_decode_bersih.split(":")[1] 
    pass_encode = pass_aja.encode('utf-8')
    pass_encode_2 = base64.b64encode(pass_encode)
    pass_cek = pass_encode_2.decode('utf-8')

    user = User.query.filter_by(username=username_aja).filter_by(password=pass_cek).first()
    if user :
        return str(user.user_id)
    # return[username_aja,pass_cek]

# Home
@app.route('/', methods=['GET'])
def home():
    return jsonify(
        "Home dari Coffee Shop"
    )

@app.route('/tes', methods=['GET'])
def tes():
    return BasicAuth()
    # data = request.get_json()
    # inputan = data['nama_item']
    # inputan_harga = data['harga_item']
    # query_item = Item.query.filter(Item.nama_item.ilike("%"+inputan+"%")).filter(Item.harga_item >= inputan_harga).all()
    # return jsonify([
    #     {
    #     'nama_item' : item.nama_item,
    #     'deskripsi' : item.deskripsi,
    #     'harga_item' : item.harga_item,
    #     'jumlah_item' : item.jumlah_item,
    #     'jumlah_terbeli' : item.jumlah_terbeli
    #     } for item in query_item
    # ]) 


# User API
@app.route('/register', methods=['POST'])
def user_register():
    data = request.get_json()
    encode_password_1 = data['password'].encode('utf-8')
    encode_password_2 = base64.b64encode(encode_password_1)
    register = User(
        nama_user = data['nama_user'],
        email_user = data['email_user'],
        username = data['username'],
        password = encode_password_2.decode('utf-8')
    )
    try :
        db.session.add(register)
        db.session.commit()
    except :
        return {
            "response" : "error"
        },401
    return {
        "response" : "success"
    },201

@app.route('/user/update', methods=['PUT'])
def user_update():
    auth = BasicAuth()
    data = request.get_json()
    if 'nama_user' not in data and 'email_user' not in data and 'username' not in data and 'password' not in data :
        return {
            "error" : "field tidak ada"
        },400
    
    if not auth :
        return {
            "message" : "auth error"
        }
    else :
        user = User.query.filter_by(user_id=auth).first()

        if 'nama_user' in data :
            user.nama_user = data['nama_user']

        if 'email_user' in data :
            user.email_user = data['email_user']

        if 'username' in data :
            user.username = data['username']

        if 'password' in data :
            encode_password_1 = data['password'].encode('utf-8')
            encode_password_2 = base64.b64encode(encode_password_1)
            user.password = encode_password_2.decode('utf-8')

        try :
            db.session.commit()
        except :
            return {
                "response" : "error"
            },401
        return {
            "response" : "success"
        },201


# Item API
@app.route('/item/add_item', methods=['POST'])
def add_item():
    data = request.get_json()
    item = Item(
        nama_item = data['nama_item'],
        deskripsi = data['deskripsi'],
        harga_item = data['harga_item'],
        jumlah_item = data['jumlah_item']
    )
    try :
        db.session.add(item)
        db.session.commit()
    except :
        return {
            "response" : "error"
        },401
    return {
        "response" : "success"
    },201

@app.route('/item/add_kategori', methods=['POST'])
def add_kategori():
    data = request.get_json()
    kategori = Kategori(
        nama_kategori = data['nama_kategori'],
        deskripsi = data['deskripsi']
    )
    try :
        db.session.add(kategori)
        db.session.commit()
    except :
        return {
            "response" : "error"
        },401
    return {
        "response" : "success"
    },201

@app.route('/item/search_item', methods=['GET'])
def search_item():
    data = request.get_json()
    inputan = data['search']
    query_item = Item.query.filter(Item.nama_item.ilike("%"+inputan+"%")).all()
    return jsonify([
        {
        'nama_item' : item.nama_item,
        'deskripsi' : item.deskripsi,
        'harga_item' : item.harga_item,
        'jumlah_item' : item.jumlah_item,
        'jumlah_terbeli' : item.jumlah_terbeli
        } for item in query_item
    ]),200

@app.route('/item/update_item/<id>', methods=['PUT'])
def item_update(id):
    data = request.get_json()

    if 'nama_item' not in data and 'deskripsi' not in data and 'harga_item' not in data and 'jumlah_item' not in data and 'jumlah_terbeli' not in data :
        return {
            "error" : "field tidak ada"
        },400

    item = Item.query.filter_by(item_id=id).first()

    if 'nama_item' in data :
        item.nama_item = data['nama_item']

    if 'deskripsi' in data :
        item.deskripsi = data['deskripsi']

    if 'harga_item' in data :
        item.harga_item = data['harga_item']
    
    if 'jumlah_item' in data :
        item.jumlah_item = data['jumlah_item']

    try :
        db.session.commit()
    except :
        return {
            "response" : "error"
        },401
    return {
        "response" : "success"
    },201


# Order API
@app.route('/order/add_order', methods=['POST'])
def add_order():
    auth = BasicAuth()
    if not auth :
        return jsonify("auth error")
    else :
        data = request.get_json()
        # input_item = data['item_id']
        # input_user = data['user_id']
        # query_item = Item.query.filter_by(item_id=input_item).first()
        query_user = User.query.filter_by(user_id=auth).first()
        order = Order(
            user_id = auth,
            order_date = datetime.now()
        )
        db.session.add(order)
        db.session.commit()
        query_orderid = Order.query.all()
        arr = []
        for i in query_orderid :
            arr.append(i.order_id)

        for i in range(len(data["orderan"])) :
            query_item = Item.query.filter_by(nama_item = data['orderan'][i]).first()
            orderdetail = Orderdetail(
                order_id = max(arr),
                item_id = query_item.item_id,
                nama_item = data['orderan'][i],
                jumlah_subbarang = data['jumlah_subbarang'][i],
                subtotal_harga = data['jumlah_subbarang'][i] * query_item.harga_item
            ) 
            db.session.add(orderdetail)
            db.session.commit()


        query_orderdetail = Orderdetail.query.filter_by(order_id=max(arr)).all()
        
        kalkulasi_total = 0
        kalkulasi_barang = 0
        for i in query_orderdetail :
            kalkulasi_total += i.subtotal_harga
            kalkulasi_barang += i.jumlah_subbarang

        query_order_2 = Order.query.filter_by(order_id = max(arr)).first()
        query_order_2.total_harga = kalkulasi_total
        query_order_2.jumlah_barang = kalkulasi_barang

        try :
            # db.session.add(order)
            db.session.commit()
        except :
            return {
                "response" : "error"
            },401
        return {
        "total" : kalkulasi_total,
        "barang" : kalkulasi_barang
    },201

@app.route('/order/check_order_pending/<id>', methods=['PUT'])
def check_order_pending(id):
    hitung = Order.query.filter_by(order_status = 'activate').count()
    query_order = Order.query.filter_by(user_id=id).filter_by(order_status="pending").first()
    query_user = User.query.filter(User.user_id==query_order.user_id).first()
    
    if not hitung < 10 :
            return {
            "message" : "antrian penuh"
        }
    elif query_order.order_status == "pending" :
        query_order.order_status = "activate"
        query_orderdetail = Orderdetail.query.filter(query_order.order_id == Orderdetail.order_id).all()
        for i in query_orderdetail :
            query_item = Item.query.filter(Item.item_id == i.item_id).first()
            if query_item.jumlah_item < i.jumlah_subbarang :
                db.session.delete(query_order)
                db.session.commit()
                return jsonify("pesanan lebih dari stok")
                break
            query_item.jumlah_item -= i.jumlah_subbarang
            query_item.jumlah_terbeli += i.jumlah_subbarang
            # db.session.commit()
            
  
        query_user.total_pembelian += 1

    try :
        # db.session.add()
        db.session.commit()
    except :
        return {
            "response" : "error"
        },401
    return {
        "response" : "success"
    },201

@app.route('/order/check_order_activate/<id>', methods=['PUT'])
def check_order_activate(id):
    # data = request.get_json()
    # hitung = Order.query.filter_by(order_status = 'activate').count()
    query_order = Order.query.filter_by(user_id=id).filter_by(order_status="activate").first()
    query_user = User.query.filter(User.user_id==query_order.user_id).first()

    if query_order.order_status == "activate" :
        query_order.order_status = "completed"

        try :
            # db.session.add()
            db.session.commit()
        except :
            return {
                "response" : "error"
            },401
        return {
            "response" : "success",
            "order_id" : query_order.order_id,
            "user_id" : query_user.user_id,
            "nama_user" : query_user.nama_user,
            "order_status" : "completed"
        },201

@app.route('/order/cancel_order', methods=['DELETE'])
def cancel_order():
    auth = BasicAuth()
    if not auth :
        return jsonify ("auth error")
    else :
        Order.query.filter(Order.order_status == "pending").filter_by(user_id=auth).delete()
    try :
        # order = Order.query.filter(Order.order_status == "pending").filter_by(user_id=id).delete()
        db.session.commit()
    except :
        return {
            "response" : "error"
            },401
    return {
        "response" : "success"
        },201


# Reporting API
@app.route('/reporting/top5_user', methods=['GET'])
def top5_user():
    # data = request.get_json()
    top5_user = db.engine.execute('''SELECT * FROM "user" ORDER BY total_pembelian DESC LIMIT 5''')
    try :
        db.engine.execute('''SELECT * FROM "user" ORDER BY total_pembelian DESC LIMIT 5''')
        db.session.commit()
    except :
        return {
            "response" : "error"
            },401
    return jsonify([
        {
        'nama_user' : user.nama_user,
        'email_user' : user.email_user,
        'total_pembelian' : user.total_pembelian
        } for user in top5_user
    ]) 

@app.route('/reporting/top5_item', methods=['GET'])
def top5_item():
    top5_item = db.engine.execute('''SELECT * FROM item ORDER BY jumlah_terbeli DESC LIMIT 5''')
    try :
        top5_item
        db.session.commit()
    except :
        return {
            "response" : "error"
            },401
    return jsonify([
        {
        'nama_item' : item.nama_item,
        'harga_item' : item.harga_item,
        'jumlah_terbeli' : item.jumlah_terbeli
        } for item in top5_item
    ]) 
