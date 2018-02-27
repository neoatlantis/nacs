__pragma__ ("alias", "S", "$")

from nacs.uris import uriThread

class CommentCount:

    def __init__(self, dataId):
        self.select = \
            lambda: S(".nacs-comment-count[data-id=\"" + dataId + "\"]")
        self.dataId = dataId
        self.database = firebase.database()
        self.updateCount(0)
        self.__bindEvents()

    def __bindEvents(self):
        self.commentsListener = self.database.ref(uriThread(self.dataId))
        self.commentsListener.on("value", self.onComments)

    def updateCount(self, count):
        self.select().text(count)

    async def onComments(self, snapshot):
        __pragma__("jsiter")
        comments = snapshot.val()
        if not comments: 
            count = 0
        else:
             count = len(comments)
        self.updateCount(count)
        __pragma__("nojsiter")
