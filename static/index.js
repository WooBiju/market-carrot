// 시간 계산 하는 로직
const calcTime = (timestamp) => {
    const curTime = new Date().getTime() -9*60*60*1000 ;
    const time = new Date(curTime-timestamp);
    const hour = time.getHours();
    const minutes = time.getMinutes();
    const second = time.getSeconds();

    if (hour > 0) return `${hour}시간 전`
    else if (minutes > 0) return`${minutes}분 전 `
    else if (second > 0) `${second}초 전 `
    else "방금 전";
}


// 데이터 랜더링 해주기
const renderData = (data) => {
    const main = document.querySelector("main")
    data.reverse().forEach(async(obj) => {
        const div = document.createElement('div');
        div.className = "item-list"

        const imgDiv = document.createElement("div");
        imgDiv.className = "item-list__img"

        const img = document.createElement("img");
        const res = await fetch(`/images/${obj.id}`);
        const blob = await res.blob();
        const url = URL.createObjectURL(blob);
        img.src = url;

        const InfoDiv = document.createElement('div');
        InfoDiv.className = "item-list__info";

        const InfoTitleDiv = document.createElement('div');
        InfoTitleDiv.className = "item-list__info-title";
        InfoTitleDiv.innerText = obj.title;

        const InfoMetaDiv = document.createElement('div');
        InfoMetaDiv.className = "item-list__info-meta";
        InfoMetaDiv.innerText = obj.place + " " + calcTime(obj.insertAT);

        const InfoPriceDiv = document.createElement('div');
        InfoPriceDiv.className = "item-list__info-price";
        InfoPriceDiv.innerText = obj.price;

        imgDiv.appendChild(img);
        InfoDiv.appendChild(InfoTitleDiv);
        InfoDiv.appendChild(InfoMetaDiv);
        InfoDiv.appendChild(InfoPriceDiv);

        div.appendChild(imgDiv);
        div.appendChild(InfoDiv);
        
        main.appendChild(div);
        
    })

}


// 서버에 저장된 데이터 불러오기 (read -> GET 요청)
const fetchList =  async () => {
    const res = await fetch("/items");
    const data = await res.json();
    console.log(data);
    renderData(data);
};

fetchList();