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

// 年月表示
const year_name = document.getElementById('year_name');

// 試験名表示
const select_siken_name = document.getElementById('select_siken_name');

function Show_years() {
    years_container.style.display = "block";
    sikens_container.style.display = "none";
    times_container.style.display = "none";
    control_buttons.style.display = "none";
}

function Show_sikens() {
    years_container.style.display = "none";
    sikens_container.style.display = "block";
    times_container.style.display = "none";
    control_buttons.style.display = "none";
}

function Show_times() {
    years_container.style.display = "none";
    sikens_container.style.display = "none";
    times_container.style.display = "block";
    control_buttons.style.display = "none";
}

function Show_Conrtols() {
    years_container.style.display = "none";
    sikens_container.style.display = "none";
    times_container.style.display = "none";
    control_buttons.style.display = "block";
}

async function Get_Years(siken_tag,siken_name) {
    // ロード画面表示
    setLoadText("データを取得中");
    showLoading();

    try {
        // 年を表示
        Show_years();

        // 試験名表示
        select_siken_name.innerText = siken_name;

        // 年度を全削除
        RemoveChildren(year_buttons);

        const req = await fetch(`/app/years/${siken_tag}`,{
            method: "GET",
            headers: {
                "actoken" : await GetToken()
            }
        })

        const res = await req.json();

        // リストを回す
        for (const year of res) {
            //ボタンを生成
            const abtn = document.createElement('a');
            abtn.className = "select_btn";
            abtn.innerText = year;

            abtn.addEventListener('click',async () => {
                await getTimes(year,siken_tag,siken_name);
            })

            //ボタンを追加
            year_buttons.appendChild(abtn);
        }
    } catch (error) {
        console.log(error);
    }

    // ロード画面非表示
    hideLoading();
}

async function Siken_Data(year) {
    // 試験一覧を全削除
    RemoveChildren(sikens_area);

    // ロード画面表示
    setLoadText("データを取得中");
    showLoading();

    try {
        const req = await fetch(`/app/sikens/${year}`,{
            method: "GET",
            headers: {
                "actoken" : await GetToken()
            }
        })

        const res = await req.json();

        console.log(res);

        // 年表示
        year_name.innerText = `${year}年度`;

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
    } catch (error) {
        console.log(error);
    }

    // ロード画面非表示
    hideLoading();
}

async function getTimes(year,sikentag,sikenName) {
    //問題のURL を削除
    last_qslink = "";

    // 試験の時間を全削除
    RemoveChildren(times_area);

    // ロード画面表示
    setLoadText("データを取得中");
    showLoading();

    try {

        // 試験名表示
        siken_name.innerText = `試験名 : ${year}年度 : ${sikenName}`;

        // リクエスト送信
        const req = await fetch(`/app/times/${year}/${sikentag}`,{
            method: "GET",
            headers : {
                "actoken" : await GetToken()
            }
        })

        // 試験の時間を取得
        const res = await req.json();

        // 試験の時間を回す
        for (const time_tag of Object.keys(res)) {
            // 問題のデータ取得
            const mondai_data = await GetSiken(year,sikentag,sikenName,time_tag,res[time_tag]);

            // 試験を生成
            const abtn = document.createElement('a');
            abtn.className = "select_btn";

            // 問題のデータがない場合
            if (mondai_data["count"] == 0) {

                abtn.innerHTML = `
                    ${res[time_tag]} 
                    <span style="color:red;">${mondai_data["count"]}</span>問
                `;
            } else {
                // 問題数表示
                abtn.innerText = `${res[time_tag]} ${mondai_data["count"]}問`;

                //イベント追加
                abtn.addEventListener('click',async () => {
                    // 問題を取得
                    const data = await GetSiken(year,sikentag,sikenName,time_tag,res[time_tag]);

                    // 問題を生成
                    show_mondai(year,sikentag,sikenName,time_tag,time_tag,data["data"],data["qslink"]);
                })
            }

            // 試験を追加
            times_area.appendChild(abtn);
        }

        Show_times();
    } catch (error) {
        console.log(error);
        alert("問題の取得に失敗しました。");
    }

    // ロード画面非表示
    hideLoading();
}

async function GetSiken(year,sikentag,sikenName,time_tag,timeName) {
    const req = await fetch(`/app/siken/${year}/${sikentag}/${time_tag}`,{
        method: "GET",
        headers : {
            "actoken" : await GetToken()
        }
    })

    const res = await req.json();

    return res;
}

async function main() {
    // ボタンを全削除
    RemoveChildren(sikens_area);

    // ロード画面表示
    setLoadText("データを取得中");
    showLoading();

    try {

        // リクエスト送信
        const req = await fetch("/app/sikens",{
            method: "GET",
            headers : {
                "actoken" : await GetToken()
            }
        });

        const res = await req.json();

        console.log(res);

        // 試験を回す
        for (const siken_tag of Object.keys(res)) {
            //ボタンを生成
            const abtn = document.createElement('a');
            abtn.className = "select_btn";
            abtn.innerText = res[siken_tag] + "年";

            //ボタンを追加
            sikens_area.appendChild(abtn);

            //イベント追加
            abtn.addEventListener('click',async () => {
                await Get_Years(siken_tag,res[siken_tag]);
            })
        }
        
    } catch (error) {
        console.log(error);
    }

    // ロード画面非表示
    hideLoading();
}

main();