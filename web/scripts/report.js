const export_button = document.getElementById('export_button');

export_button.addEventListener('click',async () => {
    console.log("click");

    html2canvas(document.body).then(function(canvas) {
        document.body.appendChild(canvas);
    });
})