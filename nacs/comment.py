__pragma__ ("alias", "S", "$")

from nacs.compose import ComposeArea
from nacs.uris import uriThread

class CommentArea:
    
    def __init__(self, dataId):
        self.select = \
            lambda: S(".nacs-comment-area[data-id=\"" + dataId + "\"]")
        self.dataId = dataId
        self.database = firebase.database()
        self.__initializeUI()
        self.__bindEvents()

    def __initializeUI(self):
        html = """
            <div name="comments"></div>
            <div name="compose"></div>
        """
        self.select().html(html)
        self.composer = ComposeArea(self.select().find("[name=\"compose\"]"))

    def __bindEvents(self):
        self.commentsListener = self.database.ref(uriThread(self.dataId))
        self.commentsListener.on("value", self.onComments)

    def __addComments(self, comments):
        target = self.select().find('[name="comments"]').empty()
        comments = sorted(comments, key=lambda e: e["timestamp"])
        for comment in comments:
            obj = S("<div class=\"nacs-comment\">").html("""
                <div class="meta">
                    &lt;<span class="email"></span>&gt;
                    <span class="timestamp"></span>
                </div>
                <textarea class="content" readonly></textarea>
            """)
            obj.find(".email").text(comment["email"])
            obj.find(".timestamp").text(
                __new__(Date(comment["timestamp"])).toString()
            )
            obj.find(".content").val(comment["content"])
            
            target.append(obj)
        
    async def onComments(self, snapshot):
        __pragma__("jsiter")
        comments = snapshot.val()
        if not comments: 
            self.select().find('[name="comments"]').empty()
        else:
            self.__addComments([comments[i] for i in comments])
        __pragma__("nojsiter")
