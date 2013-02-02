
var redraw, g, renderer, current_result;

function makeGraphOfKeywords(arrayWords){
    for (var i = 0; i < arrayWords.length; i++) {
        if( arrayWords[i] != undefined) {
            g.addNode(arrayWords[i]);
        }
    }

    var rel = { directed: true, stroke : "#bfa" , fill : "#56f"};

    for (var i = 0; i < arrayWords.length-1; i++) {
        if(( arrayWords[i] != undefined) && ( arrayWords[i+1] != undefined)) {
            g.addEdge(arrayWords[i], arrayWords[i+1], rel);
        }
    };
}

function initRelGraph() {
    var twitter = document.getElementById("twitter");
    var me2day = document.getElementById("me2day");
    var yozm = document.getElementById("yozm");
    snsView(emptyObject, twitter);
    snsView(emptyObject, me2day);
    snsView(emptyObject, yozm);
    var graph = document.getElementById("graph");
    g = new Graph();
}

function showRelGraph(width, height) {
    
    var layouter = new Graph.Layout.Spring(g);
    
    renderer = new Graph.Renderer.Raphael('graph', g, width, height);
    
    redraw = function() {
        layouter.layout();
        renderer.draw();
    };

    hide = function(id) {
        g.nodes[id].hide();
    };
    show = function(id) {
        g.nodes[id].show();
    };
};

window.onload = function() {
    // var naverRank = document.getElementById("naverRank");
    // var naverView = document.getElementById("naver");
    // var naverKeyword = get("/rank/naver", keywordView, naverRank, naverView);
// 
    // var daumRank = document.getElementById("daumRank");
    // var daumView = document.getElementById("daum");
    // var daumKeyword = get("/rank/daum", keywordView, daumRank, daumView);
// 
    // var nateView = document.getElementById("nate");
    // var nateRank = document.getElementById("nateRank");
    // var nateKeyword = get("/rank/nate", keywordView, nateRank, nateView);
}

// Object.prototype.clone = function() {
    // var newObj = (this instanceof Array) ? [] : {};
    // for (i in this) {
        // if (i == 'clone')
            // continue;
        // if (this[i] && typeof this[i] == "object") {
            // newObj[i] = this[i].clone();
        // } else
            // newObj[i] = this[i]
    // }
    // return newObj;
// };

var count = 0;
var dataObject;
var dataArray = new Array();
var topData;
var currentKey = "engineerpub";
// var emptyObject = new ObjectData();

function get(url, callback, viewParam, loadingParam) {
    var request = new XMLHttpRequest();
    request.open("GET", url);
    request.onreadystatechange = function() {
        // alert("ready status:" + request.readyState);
        if (request.readyState == 4 && request.status === 200) {
            var type = request.getResponseHeader("Content-Type");
            if (type.indexOf("xml") !== -1 && request.responseXML) {
                callback(request.responseXML, viewParam);
            } else if (type === "application/json") {
                callback(JSON.parse(request.responseText), viewParam);
            } else {
                data = JSON.parse(request.responseText);
                //console.log(data.service + " / " + data.contents.length);
                if (count < 3) {
                    dataObject = data.clone();
                    dataArray.push(dataObject);
                }
                if (count == 2) {

                    topData = getData(dataArray[0], dataArray[1], dataArray[2]);

                    var topRank = document.getElementById("topRank");
                    //var topView = document.getElementById("top");
                    var topKeyword = topKeywordView(topData, topRank);

                    var temp = topData.contents[0].keyword;
                    var searchKey = encodeURI(temp);
                    //var tempArray = temp.split(" ");
                    //var searchKey = encodeURI(tempArray[0]);

                    currentKey = searchKey;

                    var twitter = document.getElementById("twitter");
                    var twitSearch = get("/sns/twitter/" + searchKey + "/10",
                            snsView, twitter, twitter);

                    var me2day = document.getElementById("me2day");
                    var me2Search = get("/sns/me2day/" + searchKey + "/5",
                            snsView, me2day, me2day);
                    var yozm = document.getElementById("yozm");
                    var yozmSearch = get("/sns/yozm/" + searchKey + "/5",
                            snsView, yozm, yozm);
                }
                count++;
                callback(data, viewParam);
            }
            clear(loadingParam);
        }
    };
    request.send(null);
}

function snsView(data, param) {
    var keywordTemplateObj = TrimPath.parseDOMTemplate("sns_jst");
    var result = keywordTemplateObj.process(data);
    param.innerHTML = result;
}

function keywordView(data, param) {
    // someOutPutDiv = document.getElementById("someOutPutDiv");

    var keywordTemplateObj = TrimPath.parseDOMTemplate("keyword_jst");
    var result = keywordTemplateObj.process(data);

    param.innerHTML = result;
    // someOutPutDiv.innerHTML = result;
    // alert(result);
    // return result;
}

function topKeywordView(data, param) {
    // someOutPutDiv = document.getElementById("someOutPutDiv");

    var keywordTemplateObj = TrimPath.parseDOMTemplate("top_jst");
    var result = keywordTemplateObj.process(data);

    param.innerHTML = result;
    // someOutPutDiv.innerHTML = result;
    // alert(result);
    // return result;
}

function topKeyClick(clickKey) {
    var tempArray = clickKey.split(" ");
    var key = tempArray[0];
    currentKey = key;
    var graph = document.getElementById("graph");
    graph.innerHTML = ""
    var twitter = document.getElementById("twitter");
    var me2day = document.getElementById("me2day");
    var yozm = document.getElementById("yozm");
    var twitSearch = get("/sns/twitter/" + key + "/10", snsView, twitter,
            twitter);
    var me2Search = get("/sns/me2day/" + key + "/5", snsView, me2day, me2day);
    var yozmSearch = get("/sns/yozm/" + key + "/5", snsView, yozm, yozm);
}

function allsnsClick() {
    var graph = document.getElementById("graph");
    graph.innerHTML = ""
    var twitter = document.getElementById("twitter");
    var me2day = document.getElementById("me2day");
    var yozm = document.getElementById("yozm");
    var key = currentKey;
    var twitSearch = get("/sns/twitter/" + key + "/10", snsView, twitter,
            twitter);
    var me2Search = get("/sns/me2day/" + key + "/5", snsView, me2day, me2day);
    var yozmSearch = get("/sns/yozm/" + key + "/5", snsView, yozm, yozm);
}

function twitterClick() {
    var graph = document.getElementById("graph");
    graph.innerHTML = ""
    var twitter = document.getElementById("twitter");
    var me2day = document.getElementById("me2day");
    var yozm = document.getElementById("yozm");
    var key = currentKey;
    snsView(emptyObject, me2day);
    snsView(emptyObject, yozm);
    var twitSearch = get("/sns/twitter/" + key + "/20", snsView, twitter,
            twitter);
}

function me2dayClick() {
    var graph = document.getElementById("graph");
    graph.innerHTML = ""
    var twitter = document.getElementById("twitter");
    var me2day = document.getElementById("me2day");
    var yozm = document.getElementById("yozm");
    var key = currentKey;
    snsView(emptyObject, twitter);
    snsView(emptyObject, yozm);
    var me2Search = get("/sns/me2day/" + key + "/20", snsView, me2day, me2day);
}

function yozmClick() {
    var graph = document.getElementById("graph");
    graph.innerHTML = ""
    var twitter = document.getElementById("twitter");
    var me2day = document.getElementById("me2day");
    var yozm = document.getElementById("yozm");
    var key = currentKey;
    snsView(emptyObject, twitter);
    snsView(emptyObject, me2day);
    var yozmSearch = get("/sns/yozm/" + key + "/20", snsView, yozm, yozm);
}

function portalKeyClick(service, clickKey) {
    if (service == "daum") {
        window.open("http://search.daum.net/search?q=" + clickKey);
        return false;
    } else if (service == "nate") {
        window
                .open("http://search.nate.com/search/all.html?s=&sc=&afc=&j=&thr=sbma&nq=&q="
                        + clickKey);
        return false;
    } else {
        window.open("http://search.naver.com/search.naver?query=" + clickKey);
        return false;
    }
}


// init
$(document).ready(function() {
	init();
	var service = "realtopic";
	loadKeyword(service);
});

function loadKeyword(service) {
	var url = "/rank/" + service;
	if ("realtopic" == service) {
		var template = "#topTemplate";
	} else {
		var template = "#keywordTemplate";
	}
	var node = "#" + service + "Rank";
	$(node).empty();
	$.getJSON(url, function (data) {
		// $("#snsTemplate").tmpl(data.contents).appendTo("#sns");
		// $("#keywordTemplate").tmpl(data.contents).appendTo("#realtopicRank");

		$(template).tmpl(data.contents).appendTo(node);
	
		// setTimeout(function () {
			// $(".box").css('opacity', 1);
		// }, 20);
		$('.keyword').bind('click', function(event) {
			
			event.preventDefault();
			var effect = "fade";
			changePage( $('#sns'), effect);
			var keyword = event.srcElement.innerText;
			loadContents(keyword);			
		});
	});
	
}

function loadContents(keyword) {
	console.log("keywork:" + keyword);
	var url = "/sns/all/" + keyword;
	$.getJSON(url, function (data) {
        var posts = data.contents,
            cnt = posts.length;
		(function showContents() {
                $(".section").css('opacity', 1);
                $("#snsTemplate").tmpl(posts.pop()).prependTo("#snsList");
                if (--cnt > 0) {
                    setTimeout(function () {showContents();}, 500);
                }
          })();
	});
}


function init() {
	
	$('.menu').bind('touchstart mousedown', function(event) {
		event.preventDefault();
		
		var status = $('#leftmenu').attr('class').indexOf('in');
		
		//console.log(status);
		
		if(status < 0 ){
			moveMenu('in');
		}else{
			moveMenu();
		}
		
	});
	
	
	$('#menulist a').bind('click', function(event) {
		event.preventDefault();
		
		var nextPage = $(this).get(0).hash;
		
		console.log(nextPage);
	
		var effect = $(this).attr("data-effect");
		
		if(!effect){
			effect = "fade";
		}
		
		console.log(effect);
		
		changePage( $(nextPage), effect);	
		
		moveMenu();

		var service = nextPage.replace("#","");
		loadKeyword(service);
	});	
	

}

function moveMenu(type){
	if(type == 'in'){
		$('.leftmenu').addClass("in");
		$('.container').addClass("in");
	}else{
		$('.leftmenu').removeClass('in');
		$('.container').removeClass("in");		
	}
	
}

function changePage( $next, effect){
	
	$before  = $('.current'); 
	
	console.log($before.attr('class'));
	
	if($before.attr("id") == $next.attr("id")){
		return;
	}
	
	$before.addClass(effect+'-out');
	$before.removeClass('current');
		
	$next.addClass('current '+effect+'-in');

	$next.one("webkitAnimationEnd", function( ) {
		 $before.removeClass("current "+effect+"-out");
		 $next.removeClass(effect+'-in'); 
	});
	
}