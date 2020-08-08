
server = null;

function loadContent(url)
{
    server = new RomiDataServer(url);
    displayFarms();
}

function closure(callback, arg1, arg2, arg3)
{
    return function() { callback(arg1, arg2, arg3); };
}

function makeEventLink(anchorText, handler, className) 
{
    var a = document.createElement("A");
    a.className = className;
    a.setAttribute("href", "javascript:void(0)");
    a.appendChild(document.createTextNode(anchorText));
    a.onclick = function() { return false; }
    a.onmousedown = function() { return false; }
    a.addEventListener("click", handler, false);
    return a;
}

function makeText(text) 
{
    return document.createTextNode(text);
}

function makeParagraph(text, className) 
{
    var t = document.createElement("P");
    t.className = className;
    t.innerHTML = text;
    return t;
}

function makeImage(src, className) 
{
    var img = document.createElement("IMG");
    img.src = src;
    img.className = className;
    return img;
}

function clearContent()
{
    content = document.getElementById("content");
    while (content.hasChildNodes()) {
	content.removeChild(content.firstChild);
    }
}

function displayAnalysis(farmid, zoneid, analysisid)
{
    server.getAnalysis(farmid, zoneid, analysisid, insertAnalysis);
}

function displayScan(farmid, zoneid, scanid)
{
    server.getScan(farmid, zoneid, scanid, insertScan);
}

function displayZone(farmid, zoneid)
{
    server.getZone(farmid, zoneid, insertZone);
}

function displayFarm(farmid)
{
    server.getFarm(farmid, insertFarm);
}

function displayFarms()
{
    server.getFarms(insertFarms);
}

function insertNavigation(div, farmid, zoneid, scanid)
{
    nav = makeParagraph("", "nav");
    nav.appendChild(makeText("Navigation ")); 
    nav.appendChild(makeEventLink("Index",
                                  displayFarms,
                                  "nav-link"))
    if (farmid)
        nav.appendChild(makeEventLink("Farm",
                                      closure(displayFarm, farmid),
                                      "nav-link")) 
    if (zoneid)
        nav.appendChild(makeEventLink("Zone",
                                      closure(displayZone, farmid, zoneid),
                                      "nav-link")) 
    if (scanid)
        nav.appendChild(makeEventLink("Scan",
                                      closure(displayScan, farmid, zoneid, scanid),
                                      "nav-link")) 
    content.appendChild(nav);
}

function insertStitchingAnalysis(analysis)
{
    clearContent();
    content = document.getElementById("content");
    insertNavigation(content, analysis.farm, analysis.zone, analysis.scan);
    
    t = makeParagraph(analysis.name, "analysis-name") 
    content.appendChild(t);
    
    t = makeParagraph("Analysis '" + analysis.short_name + "' of zone '" + analysis.zone + "'", "analysis-summary") 
    content.appendChild(t);
    
    t = makeParagraph("Description: " + analysis.description, "analysis-description") 
    content.appendChild(t);
    
    t = makeParagraph("State: " + analysis.state, "analysis-state") 
    content.appendChild(t);
    
    t = makeParagraph("Results", "analysis-results-title") 
    content.appendChild(t);

    table = document.createElement("TABLE");
    row = document.createElement("TR");
    
    cell = document.createElement("TD");
    map_id = analysis.results.map;
    src = server.imageURL(analysis.farm, analysis.zone, map_id, "large");
    img = makeImage(src, "scan-image");
    cell.appendChild(img);
    row.appendChild(cell);

    cell = document.createElement("TD");
    mask_id = analysis.results.mask;
    src = server.imageURL(analysis.farm, analysis.zone, mask_id, "large");
    img = makeImage(src, "scan-image");
    cell.appendChild(img);
    row.appendChild(cell);

    table.appendChild(row);
    content.appendChild(table);

    t = makeParagraph("Results (rwa)", "analysis-results-title") 
    content.appendChild(t);
    
    code = document.createElement("PRE");
    code.className = "analysis-results";
    code.innerHTML = syntaxHighlight(analysis.results)
    content.appendChild(code);
}

function insertPlantAnalysis(analysis)
{
}

function syntaxHighlight(json)
{
    if (typeof json != 'string') {
         json = JSON.stringify(json, undefined, 4);
    }
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, function (match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                cls = 'key';
            } else {
                cls = 'string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'boolean';
        } else if (/null/.test(match)) {
            cls = 'null';
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}

function insertAnyAnalysis(analysis)
{
    clearContent();
    content = document.getElementById("content");
    insertNavigation(content, analysis.farm, analysis.zone, analysis.scan);
    
    t = makeParagraph(analysis.name, "analysis-name") 
    content.appendChild(t);
    
    t = makeParagraph("Analysis '" + analysis.short_name + "' of zone '" + analysis.zone + "'", "analysis-summary") 
    content.appendChild(t);
    
    t = makeParagraph("Description: " + analysis.description, "analysis-description") 
    content.appendChild(t);
    
    t = makeParagraph("State: " + analysis.state, "analysis-state") 
    content.appendChild(t);
    
    t = makeParagraph("Results", "analysis-results-title") 
    content.appendChild(t);
    
    code = document.createElement("PRE");
    code.className = "analysis-results";
    code.innerHTML = syntaxHighlight(analysis.results)
    content.appendChild(code);
}

function insertAnalysis(userData, analysis)
{
    console.log("Analysis: " + JSON.stringify(analysis))
    
    if (analysis.short_name == "stitching")
        insertStitchingAnalysis(analysis)
    /*else if (analysis.short_name == "plant_analysis")
        insertPlantAnalysis(analysis) */
    else 
        insertAnyAnalysis(analysis)
}

function insertScan(userData, scan)
{
    console.log("Scan: " + JSON.stringify(scan))

    clearContent();
    content = document.getElementById("content");
    insertNavigation(content, scan.farm, scan.zone, null);
    
    t = makeParagraph("Scan of zone " + scan.zone + " at " + scan.date, "scan-zone-title") 
    content.appendChild(t);
    
    t = makeParagraph("Available analyses", "scans-analysis-title") 
    content.appendChild(t);

    for (var i = 0; i < scan.analyses.length; i++) {
        analysis = scan.analyses[i];
        a = makeEventLink(analysis.name + " (" + analysis.state + ")",
                          closure(displayAnalysis, scan.farm, scan.zone, analysis.id),
                          "analysis-name"); 
        content.appendChild(a);
        content.appendChild(document.createElement("BR"));
    }
    
    t = makeParagraph("Images", "scans-images-title") 
    content.appendChild(t);

    table = document.createElement("TABLE");
    content.appendChild(table);
    for (var i = 0; i < scan.images.length; i++) {
        image_id = scan.images[i];
        
        if ((i % 10) == 0) {
            row = document.createElement("TR");
            table.appendChild(row);
        }
        cell = document.createElement("TD");
        src = server.imageURL(scan.farm, scan.zone, image_id, "thumb");
        img = makeImage(src, "scan-image");
        cell.appendChild(img);
        row.appendChild(cell);
    }
}

function insertZone(userData, zone)
{
    console.log("Zone: " + JSON.stringify(zone))

    clearContent();
    content = document.getElementById("content");
    insertNavigation(content, zone.farm, null, null);
    
    t = makeParagraph(zone.short_name, "zone-name") 
    content.appendChild(t);
    t = makeParagraph("Scans", "zones-scans-title") 
    content.appendChild(t);
    for (var i = 0; i < zone.scans.length; i++) {
        scan = zone.scans[i];
        a = makeEventLink(scan.date,
                          closure(displayScan, zone.farm, zone.id, scan.id),
                          "scan-name"); 
        content.appendChild(a);
        content.appendChild(document.createElement("BR"));
    }
}

function insertFarm(userData, farm)
{
    console.log("Farm: " + JSON.stringify(farm))
    
    clearContent();
    content = document.getElementById("content");
    insertNavigation(content, null, null, null);
    
    t = makeParagraph(farm.name, "farm-name") 
    content.appendChild(t);
    t = makeParagraph(farm.description, "farm-description") 
    content.appendChild(t);
    t = makeParagraph("Zones", "farm-zones-title") 
    content.appendChild(t);
    for (var i = 0; i < farm.zones.length; i++) {
        zone = farm.zones[i];
        a = makeEventLink(zone.short_name,
                          closure(displayZone, farm.id, zone.id),
                          "zone-name"); 
        content.appendChild(a);
        content.appendChild(document.createElement("BR"));
    }
}

function insertFarms(userData, farms)
{
    console.log("Farms: " + JSON.stringify(farms))
    
    clearContent();
    content = document.getElementById("content");
    for (var i = 0; i < farms.length; i++) {
        farm = farms[i];
        a = makeEventLink(farm.name,
                          closure(displayFarm, farm.id),
                          "farm-name"); 
        content.appendChild(a);
        content.appendChild(document.createElement("BR"));
    }
}

function RomiDataServer(rootURL)
{
    this.root = rootURL;

    this.newRequest = function(callback, userData) {
	var xmlhttp = new XMLHttpRequest();
        xmlhttp.userData = userData;
        xmlhttp.callback = callback;
	return xmlhttp;
    }

    this.handleResponse = function(xmlhttp) {
        result = JSON.parse(xmlhttp.response);
        xmlhttp.callback(xmlhttp.userData, result);
    }
    
    this.handleStateChange = function(xmlhttp) {
	if (xmlhttp.readyState == 4) {
	    if (xmlhttp.status == 200) {
		this.handleResponse(xmlhttp);
	    } else {
		alert("Request for " + xmlhttp._url + " failed: Status " + xmlhttp.status);
	    }
	    delete xmlhttp;
	}
    }

    this.get = function(url, userData, callback) {
	var self = this;
	var xmlhttp = this.newRequest(callback, userData);
        xmlhttp._url = this.root + "/" + url;
	xmlhttp.open("GET", this.root + "/" + url, true);
	xmlhttp.onreadystatechange = function() {
	    self.handleStateChange(xmlhttp);
	}
	xmlhttp.send();
    }

    this.getFarms = function(callback) {
        this.get("farms", null, callback);
    }
    
    this.getFarm = function(id, callback) {
        this.get("farms/" + id, null, callback);
    }

    this.getZone = function(farmid, zoneid, callback) {
        this.get("farms/" + farmid + "/zones/" + zoneid, null, callback);
    }

    this.getScan = function(farmid, zoneid, scanid, callback) {
        this.get("farms/" + farmid + "/zones/" + zoneid + "/scans/" + scanid,
                 null, callback);
    }

    this.getAnalysis = function(farmid, zoneid, analysisid, callback) {
        this.get("farms/" + farmid + "/zones/" + zoneid + "/analyses/" + analysisid,
                 null, callback);
    }

    this.imageURL = function(farmid, zoneid, imageid, size) {
	return (this.root + "/images/"
                + farmid + "/" + zoneid + "/" + imageid
                + "?size=" + size);
    }
}
