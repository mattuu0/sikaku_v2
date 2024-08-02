// ロードを表示
showLoading();
setLoadText("ロード中");

async function Init() {
    //メインのdiv 取得
    const main_content = document.getElementById("main_content");

    try {
        // 現在のセッション取得
        const session = await account.getSession('current');

        // Provider information
        console.log(session.provider);
        console.log(session.providerUid);
        console.log(session.providerAccessToken);

        // ロードを隠す
        hideLoading();

        // メインコンテンツ表示
        main_content.style.display = "";
    } catch (ex) {
        window.location.href = "/statics/auth/auth.html";
    }
}

window.addEventListener("DOMContentLoaded",Init)