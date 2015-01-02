(function(){

var port = %port%;

var local_probe = new WebSocket("wss://localhost:" + port);

var send = function(msg){
    var json = JSON.stringify(msg);
    local_probe.send(json);
}

document.addEventListener("mousedown", function(event){
    reportElem(event);
});

var reportElem = function(event){
    var elem = event.target;
    var path = buildPath(elem);
    var date = new Date();
    var msg = {};
    msg.event = event.type;
    msg.datetime = date.toISOString();
    msg.elem_location = window.location.hostname + window.location.pathname;
    msg.elem_id = elem.id
    msg.elem_tagName = elem.tagName;
    msg.elem_className = elem.className;
    msg.elem_innerHTML = elem.innerHTML;
    msg.css_location = path;
    send(msg);
};

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
