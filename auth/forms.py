from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, Length, Regexp

# 회원가입
class SignUpForm(FlaskForm):
    id = StringField(
        "아이디",
        validators=[
            DataRequired("아이디 입력은 필수입니다."),
            Length(1, 30, "30문자 이내로 입력해 주세요.")
        ]
    )
    password = PasswordField(
        "비밀번호",
        validators=[DataRequired("비밀번호는 필수입니다.")]
    )
    username = StringField(
        "이름",
        validators=[
            DataRequired("사용자명을 입력해주세요."),
            Length(1, 30, "30문자 이내로 입력해 주세요.")
        ]
    )
    phonenumber = StringField(
        "휴대전화",
        validators=[
            DataRequired("휴대폰 번호를 입력해주세요."),
            Length(10, 13),
            Regexp('^010[0-9]{3,4}[0-9]{4}$')
        ]
    )
    email = StringField(
        "이메일",
        validators=[
            DataRequired("메일 주소는 필수입니다."),
            Email("메일 주소의 형식으로 입력해 주세요.")
        ]
    )    
    submit = SubmitField("회원가입")

# 로그인
class LoginForm(FlaskForm):
    id = StringField("아이디",validators=[DataRequired("아이디 입력은 필수입니다")])
    password = PasswordField("비밀번호", validators=[DataRequired("비밀번호는 필수입니다.")])
    submit = SubmitField("로그인")