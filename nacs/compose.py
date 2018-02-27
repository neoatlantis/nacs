__pragma__ ("alias", "S", "$")

from nacs.uris import uriThread, uriNewComment
from nacs.authenticate import AuthenticationArea
from nacs.admin import AdminArea



class ComposeArea:

    def __init__(self, area):
        self.select = lambda: S(area)
        self.__initializeUI()
        self.__bindEvents()

    def __initializeUI(self):
        self.select().html("""
            <div name="composer-area">
                <div><strong>Add new comment:</strong></div>
                <textarea name="nacs-content"></textarea>
                <button type="button" name="submit">Submit</button>
                <span class="warn not-logged-in">
                    You must log in to comment.
                </span>
            </div>
            <div name="admin-area"></div>
            <div name="login-area"></div>
        """)
        self.login = AuthenticationArea(\
            self.select().find("[name=\"login-area\"]")
        )
        self.admin = AdminArea(
            self.select().find("[name=\"admin-area\"]"),
            self.login
        )
        self.textarea = lambda:\
            self.select().find("textarea[name=\"nacs-content\"]")

    def __bindEvents(self):
        self.select().find('[name="composer-area"] button[name="submit"]')\
            .click(self.onSubmit)
        self.admin.eventReadonly.append(self.onReadonly)
        self.login.eventLogin.append(lambda: self.onAuthChanged(True))
        self.login.eventLogout.append(lambda: self.onAuthChanged(False))

    async def onSubmit(self):
        user = self.login.getCurrentUser()
        if not user:
            self.login.resetUI()
            return False

        text = str(self.textarea().val()).strip()
        dataId = self.select().parents("[data-id]").attr("data-id")
        if len(text) < 3:
            alert("Comment too short.")
            return False
        updates = {}
        newKey = firebase.database().ref().child(uriThread(dataId)).push().key
        updates[uriNewComment(dataId, newKey)] = {
            "uid": user.uid,
            "email": user.email,
            "content": text,
            "timestamp": firebase.database.ServerValue.TIMESTAMP,
        }
        console.log(updates)
        
        self.textarea().attr("disabled", True)
        try:
            await firebase.database().ref().js_update(updates)
            self.textarea().val("")
            self.textarea().attr("disabled", False)
            return True
        except:
            self.textarea().attr("disabled", False)
            return False

    async def onReadonly(self, readonly):
        # if a post is declared readonly, disable posting button, otherwise
        # enable it.
        self.select().find('[name="composer-area"]').toggle(not readonly)

    async def onAuthChanged(self, login):
        self.select().find('[name="composer-area"] button[name="submit"]')\
            .attr('disabled', not login)
        self.select().find('[name="composer-area"] .not-logged-in')\
            .toggle(not login)
