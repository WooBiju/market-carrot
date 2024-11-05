// 화면에 보여지는 채팅
function displaychat(chat) {
    const ul = document.querySelector("#msg")
    const textbox = document.createElement("li");
    textbox.innerText = chat.content;
    ul.appendChild(textbox);
}


// 4. 서버에 넘어간 데이터를 읽어와야됨 (read -> GET)
async function read_chat() {
    const res = await fetch("/chats");
    const jsonRes = await res.json();
    const ul = document.querySelector("#msg")
    ul.innerText = "";

    jsonRes.forEach(displaychat);
    console.log(jsonRes)
    
}


// 3. 서버에 채팅 만들어달라고 요청 (채팅을 생성하는것 -> POST)
async function createChat(value) {
    const res = await fetch("/chats", {
        method : "POST",
        headers : {
            "Content-Type" : "application/json"
        },
        body : JSON.stringify( {
            content : value,
        }),
    });
    read_chat();
}


// 2. submit 이벤트가 발생했을때 채팅을 서버에 보내줌
function handleSubmit(event) {
    event.preventDefault();
    console.log("전송됨?");
    const input = document.querySelector("#chat-input");
    createChat(input.value);
    input.value = "";
}

const form = document.querySelector("#chat-form");
form.addEventListener("submit",handleSubmit);

read_chat();


// 안되는 이유 ? app.js 파일이 html 두군데 나눠져 있는데 두개가 같이 연동이 안되는건가?
// 그냥 해당 div 태그 안에 onclick 사용해서 오류 해결

// // 1. 클릭시 채팅방으로 이동시켜야 함
// function chatMove() {
//     window.location.href = "chat.html";
// }

// // 이벤트 걸어주기 (채팅 클릭시 채팅방으로 이동)
// const chat = document.querySelector('#chat');
// chat.addEventListener("click",chatMove) // chat에 click 이벤트가 발생하면 chat.html 로 이동
