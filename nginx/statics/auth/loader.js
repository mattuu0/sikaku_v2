// ロード中の画面を作成
const load_div = document.createElement("div");

//クラスを設定
load_div.className = "loader_screen";

// ロード中の画面の内容
const loader_content = document.createElement("div");
loader_content.className = "loader_content";

// ロード中の画面のくるくる
const spiner_span = document.createElement("span");
spiner_span.className = "loader";
loader_content.appendChild(spiner_span);

// ロード中の画面のテキスト
const load_text = document.createElement("h2");
load_text.textContent = "Loading...";
load_text.className = "loader_text";
loader_content.appendChild(load_text);

// ロード中の画面の追加
load_div.appendChild(loader_content);

// ロード中の画面を非表示
load_div.style.display = "none";

// ロード中の画面を表示
document.body.appendChild(load_div);

function showLoading() {
    // ロード中の画面を表示
    load_div.style.display = "";
}

function hideLoading() {
    // ロード中の画面を非表示
    load_div.style.display = "none";
}

function setLoadText(text) {
    // ロード中のテキストを更新
    load_text.textContent = text;
}

//css を挿入
const style = document.createElement("style");
style.textContent = `
.loader {
    width: 300px;
    height: 300px;
    border: 5px solid #FFF;
    border-bottom-color: transparent;
    border-radius: 50%;
    display: inline-block;
    box-sizing: border-box;
    animation: rotation 1s linear infinite;
    margin: auto;
}

@keyframes rotation {
    0% {
        transform: rotate(0deg);
    }
    100% {
        transform: rotate(360deg);
    }
} 

/* ロード中の画面の設定 */
.loader_screen {
    position: fixed;
    display: flex;
    justify-content: center;
    align-items: center;
    top: 0; 
    left: 0; 
    width: 100%; 
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 9999;
}

/* ロード中のテキストの設定 */
.loader_text {
    color: #FFF;
    font-size: 100px;
    font-weight: bold;
    text-align: center;
    margin-top: 30px;
}

/* ロード画面の中身 */
.loader_content {
    text-align: center;
}
`

// css を挿入
document.head.appendChild(style);