import base64
import datetime as dt
import json
from datetime import datetime

import jwt
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy

# cors_config = {
#     "origins": ['http://127.0.0.1:5000/'],
#     "methods": ['GET, POST, OPTIONS, PUT, PATCH, DELETE']
# }

app = Flask(__name__)
db = SQLAlchemy(app)
CORS(app)
# CORS(app, resources = {
#     r"/*": cors_config
# })

ctx = app.app_context()
ctx.push()
# CORS(app, supports_credentials=True) 
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:1234@localhost:5432/coffeeshop?sslmode=disable'

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, index=True, nullable=False, unique=True)
    nama_user = db.Column(db.String(50), nullable=False)
    email_user = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    total_pembelian = db.Column(db.Integer, default=0)
    is_admin = db.Column(db.Boolean,nullable=False,default=False)

class Item(db.Model):
    item_id = db.Column(db.Integer, primary_key=True, index=True, nullable=False, unique=True)
    nama_item = db.Column(db.String(50), nullable=False)
    deskripsi = db.Column(db.String(200), nullable=False)
    harga_item = db.Column(db.Integer, nullable=False)
    jumlah_item = db.Column(db.Integer, nullable=False)
    jumlah_terbeli = db.Column(db.Integer,default=0)
    kategori_id = db.Column(db.Integer, db.ForeignKey('kategori.kategori_id'))
    nama_kategori = db.relationship('Kategori',backref = "item")

class Kategori(db.Model):
    kategori_id = db.Column(db.Integer, primary_key=True, index=True, nullable=False, unique=True)
    nama_kategori = db.Column(db.String(200), nullable=False)
    deskripsi = db.Column(db.String(200), nullable=False)

class CartOrder(db.Model):
    cart_order_id = db.Column(db.Integer, primary_key=True, index=True, nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id',ondelete='CASCADE'))
    item_id = db.Column(db.Integer, nullable=False)
    nama_item = db.Column(db.String(50), nullable=False)
    jumlah_barang = db.Column(db.Integer)
    total_harga = db.Column(db.Integer)

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
    # Masukkan dari Postman sudah di encode dengan Basic Auth, jadi harus di decode dulu untuk memisahkan username & password
    pass_str = request.headers.get('Authorization')     
    pass_bersih = pass_str.replace('Basic ',"")        
    hasil_decode = base64.b64decode(pass_bersih)       
    hasil_decode_bersih = hasil_decode.decode('utf-8')  
    username_aja = hasil_decode_bersih.split(":")[0]    
    pass_aja = hasil_decode_bersih.split(":")[1]

    #Password yang sudah di decode dan dipisah dari username diatas di encode lagi
    pass_encode = pass_aja.encode('utf-8')
    pass_encode_2 = base64.b64encode(pass_encode)
    pass_cek = pass_encode_2.decode('utf-8')
    
    user = User.query.filter_by(username=username_aja).filter_by(password=pass_cek).first_or_404()
    
    if user :
        token = jwt.encode({
            'username': username_aja,
            'password' :pass_aja,
            'id' : user.user_id,
            'exp': datetime.now() + dt.timedelta(hours=24)
            },
            'secret' ,algorithm='HS256')
        return [user.user_id,user.is_admin,user.password,token]
        # return jsonify(pass_str)
        # return {
        #     "username" : username_aja,
        #     "password" : pass_cek
        #  }





### Home &
@app.route('/', methods=['GET'])
def home():
    return jsonify(
        "Home dari Coffee Shop"
    )

@app.route('/tes', methods=['GET'])
def tes():
    # auth = BasicAuth()
    # return auth["username"]
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



### User API
@app.route('/login', methods=['POST'])
# @cross_origin(origin='*',headers=['Content-Type','Authorization'], supports_credentials=True) 
def login():
    # identity = request.headers.get('Authorization')
    allow = BasicAuth()
    # return jsonify(allow1)
   
    # response = make_response( render_template() ) 
    # resp = make_response("token generated")
    # resp.set_cookie('token',value=token,expires=datetime.now()+ dt.timedelta(hours=24), path='/',samesite='Lax',domain="127.0.0.1")

    if BasicAuth() :
        return {
        "token" : allow[3],
        "username" : allow[0],
        "isAdmin" : allow[1],
        "message" : "success"
    }
        # return "True"
    else :
        return "False" 

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
    # cek_username = str(auth["username"])
    # cek_password = auth["password"]
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
        user = User.query.filter_by(user_id=auth[0]).first()

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

@app.route('/user/get_update_data/<id>', methods=['GET'])
def get_update_data(id):
    # auth = BasicAuth()
    # data = request.get_json()
    
    get_user = db.engine.execute(f'''SELECT * FROM "user" WHERE user_id = {id}''')

    try :
        db.engine.execute(f'''SELECT * FROM "user" WHERE user_id = {id}''')
        db.session.commit()
    except :
        return {
            "response" : "error"
            },401
    return jsonify([
        {
        'user_id' : user.user_id,
        'nama_user' : user.nama_user,
        'email_user' : user.email_user,
        'username' : user.username
        } for user in get_user
    ]) 


### Item API
@app.route('/get_all_item', methods=['GET'])
def get_all_item():
    get_all_item = db.engine.execute('''SELECT * FROM "item" INNER JOIN "kategori" ON item.kategori_id=kategori.kategori_id ORDER BY item_id''')
    try :
        db.engine.execute('''SELECT * FROM "item" ORDER BY item_id''')
        db.session.commit()
    except :
        return {
            "response" : "error"
            },401
    return jsonify([
        {
        'item_id' : item.item_id,
        'nama_item' : item.nama_item,
        'deskripsi' : item.deskripsi,
        'harga_item' : item.harga_item,
        'jumlah_item' : item.jumlah_item,
        'jumlah_terbeli' : item.jumlah_terbeli,
        'kategori_id' : item.kategori_id,
        'kategori' : item.nama_kategori
        } for item in get_all_item
    ])

@app.route('/get_item/<id>', methods=['GET'])
def get_item(id):
    get_item = db.engine.execute(f'''SELECT * FROM item WHERE item_id = {id}''')
    try :
        db.engine.execute(f'''SELECT * FROM item WHERE item_id = {id}''')
        db.session.commit()
    except :
        return {
            "response" : "error"
            },401
    return jsonify([
        {
        'item_id' : item.item_id,
        'nama_item' : item.nama_item,
        'deskripsi' : item.deskripsi,
        'harga_item' : item.harga_item,
        'jumlah_item' : item.jumlah_item,
        'kategori' : item.kategori_id
        } for item in get_item
    ]) 

@app.route('/get_kategori', methods=['GET'])
def get_kategori():
    get_kategori = db.engine.execute('''SELECT * FROM "kategori" ORDER BY nama_kategori''')
    try :
        db.engine.execute('''SELECT * FROM "kategori" ORDER BY nama_kategori''')
        db.session.commit()
    except :
        return {
            "response" : "error"
            },401
    return jsonify([
        {
        'kategori_id' : item.kategori_id,
        'nama_kategori' : item.nama_kategori
        } for item in get_kategori
    ]),200

@app.route('/item/add_item', methods=['POST'])
def add_item():
    # auth = BasicAuth()
    # if auth[1] != True :
    #     return {
    #         "response" : "unauthorized"
    #     }
    # else :
        data = request.get_json()
        item = Item(
            nama_item = data['nama_item'],
            deskripsi = data['deskripsi'],
            harga_item = data['harga_item'],
            jumlah_item = data['jumlah_item'],
            kategori_id = data['kategori_id']
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
    auth = BasicAuth()
    if auth[1] != True :
        return {
            "response" : "auth error"
        }
    else : 
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

@app.route('/item/search_item', methods=['POST'])
def search_item():
    data = request.get_json()
    inputan = data['search']
    query_item = Item.query.filter(Item.nama_item.ilike("%"+inputan+"%")).all()
    # return jsonify("hello")
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
    # auth = BasicAuth()
    # if auth[1] != True :
    #     return {
    #         "response" : "auth error"
    #     }
    # else :
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
            # harga_item = int(data['harga_item'])
            item.harga_item = data['harga_item']
        
        if 'jumlah_item' in data :
            # jumlah_item = int(data['jumlah_item'])
            item.jumlah_item = data['jumlah_item']
        
        db.session.commit()

        # try :
        #     db.session.commit()
        # except :
        #     return {
        #         "response" : "error"
        #     },401
        return {
            "response" : "success"
        },200

@app.route('/item/delete_item/<id>', methods=['DELETE'])
def delete_item(id):
    # auth = BasicAuth()
    # if not auth :
    #     return jsonify("auth error")
    # else :
        # data = request.get_json()
        
        db.engine.execute(f'''DELETE FROM "item" WHERE item_id = {id}''')
        try :
            db.session.commit()
        except :
            return {
                "response" : "error"
            },401
        return {
            "response" : "success"
        },200


### Order API

# @app.route('/order/add_order', methods=['POST']) # Backend Only
# def add_order():
    # auth = BasicAuth()
    # if not auth :
    #     return jsonify("auth error")
    # else :
        # return {"yes" : auth[0]}
        # data = request.get_json()
        # order = data["orderan"]
        # input_item = data['item_id']
        # input_user = data['user_id']
        # query_item = Item.query.filter_by(item_id=input_item).first()
        # query_user = User.query.filter_by(user_id=auth[0]).first()
        # order = Order(
        #     user_id = auth[0],
        #     order_date = datetime.now()
        # )
        # db.session.add(order)
        # db.session.commit()
        # query_orderid = Order.query.all()
        # arr = []
        # for i in query_orderid :
        #     arr.append(i.order_id)

        # for i in range(len(data["orderan"])) :
        #     query_item = Item.query.filter_by(item_id = data['orderan'][i]).first()
        #     orderdetail = Orderdetail(
        #         order_id = max(arr),
        #         item_id = query_item.item_id,
        #         nama_item = data['orderan'][i],
        #         jumlah_subbarang = data['jumlah_subbarang'][i],
        #         subtotal_harga = data['jumlah_subbarang'][i] * query_item.harga_item
        #     ) 
        #     db.session.add(orderdetail)
        #     db.session.commit()


        # query_orderdetail = Orderdetail.query.filter_by(order_id=max(arr)).all()
        
        # kalkulasi_total = 0
        # kalkulasi_barang = 0
        # for i in query_orderdetail :
        #     kalkulasi_total += i.subtotal_harga
        #     kalkulasi_barang += i.jumlah_subbarang

        # query_order_2 = Order.query.filter_by(order_id = max(arr)).first()
        # query_order_2.total_harga = kalkulasi_total
        # query_order_2.jumlah_barang = kalkulasi_barang

        # try :
            # db.session.add(order)
        #     db.session.commit()
        # except :
        #     return {
        #         "response" : "error"
        #     },401
    #     return {
    #     # "total" : kalkulasi_total,
    #     # "barang" : kalkulasi_barang
    #     "tes" : order
    # },201

@app.route('/order/add_order', methods=['POST'])
def add_order() :
# Format Input :
# {
#     "orderan" :[
#         {"item_id" : 10,
#         "jumlah_subbarang" : 1
#         }
#     ]
# }
    auth = BasicAuth()
    if not auth :
        return jsonify("auth error")
    else :
        # data = request.get_json()
        user_order = CartOrder.query.filter_by(user_id=auth[0]).all()
        user_order_arr = [
            {
            'user_id' : item.user_id,
            'item_id' : item.item_id,
            'nama_item' : item.nama_item,
            'jumlah_barang' : item.jumlah_barang
            } for item in user_order
        ]

        order = Order(
            user_id = auth[0],
            order_date = datetime.now()
        )
        db.session.add(order)
        db.session.commit()

        orderid_target = Order.query.filter_by(user_id=auth[0]).all()
        orderid_arr = []
        for i in orderid_target :
            orderid_arr.append(i.order_id)

        cart_length = len(user_order)
        for i in range(cart_length) :
                query_item = Item.query.filter_by(item_id = user_order_arr[i]['item_id']).first()
                orderdetail = Orderdetail(
                    order_id = max(orderid_arr),
                    item_id = query_item.item_id,
                    nama_item = query_item.nama_item,
                    jumlah_subbarang = user_order_arr[i]['jumlah_barang'],
                    subtotal_harga = user_order_arr[i]['jumlah_barang'] * query_item.harga_item
                ) 
                db.session.add(orderdetail)
                db.session.commit()

        query_orderdetail = Orderdetail.query.filter_by(order_id=max(orderid_arr)).all()

        kalkulasi_total = 0
        kalkulasi_barang = 0
        for i in query_orderdetail :
            kalkulasi_total += i.subtotal_harga
            kalkulasi_barang += i.jumlah_subbarang

        query_order_2 = Order.query.filter_by(order_id = max(orderid_arr)).first()
        query_order_2.total_harga = kalkulasi_total
        query_order_2.jumlah_barang = kalkulasi_barang

        delete_cart = db.engine.execute(f'''DELETE FROM cart_order WHERE user_id={auth[0]}''')

        try :
            db.session.add(order)
            db.session.commit()
            delete_cart
        except :
            return {
                "response" : "error"
            },401
        return {
        "total" : kalkulasi_total,
        "barang" : kalkulasi_barang
        },201

@app.route('/order/add_cart_order', methods=['POST'])
def add_cart_order():
    auth = BasicAuth()
    if not auth :
        return jsonify("auth error")
    else :
        data = request.get_json()
        query_user = User.query.filter_by(user_id=auth[0]).first()
        
        input_item = data["item_id"]
        input_jumlah = data["jumlah_barang"]
        kali_jumlah = int(input_jumlah)
        query_item = Item.query.filter_by(item_id=input_item).first()
        query_cart = CartOrder.query.filter_by(user_id=auth[0]).filter_by(item_id=input_item).first()

        if query_cart != None :
            total_harga = query_item.harga_item * kali_jumlah
            query_cart.jumlah_barang += kali_jumlah
            # query_cart.jumlah_
        else :
            total_harga = query_item.harga_item * kali_jumlah 
            cart_order = CartOrder(
                user_id = auth[0],
                item_id = input_item,
                nama_item = query_item.nama_item,
                jumlah_barang = input_jumlah,
                total_harga = total_harga
            )
            db.session.add(cart_order)

        
        try :
            
            db.session.commit()
        except :
            return {
                "response" : "error"
            },401
        return {
            "response" : "success"
        },200
        # return jsonify({
        #     "user_id" : auth[0],
        #     "item_id" : query_item.item_id,
        #     "nama_item" : query_item.nama_item,
        #     "jumlah_barang" : input_jumlah,
        #     "total_harga" : total_harga
        # }
        # )

@app.route('/order/get_cart_order', methods=['POST'])
def get_cart_order():
    auth = BasicAuth()
    if not auth :
        return jsonify("auth error")
    else :
        # return jsonify(auth[0])
        # return jsonify(auth[0])
 
        # data = request.get_json()
        query_cart = CartOrder.query.filter_by(user_id=auth[0]).all()
        cart_total = db.engine.execute(f'''SELECT SUM(total_harga) FROM cart_order WHERE user_id={auth[0]}''')
        # query_cart = db.engine.execute(f'''SELECT * FROM cart_order WHERE user_id = 2''')
        # return jsonify(query_cart)
        
        # query_cart_arr = [
        #     {
        #     'user_id' : item.user_id,
        #     'item_id' : item.item_id,
        #     'nama_item' : item.nama_item,
        #     'jumlah_barang' : item.jumlah_barang
        #     } for item in query_cart
        #     ]

        result = [list(row) for row in cart_total]
        results = result[0][0]
        # results_dict = {'results': results}
        # return jsonify(results_dict)

        try :
            #  db.engine.execute(f'''SELECT * FROM cart_order WHERE user_id = {auth[0]}''')
             db.session.commit()
        except :
            return {
                "response" : "error"
            },401
        return [
            {
            'cart_order_id' : item.cart_order_id,
            'user_id' : item.user_id,
            'item_id' : item.item_id,
            'nama_item' : item.nama_item,
            'jumlah_barang' : item.jumlah_barang,
            'total_harga' : item.total_harga,
            'cart_total' : results
            } for item in query_cart
            ],201

@app.route('/order/delete_cart_item/<id>', methods=['DELETE'])
def delete_cart_item(id):
    # auth = BasicAuth()
    # if not auth :
    #     return jsonify("auth error")
    # else :
        # data = request.get_json()
        
        # query_user = User.query.filter_by(user_id=auth[0]).first()
        # CartOrder.query.filter_by(cart_order_id=data['cart_order_id']).delete()
        # query_cart = CartOrder.query.filter_by(cart_order_id=id).first()
        db.engine.execute(f'''DELETE FROM cart_order WHERE cart_order_id = {id}''')
        try :
            db.session.commit()
        except :
            return {
                "response" : "error"
            },401
        return {
            "response" : "success"
        },200

        
@app.route('/order/check_order_pending/<id>', methods=['PUT'])
def check_order_pending(id):
    # auth = BasicAuth()
    # if auth[1] != True :
    #     return {
    #         "response" : "auth error"
    #     }
    # else :
        hitung = Order.query.filter_by(order_status = 'activate').count()
        query_order = Order.query.filter_by(order_id=id).first()
        # query_user = User.query.filter(User.user_id==query_order.user_id).first()
        
        if not hitung < 10 :
                return {
                "message" : "antrian penuh"
            }
        elif query_order.order_status == "pending" :
                query_order.order_status = "activate"

        try :
            # db.session.add()
            db.session.commit()
        except :
            return {
                "response" : "error"
            },401
        return {
            "response" : query_order.order_status
        },201
        # return {
        #         "response" : query_order.order_status
        #     },201

@app.route('/order/check_order_activate/<id>', methods=['PUT'])
def check_order_activate(id):
    # auth = BasicAuth()
    # if auth[1] != True :
    #     return {
    #         "response" : "auth error"
    #     }
    # else :
        # data = request.get_json()
        # hitung = Order.query.filter_by(order_status = 'activate').count()
        query_order = Order.query.filter_by(order_id=id).first()
        query_user = User.query.filter(User.user_id==query_order.user_id).first()

        if query_order.order_status == "activate" :
            query_orderdetail = Orderdetail.query.filter(query_order.order_id == Orderdetail.order_id).all()
            for i in query_orderdetail :
                query_item = Item.query.filter(Item.item_id == i.item_id).first()
                if query_item.jumlah_item < i.jumlah_subbarang :
                    # db.session.delete(query_order)
                    db.session.commit()
                    return jsonify("pesanan lebih dari stok")
                    break
                query_item.jumlah_item -= i.jumlah_subbarang
                query_item.jumlah_terbeli += i.jumlah_subbarang
                query_order.order_status = "completed"
                query_user.total_pembelian += 1

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
    data = request.get_json()
    auth = BasicAuth()
    if not auth :
        return jsonify ("auth error")
    else :
        # Order.query.filter(Order.order_status == "pending").filter_by(user_id=auth[0]).filter_by(order_id=data["order_id"]).delete()
        Order.query.filter_by(order_id=data["order_id"]).delete()
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

@app.route('/order/admin_cancel_order/<id>', methods=['DELETE'])
def admin_cancel_order(id):
    # data = request.get_json()
    # auth = BasicAuth()
    # if not auth :
    #     return jsonify ("auth error")
    # else :
        # Order.query.filter(Order.order_status == "pending").filter_by(user_id=auth[0]).filter_by(order_id=data["order_id"]).delete()
    Order.query.filter_by(order_id=id).delete()
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

@app.route('/order/get_all_order', methods=['GET'])
def get_all_order():
    get_all_order = db.engine.execute('''SELECT * FROM "order" INNER JOIN "user" ON "order".user_id = "user".user_id''')
    try :
        db.engine.execute('''SELECT * FROM "order" INNER JOIN "user" ON "order".user_id = "user".user_id''')
        db.session.commit()
    except :
        return {
            "response" : "error"
            },401
    return jsonify([
        {
        'order_id' : order.order_id,
        'user_id' : order.user_id,
        'nama_user' : order.nama_user,
        'order_status' : order.order_status,
        'order_date' : order.order_date,
        'jumlah_barang' : order.jumlah_barang,
        'total_harga' : order.total_harga
        } for order in get_all_order
    ])

@app.route('/order/get_order/<id>', methods=['GET'])
def get_order(id):
    # auth = BasicAuth()
    # if not auth :
    #     return jsonify("auth error")
    # else :
        get_order = db.engine.execute(f'''SELECT * FROM "order" INNER JOIN "user" ON "order".user_id = "user".user_id WHERE "order".user_id = {id}''')
        try :
            db.engine.execute(f'''SELECT * FROM "order" INNER JOIN "user" ON "order".user_id = "user".user_id WHERE "order".user_id = {id}''')
            db.session.commit()
        except :
            return {
                "response" : "error"
                },401
        return jsonify([
            {
            'order_id' : order.order_id,
            'user_id' : order.user_id,
            'nama_user' : order.nama_user,
            'order_status' : order.order_status,
            'order_date' : order.order_date,
            'jumlah_barang' : order.jumlah_barang,
            'total_harga' : order.total_harga
            } for order in get_order
        ])

@app.route('/order/get_orderdetail/<id>', methods=['GET'])
def get_orderdetail(id):
    # auth = BasicAuth()
    # if not auth :
    #     return jsonify("auth error")
    # else :
        get_orderdetail = db.engine.execute(f'''SELECT * FROM orderdetail WHERE order_id = {id}''')
        try :
            db.engine.execute(f'''SELECT * FROM orderdetail WHERE order_id = {id}''')
            db.session.commit()
        except :
            return {
                "response" : "error"
                },401
        return jsonify([
            {
            'order_id' : order.order_id,
            'item_id' : order.item_id,
            'nama_item' : order.nama_item,
            'jumlah_subbarang' : order.jumlah_subbarang,
            'subtotal_harga' : order.subtotal_harga
            } for order in get_orderdetail
        ])



### Reporting API
@app.route('/reporting/top5_user', methods=['GET'])
def top5_user():
    # auth = BasicAuth()
    # if auth[1] != True :
    #     return {
    #         "response" : "auth error"
    #     }
    # else :
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
    # auth = BasicAuth()
    # if auth[1] != True :
    #     return {
    #         "response" : "auth error"
    #     }
    # else :
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
        ]),200

# @app.after_request
# def after_request_func(response):
#     origin = request.headers.get('Origin')
#     if request.method == 'OPTIONS':
#         response.headers.add('Access-Control-Allow-Credentials', 'true')
#         response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
#         response.headers.add('Access-Control-Allow-Headers', 'x-csrf-token')
#         response.headers.add('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Accept, Authorization')
#         response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, PATCH, DELETE')
#         if origin:
#             response.headers.add('Access-Control-Allow-Origin', origin)
#     else:
#         response.headers.add('Access-Control-Allow-Credentials', 'true')
#         if origin:
#             response.headers.add('Access-Control-Allow-Origin', origin)
#     return response