from fastapi import FastAPI,UploadFile,Form,Response
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Annotated
import sqlite3

# 데이터베이스랑 연결
con = sqlite3.connect("db.db",check_same_thread=False)
cur = con.cursor()

# Chat 클래스 속성 타입 지정
class Chat(BaseModel):
    content : str

# 채팅 담을 배열
chats = []

app = FastAPI()

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
async def get_items():
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

# 회원가입 
@app.post("/signup")
def signup(id:Annotated[str,Form()],
           password:Annotated[str,Form()],
           name:Annotated[str,Form()],
           email:Annotated[str,Form()]):
    cur.execute(f"""
                INSERT INTO users(id,name,email,password)
                VALUES('{id}','{name}','{email}','{password}')
                """)
    con.commit()
    print(id,password)
    return '200'


app.mount("/", StaticFiles(directory="static" , html=True), name="static")
