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