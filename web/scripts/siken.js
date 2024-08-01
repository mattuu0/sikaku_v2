// 解答欄を作る場所
const kaitou_tbody = document.getElementById("kaitou_tbody");

//問題を開くボタン
const Open_mondai = document.getElementById('open_mondai_button');
// 問題のURL
let last_qslink = "";

// 答え合わせボタン
const kaitou_button = document.getElementById('kaitou_button');

// 管理ボタン
const control_buttons = document.getElementById('control_buttons');

//pdf viewer
const pdfjs_iframe = document.getElementById('pdfjs-iframe');

// 試験の名前を表示する
const total_siken_name = document.getElementById('total_siken_name');

//答えの情報保持
let kotae_data = {};

function show_mondai(year,sikentag,sikenName,timetag,data, qslink) {
    //確認を表示する
    const clear_confirm = window.confirm("新しい問題を読み込むとあなたの回答が消去されます。\nよろしいですか？");
    if (!clear_confirm) {
        return;
    }

    //前の解答欄を削除する
    RemoveChildren(kaitou_tbody);

    // 答えのデータ設定
    kotae_data = data;

    //問題を回す
    for (const key of Object.keys(data)) {
        // 問題を取得
        const kaitou_data = data[key];

        console.log(kaitou_data);

        // 解答欄のID 生成
        const kaitouid = `kaitou_input_${kaitou_data["num"]}`;

        // 模範解答欄のID 生成
        const mohan_kaitouid = `mohan_input_${kaitou_data["num"]}`;

        // 解答欄のtr id 生成
        const kaitou_trid = `kaitou_tr_${kaitou_data["num"]}`;

        // 模範解答のselect id 生成
        const mohan_selectid = `mohan_select_${kaitou_data["num"]}`;

        //解答欄を生成
        kaitou_tbody.insertAdjacentHTML('beforeend', `
            <tr class="kaitou_row" id=${kaitou_trid}>
                <th scope="row">${kaitou_data["num"]}</th>
                <td class="minaosi_area">
                    <input type="checkbox" class="minaosi_check">
                </td>
                <td>
                    <select name="" id=${kaitouid} class="kaitou_select form-select form-select-lg">
                        <option value="none" selected>未選択</option>
                        <option value="a">ア</option>
                        <option value="i">イ</option>
                        <option value="u">ウ</option>
                        <option value="e">エ</option>
                    </select>
                </td>
                <td>
                    <select name="" id=${mohan_kaitouid} disabled class="form-select form-select-lg mohan_select">
                        <option selected id=${mohan_selectid}>未選択</option>
                    </select>
                </td>
            </tr>`
        );
    }

    // 問題のURL
    last_qslink = qslink;

    console.log(qslink);

    total_siken_name.textContent = `${year}年度 ${sikenName}試験 ${timetag}問題`;

    // コントロールを表示
    Show_Conrtols();
}

Open_mondai.addEventListener('click', async () => {
    if (last_qslink == "") {
        return;
    }

    // pdfjs_iframe.src = "./pdfjs-4.5.136-dist/web/viewer.html?file=" + last_qslink;
    //問題のURLをポップアップ
    window.open(last_qslink, 'mondai_window');
})

kaitou_button.addEventListener('click', async () => {
    for (const key of Object.keys(kotae_data)) {
        const kaitou_data = kotae_data[key];

        console.log(kaitou_data);

        // 解答欄のID 生成
        const kaitouid = `kaitou_input_${kaitou_data["num"]}`;

        // 模範解答欄のID 生成
        const mohan_kaitouid = `mohan_input_${kaitou_data["num"]}`;

        // 解答欄のtr id 生成
        const kaitou_trid = `kaitou_tr_${kaitou_data["num"]}`;

        // 解答欄を取得
        const kaitou = document.getElementById(kaitouid);

        //大本のdivを取得
        const kaitou_tr = document.getElementById(kaitou_trid);

        // 模範解答のselect id 生成
        const mohan_selectid = `mohan_select_${kaitou_data["num"]}`;

        //模範解答を変換
        const mohan_converted = ConvertAns(kaitou_data["ans"]);

        // 模範解答の select を取得
        const mohan_select = document.getElementById(mohan_selectid);

        // クラスを削除する
        kaitou_tr.classList.remove("table-danger");
        kaitou_tr.classList.remove("table-success");

        if (kaitou.value == mohan_converted) {
            //正解
            kaitou_tr.classList.add("table-success");
        } else {
            //不正解
            kaitou_tr.classList.add("table-danger");
        }

        // 答えを設定
        mohan_select.value = mohan_converted;
        mohan_select.textContent = kaitou_data["ans"];
    }
})