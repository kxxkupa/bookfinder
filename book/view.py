import uuid
import os

from flask import Blueprint, render_template, request, redirect, url_for, send_from_directory, current_app, flash
from flask_login import login_required, current_user
from pathlib import Path

from apps.app import db
from apps.auth.models import User
from apps.book.forms import BoardWrite
from apps.book.models import Board

book = Blueprint(
    "book",
    __name__,
    template_folder="templates",
    static_folder="static"
)

@book.route("/users/<userId>/list")
@login_required
def index(userId):
    # 이미지 경로, 날짜 형식 변경
    my_board = Board.query.all()

    # 이미지 경로
    for image in my_board:
        file_path = image.boardImage                                                # 기존 경로 가져오기
        directory, file_name = os.path.split(file_path)                             # 기존 경로 분리 (경로, 파일명)
        new_path = os.path.join("book", "static", "images", "thumnail", file_name)  # 새로운 경로로 변경 (static\images\thumnail\파일명)
            
        # 새로운 경로로 변경된 데이터 넣기 (실제 DB에선 변동 없음! 호출되는 데이터만 변동!)
        image.boardImage = "\\" + new_path

    # 날짜 형식 (YYYY-MM-DD)
    for board in my_board:
        board.boardCreate = board.boardCreate.strftime("%Y-%m-%d")

    # 로그인한 유저가 작성한 게시글 불러오기
    user = User.query.get(userId)

    if user:
        posts = user.posts
        total = len(posts)
        return render_template("board_list.html", posts=posts, total=total)
    else:
        return print("사용자를 찾을 수 없습니다.")

@book.route("/images/<path:filename>")
def image_file(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)

@book.route("/users/<userId>/write", methods=["GET", "POST"])
@login_required
def board_write(userId):
    form = BoardWrite()

    if form.validate_on_submit():
        # 이미지 파일 저장 과정
        file = form.bookimage.data                                      # 이미지 파일 정보
        ext = Path(file.filename).suffix                                # 이미지 파일 확장자
        image_uuid_file_name = str(uuid.uuid4()) + ext                  # 이미지 파일 고유 식별자 생성
        image_path = Path(                                              # 이미지 파일 저장 경로
            current_app.config["UPLOAD_FOLDER"], image_uuid_file_name
        )

        boardData = Board(
            boardTitle = form.booktitle.data,
            boardContent = form.bookcontent.data,
            boardRating = form.bookrating.data,
            boardImage = image_path,
            userId = current_user.userId
        )

        db.session.add(boardData)
        db.session.commit()

        file.save(image_path)                                           # /book/static/images/thumnail 폴더에 이미지 파일 저장

        next_ = request.args.get("next")
        if next_ is None or not next_.startswith("/") :
            next_ = url_for("book.index", userId=userId)
        return redirect(next_)

    return render_template("board_write.html", form=form)

@book.route("/users/<userId>/view/<int:boardId>")
@login_required
def board_view(userId, boardId):
    board = Board.query.get(boardId)
    
    if board:
        return render_template("board_view.html", board=board)

@book.route("/users/<userId>/update/<int:boardId>", methods=["GET", "POST"])
@login_required
def board_update(userId, boardId):
    form = BoardWrite()
    board = Board.query.filter_by(userId=userId, boardId=boardId).first()
    
    if board:
        if form.validate_on_submit():
            # 이미지 파일 저장 과정
            file = form.bookimage.data                                      # 이미지 파일 정보
            ext = Path(file.filename).suffix                                # 이미지 파일 확장자
            image_uuid_file_name = str(uuid.uuid4()) + ext                  # 이미지 파일 고유 식별자 생성
            image_path = Path(                                              # 이미지 파일 저장 경로
                current_app.config["UPLOAD_FOLDER"], image_uuid_file_name
            )
            
            board.boardTitle = form.booktitle.data,
            board.boardContent = form.bookcontent.data,
            board.boardRating = form.bookrating.data,
            board.boardImage = image_path,
            board.userId = current_user.userId

            db.session.commit()

            file.save(image_path)                                           # /book/static/images/thumnail 폴더에 이미지 파일 저장

            return redirect(url_for("book.board_view", userId=userId, boardId=boardId))
    
        return render_template("board_update.html", form=form, board=board, boardId=boardId)
    
@book.route("/users/<userId>/delete/<int:boardId>")
def board_delete(userId, boardId):
    board = Board.query.filter_by(userId=userId, boardId=boardId).first()

    if board:
        db.session.delete(board)
        db.session.commit()
        
        return redirect(url_for("book.index", userId=userId))
    
@book.route("/bookfinder")
def book_finder():
    return render_template("finder.html", page="bookfinder")