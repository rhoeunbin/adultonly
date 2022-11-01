function doOpenCheck(chk) {
    var obj = document.getElementsByName("job");
    for (var i = 0; i < obj.length; i++) {
        if (obj[i] != chk) {
            obj[i].checked = false;
            obj[i].required = "";
        }
    }
}
