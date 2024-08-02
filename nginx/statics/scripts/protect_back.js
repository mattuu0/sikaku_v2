function beforeUnload(event){
    event.preventDefault();
    event.returnValue = 'Check';
}

window.addEventListener("DOMContentLoaded",function(evt){
    window.onbeforeunload = beforeUnload;
})