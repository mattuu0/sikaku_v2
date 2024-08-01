function beforeUnload(event){
    event.preventDefault();
    event.returnValue = 'Check';
}

window.onbeforeunload = beforeUnload;