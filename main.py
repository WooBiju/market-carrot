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
app.mount("/", StaticFiles(directory="static" , html=True), name="static")
