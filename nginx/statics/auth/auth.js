const { Client,Account,OAuthProvider } = Appwrite;

const client = new Client();
client
    .setEndpoint('https://auth.tail6cf7b.ts.net/v1')
    .setProject('66ac7b390016d21c7c7b');

const account = new Account(client);

function Start_Oauth() {
// Go to OAuth provider login page
    account.createOAuth2Session(
        OAuthProvider.Microsoft, // provider
        window.location.origin + "/statics/", // redirect here on success
        window.location.href, // redirect here on failure
        [] // scopes (optional)
    );
}

async function Logout() {
    const result = await account.deleteSession(
        'current' // sessionId
    );
    
    console.log(result);

    window.onbeforeunload = function(evt) {

    };

    window.location.reload();
}

async function GetToken() {
    try {
        //アクセストークン取得
        const result = await account.createJWT();

        //トークン返却
        return result["jwt"];
    } catch (ex) {
        //ログイン画面に飛ばす
        window.location.href = "/statics/auth/auth.html";
    }

    return "";
}
