uriThread = lambda tid: "/comments/" + tid
uriNewComment = lambda tid, cid: uriThread(tid) + "/" + cid
uriAdmin = lambda: "/admin"
uriThreadSetting = lambda tid: "/threads/" + tid
