from fastapi import FastAPI,UploadFile,Form,Response,Depends
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager # 로그인 라이브러리
from fastapi_login.exceptions import InvalidCredentialsException # 예외처리
from pydantic import BaseModel
from typing import Annotated
import sqlite3
import hashlib

# 데이터베이스랑 연결
con = sqlite3.connect("db.db",check_same_thread=False)
cur = con.cursor()

# Chat 클래스 속성 타입 지정
class Chat(BaseModel):
    content : str

# 채팅 담을 배열
chats = []

app = FastAPI()

# password hash 암호화 적용시키는 함수
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 암호화를 위해 시크릿 코드가 하나 필요
SECRETE = "super-coding"
# 아래의 코드중 /login 해당 경로에서만 토큰이 발급되도록 설정
manager = LoginManager(SECRETE,'/login')

# 로그인시 해당 유저가 존재하는지 조회 하는 함수
@manager.user_loader() # 조회할때 키를 같이 조회
def query_user(data):
    # str 으로 값이 들어올 경우
    WHERE_STATEMENTS = f'id="{data}"'
    
    # 'sub' : { 'id':user['id'], ..... } 처럼 dict 형태일 경우
    if type(data) == dict:
        WHERE_STATEMENTS = f'id="{data['id']}"'
        
    con.row_factory = sqlite3.Row # 컬럼명 가져옴
    cur = con.cursor() # 쿼리 (업데이트)
    user = cur.execute(f"""
                       SELECT * from users WHERE {WHERE_STATEMENTS}
                       """).fetchone()
    return user

# 로그인 
@app.post('/login')
def login(id:Annotated[str,Form()],
           password:Annotated[str,Form()]):
    user = query_user(id)
    print(user['password'])
    # user 존재의 유무
    if not user:
        # raise: 에러메시지 던지는 문법
        raise InvalidCredentialsException # 401 (Unauthorized) 생성해서 내려줌
    elif password != user['password']:
        raise InvalidCredentialsException
    # return 'hi' # 서버에서 따로 지정해주지 않으면 자동으로 200 상태 코드 보여줌
    
    # access_token 만들어서 data 넣어줌 (jwt -> 토큰안에 유저정보 넣어서 보관)
    access_token = manager.create_access_token(data={
        'sub' : {
             'id':user['id'],
            'name': user['name'],
            'email':user['email']
        }
    })
    return {'access_token':access_token}

# 회원가입 
@app.post("/signup")
def signup(id:Annotated[str,Form()],
           password:Annotated[str,Form()],
           name:Annotated[str,Form()],
           email:Annotated[str,Form()]):
    cur.execute(f"""
                INSERT INTO users(id,name,email,password)
                VALUES('{id}','{name}','{email}','{hash_password(password)}')
                """)
    con.commit()
    print(id,hash_password(password))
    return '200'

@app.get("/chats")
def read_chat():
    return chats

@app.post("/chats")
def create_chat(chat:Chat):
    chats.append(chat)
    return  "채팅 전송 완료"


@app.post('/items')
# 파라미터로 해당 내용들을 받아서 터미널에 출력
async def create_item(image:UploadFile,
                title:Annotated[str,Form()],
                price:Annotated[int,Form()],
                description:Annotated[str,Form()],
                place:Annotated[str,Form()],
                insertAT:Annotated[int,Form()]):
    image_bytes = await image.read() # 이미지를 읽는 시간이 필요함 (이미지 -> byte 로 변경)
    # 읽어온 데이터를 데이터 테이블에 넣어줘야 함
    cur.execute(f"""
                INSERT INTO items (title,image,price,description,place,insertAT) 
                VALUES ('{title}','{image_bytes.hex()}',{price},'{description}','{place}',{insertAT})
                """)
    con.commit()
    return '200'

@app.get("/items")
# user=Depends(manager) : user 가 인증된 상태에서만 응답을 보낼수 있도록 함
async def get_items(user=Depends(manager)):
    con.row_factory = sqlite3.Row # 컬럼명 가져옴
    cur = con.cursor() # 쿼리문 실행시키려면 커서 객체를 통해 연결해줘야 함
    # 전체 데이터 불러옴 (컬럼명 같이 불러와야 구별가능)  
    rows = cur.execute(f"""
                        SELECT * from items
                        """).fetchall()
    # ex ) [['id',1],['title':'자몽팝니다'] , ....]  -> array 형태
    
    # Json 응답으로 변경해서 내보냄(dict : array 형태를 객체형태로 변경)
    return JSONResponse(jsonable_encoder(dict(row) for row in rows))

# 이미지에 맞는 id 요청해서 이미지 불러오기
@app.get("/images/{item_id}")
async def get_image(item_id):
    cur = con.cursor()
    image_bytes = cur.execute(f"""
                              SELECT image from items WHERE id={item_id}
                              """).fetchone()[0] # 이미지 한개만 불러옴
    # image_bytes(16진법) ->  바이트로 변경
    return Response(content=bytes.fromhex(image_bytes))




app.mount("/", StaticFiles(directory="static" , html=True), name="static")
