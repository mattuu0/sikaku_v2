// 年データ
const years_container = document.getElementById('years_container');

// 年データ (ボタン置く場所)
const year_buttons = document.getElementById('year_buttons');

// 試験一覧
const sikens_container = document.getElementById('sikens_container');

// 試験 (ボタン置く場所)
const sikens_area = document.getElementById('sikens_area');

// 試験の時間 
const times_container = document.getElementById('times_container');

// 試験の時間 (ボタン置く場所)
const times_area = document.getElementById('times_area');

// 試験名表示
const siken_name = document.getElementById('siken_name');

function Show_years() {
    years_container.style.display = "block";
    sikens_container.style.display = "none";
    times_container.style.display = "none";
}

function Show_sikens() {
    years_container.style.display = "none";
    sikens_container.style.display = "block";
    times_container.style.display = "none";
}

function Show_times() {
    years_container.style.display = "none";
    sikens_container.style.display = "none";
    times_container.style.display = "block";
}

async function Siken_Data(year) {
    // 試験一覧を全削除
    RemoveChildren(sikens_area);

    const req = await fetch(`http://127.0.0.1:8000/sikens/${year}`,{
        method: "GET",
    })

    const res = await req.json();

    console.log(res);

    // 試験を回す
    for (const siken_key of Object.keys(res)) {
        // 試験を生成
        const abtn = document.createElement('a');
        abtn.className = "select_btn";
        abtn.innerText = res[siken_key];

        abtn.addEventListener('click',async () => {
            await getTimes(year,siken_key,res[siken_key]);
        })

        // 試験を追加
        sikens_area.appendChild(abtn);
    }

    Show_sikens();
}

async function getTimes(year,sikentag,sikenName) {
    //問題のURL を削除
    last_qslink = "";

    // こんとろーらーを隠す
    control_buttons.style.display = "none";

    // 試験の時間を全削除
    RemoveChildren(times_area);

    // 試験名表示
    siken_name.innerText = `試験名 : ${year}年度 : ${sikenName}`;

    // リクエスト送信
    const req = await fetch(`http://127.0.0.1:8000/times/${year}/${sikentag}`,{
        method: "GET",
    })

    // 試験の時間を取得
    const res = await req.json();

    // 試験の時間を回す
    for (const time_tag of Object.keys(res)) {
        // 試験を生成
        const abtn = document.createElement('a');
        abtn.className = "select_btn";
        abtn.innerText = res[time_tag];

        abtn.addEventListener('click',async () => {
            await GetSiken(year,sikentag,time_tag);
        })

        // 試験を追加
        times_area.appendChild(abtn);
    }

    Show_times();
}

async function GetSiken(year,sikentag,time_tag) {
    const req = await fetch(`http://127.0.0.1:8000/siken/${year}/${sikentag}/${time_tag}`,{
        method: "GET",
    })

    const res = await req.json();

    console.log(res);

    //問題を表示する
    show_mondai(res["data"],res["qslink"]);
}

async function main() {
    // ボタンを全削除
    RemoveChildren(year_buttons);

    // リクエスト送信
    const req = await fetch("http://127.0.0.1:8000/years",{
        method: "GET",
    });

    const res = await req.json();

    console.log(res);

    // 年を回す
    for (const year of res) {
        //ボタンを生成
        const abtn = document.createElement('a');
        abtn.className = "select_btn";
        abtn.innerText = year;

        //ボタンを追加
        year_buttons.appendChild(abtn);

        //イベント追加
        abtn.addEventListener('click',async () => {
            await Siken_Data(year);
        })
    }
}

main();