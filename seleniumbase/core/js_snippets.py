live_js = r"""
    (function () {
    var headers = {
    "Etag": 1, "Last-Modified": 1, "Content-Length": 1, "Content-Type": 1 },
      resources = {},
      pendingRequests = {},
      currentLinkElements = {},
      oldLinkElements = {},
      interval = 1000,
      loaded = false,
      active = { "html": 1, "css": 1, "js": 1 };
    var Live = {
    heartbeat: function () {
      if (document.body) {
        if (!loaded) Live.loadresources();
        Live.checkForChanges();
      }
      setTimeout(Live.heartbeat, interval);
    },
    loadresources: function () {
      function isLocal(url) {
        var loc = document.location,
        reg = new RegExp("^\\.|^\/(?!\/)|^[\\w]((?!://).)*$|"
          + loc.protocol + "//" + loc.host);
        return url.match(reg);
      }
      var scripts = document.getElementsByTagName("script"),
          links = document.getElementsByTagName("link"),
          uris = [];
      for (var i = 0; i < scripts.length; i++) {
        var script = scripts[i], src = script.getAttribute("src");
        if (src && isLocal(src))
          uris.push(src);
        if (src && src.match(/\blive.js#/)) {
          for (var type in active)
            active[type] = src.match("[#,|]" + type) != null
          if (src.match("notify"))
            alert("Live.js is loaded.");
        }
      }
      if (!active.js) uris = [];
      if (active.html) uris.push(document.location.href);
      for (var i = 0; i < links.length && active.css; i++) {
        var link = links[i], rel = link.getAttribute("rel"
        ),href = link.getAttribute("href", 2);
        if (href && rel && rel.match(new RegExp("stylesheet", "i")
        ) && isLocal(href)) {
          uris.push(href);
          currentLinkElements[href] = link;
        }
      }
      for (var i = 0; i < uris.length; i++) {
        var url = uris[i];
        Live.getHead(url, function (url, info) {
          resources[url] = info;
        });
      }
      var head = document.getElementsByTagName("head")[0],
          style = document.createElement("style"),
          rule = "transition: all .3s ease-out;"
      css = [".livejs-loading * { ",
      rule, " -webkit-", rule, "-moz-", rule, "-o-", rule, "}"].join('');
      style.setAttribute("type", "text/css");
      head.appendChild(style);
      style.styleSheet ? style.styleSheet.cssText = css :
      style.appendChild(document.createTextNode(css));
      loaded = true;
    },
    checkForChanges: function () {
      for (var url in resources) {
        if (pendingRequests[url])
          continue;
        Live.getHead(url, function (url, newInfo) {
          var oldInfo = resources[url],
              hasChanged = false;
          resources[url] = newInfo;
          for (var header in oldInfo) {
            var oldValue = oldInfo[header],
                newValue = newInfo[header],
                contentType = newInfo["Content-Type"];
            switch (header.toLowerCase()) {
              case "etag":
                if (!newValue) break;
              default:
                hasChanged = oldValue != newValue;
                break;
            }
            if (hasChanged) {
              Live.refreshResource(url, contentType);
              break;
            }
          }
        });
      }
    },
    refreshResource: function (url, type) {
      switch (type.toLowerCase()) {
        case "text/css":
          var link = currentLinkElements[url],
              html = document.body.parentNode,
              head = link.parentNode,
              next = link.nextSibling,
              newLink = document.createElement("link");
          html.className = html.className.replace(/\s*livejs\-loading/gi, ''
          ) + ' livejs-loading';
          newLink.setAttribute("type", "text/css");
          newLink.setAttribute("rel", "stylesheet");
          newLink.setAttribute("href", url + "?now=" + new Date() * 1);
          next ? head.insertBefore(newLink, next) : head.appendChild(newLink);
          currentLinkElements[url] = newLink;
          oldLinkElements[url] = link;
          Live.removeoldLinkElements();
          break;
        case "text/html":
          if (url != document.location.href)
            return;
        case "text/javascript":
        case "application/javascript":
        case "application/x-javascript":
          document.location.reload();
      }
    },
    removeoldLinkElements: function () {
      var pending = 0;
      for (var url in oldLinkElements) {
        try {
          var link = currentLinkElements[url],
              oldLink = oldLinkElements[url],
              html = document.body.parentNode,
              sheet = link.sheet || link.styleSheet,
              rules = sheet.rules || sheet.cssRules;
          if (rules.length >= 0) {
            oldLink.parentNode.removeChild(oldLink);
            delete oldLinkElements[url];
            setTimeout(function () {
              html.className = html.className.replace(
              /\s*livejs\-loading/gi, '');
            }, 100);
          }
        } catch (e) {
          pending++;
        }
        if (pending) setTimeout(Live.removeoldLinkElements, 50);
      }
    },
    getHead: function (url, callback) {
      pendingRequests[url] = true;
      var xhr = window.XMLHttpRequest ? new XMLHttpRequest() :
      new ActiveXObject("Microsoft.XmlHttp");
      xhr.open("HEAD", url, true);
      xhr.onreadystatechange = function () {
        delete pendingRequests[url];
        if (xhr.readyState == 4 && xhr.status != 304) {
          xhr.getAllResponseHeaders();
          var info = {};
          for (var h in headers) {
            var value = xhr.getResponseHeader(h);
            if (h.toLowerCase() == "etag" && value)
            value = value.replace(/^W\//, '');
            if (h.toLowerCase() == "content-type" && value)
            value = value.replace(/^(.*?);.*?$/i, "$1");
            info[h] = value;
          }
          callback(url, info);
        }
      }
      xhr.send();
    }
    };
    if (document.location.protocol != "file:") {
      if (!window.liveJsLoaded)
        Live.heartbeat();
      window.liveJsLoaded = true;
    }
    })();
    """
