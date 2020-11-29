# models.py
from flaskr import db, login_manager
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_login import UserMixin

# セッションに保存されたログインユーザを返すためにtemplateから呼ばれる
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# UserMixinはFLask-Loginライブラリを利用するユーザが持つべきオブジェクトを定義
class User(UserMixin, db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), index=True)
    password = db.Column(db.String(128))

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)

    def add_user(self):
        with db.session.begin(subtransactions=True):
            db.session.add(self)
        db.session.commit()
    
    @classmethod
    def select_by_email(cls, email):
        return cls.query.filter_by(email=email).first()


class Hospitals(db.Model):

    __tablename__ = 'hospitals'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    area = db.Column(db.String(64))
    content = db.Column(db.Text)
    longitude = db.Column(db.Float)
    latitude = db.Column(db.Float)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)


class Kensa(db.Model):
    __tablename__ = 'kensas'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)


class Shikkan(db.Model):
    __tablename__ = 'shikkans'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)


class Chiryo(db.Model):
    __tablename__ = 'chiryos'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)


class OpenTime(db.Model):

    __tablename__ = 'opentimes'

    id = db.Column(db.Integer, primary_key=True)
    from_time = db.Column(db.DateTime)
    to_time = db.Column(db.DateTime)
    kensa_id = db.Column(db.Integer, db.ForeignKey('kensas.id'), nullable=False)


class HospitalRegists(db.Model):
    __tablename__ = 'hospital_regists'

    id = db.Column(db.Integer, primary_key=True)
    regist_flg = db.Column(db.Boolean, default=False)
    from_hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
    to_hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)

    def __init__(self, regist_flg, from_hospital_id, to_hospital_id):
        self.regist_flg = regist_flg
        self.from_hospital_id = from_hospital_id
        self.to_hospital_id = to_hospital_id



class Messages(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text)
    from_hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)
    to_hospital_id = db.Column(db.Integer, db.ForeignKey('hospitals.id'), nullable=False)

    def __init__(self, message, from_hospital_id, to_hospital_id):
        self.message = message
        self.from_hospital_id = from_hospital_id
        self.to_hospital_id = to_hospital_id
