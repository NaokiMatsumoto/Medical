from flask import Blueprint, request, render_template, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from flaskr.forms import LoginForm, SearchForm, RegisterForm, HospitalRegisterForm, MessageForm
from flaskr.models import User, Hospitals, HospitalRegists, db, Messages
from sqlalchemy import and_, or_

bp = Blueprint('app', __name__, url_prefix='')

@bp.route('/')
def home():
    return render_template('home.html')

# ログインしていないと実行されない(login_userが実行されていないと)
# ログインしていない場合はlogin関数に飛ばされる
@bp.route('/welcome')
@login_required
def welcome():
    return render_template('welcome.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user() # ログアウトできる
    return redirect(url_for('app.home'))

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.select_by_email(form.email.data)
        # emailから取得したUserのパスワードとクライアントが入力したパスワードが一致するか
        if user and user.validate_password(form.password.data):
            login_user(user, remember=True)
            next = request.args.get('next') # 次のURL
            if not next:
                next = url_for('app.welcome')
            return redirect(next)
    return render_template('login.html', form=form)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User(
            email = form.email.data,
            username = form.username.data,
            password = form.password.data
        )
        user.add_user()
        return redirect(url_for('app.login'))
    return render_template('register.html', form=form)


@bp.route('/hospital_detail/<int:hospital_id>', methods=['GET', 'POST'])
@login_required
def hospital_detail(hospital_id):
    hospital = Hospitals.query.get(hospital_id)
    form = HospitalRegisterForm(request.form)
    registmodel = HospitalRegists.query.filter(
        HospitalRegists.from_hospital_id==current_user.id, HospitalRegists.to_hospital_id==hospital.id).first()
    if registmodel and registmodel.regist_flg:
        form.submit.label.text = '予約取消'
    if request.method == 'POST':
        if not registmodel:
            registmodel = HospitalRegists(True, current_user.id, hospital.id)
            db.session.add(registmodel)
            db.session.commit()
        else:
            registmodel.regist_flg = False if registmodel.regist_flg else True
            db.session.commit()
    return render_template('hospital_detail.html', hospital=hospital, form=form, regist=registmodel)


@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm(request.form)
    map = None
    if request.method == 'POST' and form.validate():
        from flask_googlemaps import GoogleMaps, Map
        devices_data = {} # dict to store data of devices
        devices_location = {} # dict to store coordinates of devices
        # json_data = request.get_json(silent=True)
        # get json request
        kensa = form.kensa.data
        chiryo = form.chiryo.data
        shikkan = form.shikkan.data
        area = form.area.data
        from_time = form.from_time.data
        to_time = form.to_time.data
        hospital = Hospitals.query.first()
        json_data = { # for testing
            'user' : {
                'x' : 35.94149,
                'y' : 139.771598
            },
            'devices' : [
                {
                    'id' : '0001',
                    'x' : hospital.latitude,
                    'y' : hospital.longitude,
                    'data' : 'something'
                }
            ]
        }

        user_location = (json_data['user']['x'], json_data['user']['y'])
        # json example : { 'user' : { 'x' : '300' , 'y' : '300' } }
        # get user_location from json & store as turple (x, y)

        devices_data[str(json_data['devices'][0]['id'])] = (
            json_data['devices'][0]['data']
        )

        devices_location[str(json_data['devices'][0]['id'])] = (
            json_data['devices'][0]['x'], 
            json_data['devices'][0]['y']
        )
        # json example : { 'devices' : { 'id' : '0001', x' : '500', 'y' : '500' }, { ... } }
        # get device_location from json & store turple (x, y) in dictionary with device id as key
        # use for statements or something to get more locations from more devices

        circle = { # draw circle on map (user_location as center)
            'stroke_color': '#0000FF',
            'stroke_opacity': .5,
            'stroke_weight': 5,
            # line(stroke) style
            'fill_color': '#FFFFFF', 
            'fill_opacity': .2,
            # fill style
            'center': { # set circle to user_location
                'lat': user_location[0],
                'lng': user_location[1]
            }, 
            'radius': 100 # circle size (50 meters)
        }

        map = Map(
            identifier = "map", varname = "map",
            # set identifier, varname
            lat = user_location[0], lng = user_location[1], 
            # set map base to user_location
            zoom = 12, # set zoomlevel
            markers = [
                {
                    'lat': devices_location['0001'][0],
                    'lng': devices_location['0001'][1],
                    'infobox': devices_data['0001']
                }
            ], 
            # set markers to location of devices
            circles = [circle] # pass circles
        )

        return render_template('search.html', map=map, form=form, hospital=hospital)
    return render_template('search.html', form=form)


@bp.route('/send_message/<int:from_id>/<int:to_id>', methods=['GET', 'POST'])
@login_required
def send_messages(from_id, to_id):
    messages = Messages.query.filter(
            or_(
                and_(
                    Messages.from_hospital_id == from_id,
                    Messages.to_hospital_id == to_id
                ),
                and_(
                    Messages.from_hospital_id == to_id,
                    Messages.to_hospital_id == from_id
                )
            )
        )
    form = MessageForm(request.form)
    print(messages)
    if request.method == 'POST' and form.validate():
        new_message = Messages(form.message.data, from_id, to_id)
        
        db.session.add(new_message)
        db.session.commit()
    return render_template('messages.html', form=form, messages=messages, to_user_id=to_id)
