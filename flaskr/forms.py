from wtforms.form import Form
from wtforms.fields import StringField, PasswordField, SubmitField, HiddenField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
from flask_admin.form import widgets
from wtforms import ValidationError
from flaskr.models import User
from wtforms.fields.html5 import DateTimeLocalField

# ログイン画面で利用
class LoginForm(Form):
    email = StringField('メール: ', validators=[DataRequired(), Email()])
    password = PasswordField('パスワード: ', validators=[DataRequired()])
    submit = SubmitField('ログイン')

# 登録画面で利用
class RegisterForm(Form):
    email = StringField('メール: ', validators=[DataRequired(), Email('メールアドレスが誤っています')])
    username = StringField('名前: ', validators=[DataRequired()])
    password = PasswordField(
        'パスワード: ', validators=[DataRequired(), EqualTo('password_confirm', message='パスワードが一致しません')]
    )
    password_confirm = PasswordField('パスワード確認: ', validators=[DataRequired()])
    submit = SubmitField('登録')

    def validate_email(self, field):
        if User.select_by_email(field.data):
            raise ValidationError('メールアドレスは既に登録されています')


class SearchForm(Form):
    area = StringField('エリア: ')
    from_time = DateTimeLocalField('利用時間: ', format='%Y-%m-%dT%H:%M')
    to_time = DateTimeLocalField('', format='%Y-%m-%dT%H:%M')
    kensa = StringField('検査: ')
    shikkan = StringField('疾患・専門: ')
    chiryo = StringField('治療: ')
    submit = SubmitField('検索')


class HospitalRegisterForm(Form):
    submit = SubmitField('予約する')

class MessageForm(Form):
    to_user_id = HiddenField()
    message = TextAreaField()
    submit = SubmitField('送信する')
