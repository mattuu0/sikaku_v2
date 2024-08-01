function RemoveChildren(node) {
    while (node.firstChild) {
        node.removeChild(node.lastChild);
    }
}

function ConvertAns(ans) {
    switch (ans) {
        case "ア":
            return "a";
        case "イ":
            return "i";
        case "ウ":
            return "u";
        case "エ":
            return "e";
        default:
            return "";
    }
}

function ReverseAns(ans) {
    switch (ans) {
        case "a":
            return "ア";
        case "i":
            return "イ";
        case "u":
            return "ウ";
        case "e":
            return "エ";
        case "none":
            return "未選択";
        default:
            return "不明";
    }
}