
// 폼 데이터 서버로 전송
const handleSubmitForm = async (event) => {
    event.preventDefault();
    // 시간 데이터 추가 (세계시간 기준)
    const body = new FormData(form);
    body.append('insertAT',new Date().getTime());

    try{
        const res = await fetch('/items',{
            method: "POST",
            // body에 묶어서 한번에 보내기 위해 formData() 객체에 form을 넣어 전송
            body,
        });
    
        const data = await res.json();
        // 서버 코드가 200이면 메인 페이지로 이동
        if (data === "200") window.location.pathname = "/";
    }catch(e) {
        console.error(e);
    }
};

// form 안에서 제출 이벤트 발생했을때 
const form = document.getElementById("write-form");
form.addEventListener("submit",handleSubmitForm);