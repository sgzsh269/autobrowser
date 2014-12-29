(function(){

var port = %port%;

var local_probe = new XMLHttpRequest();

var send = function(queryString){
    local_probe.open("GET", "https://localhost:" + port + "?" + queryString,
    true);
    local_probe.send();
}

window.addEventListener("unload", function(event){
send("event=unload");

});

document.addEventListener("click", function(event){
    var elem = event.target;
    var path = buildPath(elem);
    var date = new Date();
    var queryString = "";
    queryString += "event=" + "click" + "&";
    queryString += "datetime=" + date.toISOString() + "&";
    queryString += "elem_location=" + window.location.hostname + window.location.pathname + "&";
    queryString += "elem_id=" + elem.id + "&";
    queryString += "elem_tagName=" + elem.tagName + "&";
    queryString += "elem_className=" + elem.className + "&";
    queryString += "elem_innerHTML=" + elem.innerHTML + "&";
    queryString += "elem_locator=" + path;
    send(queryString);
});

var buildPath = function(target){
    var path = "";
    while(target.tagName != "BODY"){
        var count = 0;
        var index = findIndex(target);
        var tagName = target.tagName;
        path = ">" + tagName + ":nth-child(" + index + ")" + path;
        parent = target.parentElement;
        target = parent
    }
    return "BODY" + path;
}

var findIndex = function(target){
    var count = 0;

    while(target){
        count++;
        sibling = target.previousElementSibling;
        target = sibling
    }
    return count;
}
})();
