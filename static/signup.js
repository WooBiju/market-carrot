const form = document.querySelector('#signup-form');

// 패스워드 = 패스워드 확인 일치시 회원가입 승인
const checkPassword = () => {
    const formData = new FormData(form);
    const password1 = formData.get('password');
    const password2 = formData.get('password2');
    if (password1 === password2){
        return true;
    } else return false;
 }

// submit 이벤트 발생했을때 데이터 서버에 넘겨주는 로직
const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData(form);

    const sha256Password = sha256(formData.get('password'));

    // 비밀번호 암호화
    formData.set('password',sha256Password);
    console.log(formData.get('password'));

    const div = document.querySelector("#info")

    // 비밀번호 맞는지 체크 
    if(checkPassword()) {
        const res = await fetch("/signup",{
            method : "POST",
            body : formData
        });

        const data = await res.json(); // 서버에서 받은 데이터 확인하고 처리
        if (data ==='200') {
            alert('회원 가입에 성공했습니다.')
            window.location.pathname ="/login.html";
        }

    } else {
        div.innerText = "비밀번호가 같지 않습니다";
        div.style.color = "red";
    }
}
    form.addEventListener("submit",handleSubmit)