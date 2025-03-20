from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField, FileRequired
from wtforms import StringField, RadioField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

# 글쓰기
class BoardWrite(FlaskForm):
    booktitle = StringField(
        "책 제목",
        validators=[DataRequired("책 제목 입력은 필수입니다.")]
    )
    bookimage = FileField(
        "책 이미지",
        validators=[
            FileRequired("도서 이미지를 업로드 해주세요."),
            FileAllowed(["png", "jpg", "jpeg"], "지원되지 않는 이미지 형식입니다.")    
        ]
    )
    bookrating = RadioField(
        "평점",
        choices=[
            ("1", "1점"),
            ("2", "2점"),
            ("3", "3점"),
            ("4", "4점"),
            ("5", "5점")
        ],
        validators=[DataRequired("평점을 선택해주세요.")]
    )
    bookcontent = TextAreaField(
        "후기",
        validators=[
            DataRequired("책을 읽고 난 후기를 입력해 주세요."),
        ]
    )
    submit = SubmitField("저장")