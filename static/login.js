const form = document.querySelector('#login-form');

// submit 이벤트 발생했을때 데이터 서버에 넘겨주는 로직
const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const sha256Password = sha256(formData.get('password'));
    formData.set('password',sha256Password);
    
    const res = await fetch("/login",{
        method : "POST",
        body : formData
    });
    const data = await res.json(); // 서버에서 받은 데이터
    const accessToken = data.access_token;  //  받은 데이터 토큰에 넣어서 저장

    // localStorage 에 토큰을 넣어줌
    window.localStorage.setItem("token",accessToken);
    alert('로그인 되었습니다')

    console.log(accessToken);
    // {access_token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.
    //                 eyJteW5hbWUiO…2MTN9.ZEZHoZC_YIEnhf2bf7Gh-b_2QzrtCCm9HnhRVIS94P4'}

    
    window.location.pathname = "/"

    }
    form.addEventListener("submit",handleSubmit)