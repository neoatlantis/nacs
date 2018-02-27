__pragma__ ("alias", "S", "$")

from nacs.uris import uriAdmin, uriThreadSetting
from nacs.util import EventDispatcher


class AdminArea:

    def __init__(self, area, authenticate):
        self.authenticate = authenticate # which is an AuthenticateArea()
        self.select = lambda: S(area)
        self.database = firebase.database()
        self.getCurrentUser = self.authenticate.getCurrentUser
        self.dataId = self.select().parents("[data-id]").attr("data-id")
        
        self.__initializeUI()
        self.__bindEvents()
        
        self.eventReadonly = EventDispatcher()

    def __initializeUI(self):
        html = """
            <div class="readonly warn">Comments disabled.</div>
            <div class="logged-in">
                <div class="readonly">
                    But you are allowed to enable it.
                    <button type="button" name="enable-comment">
                        Enable comments
                    </button>
                </div>
                <div class="not-readonly">
                    You are administrator.
                    <button type="button" name="disable-comment">
                        You may disable comments.
                    </button>
                </div>
            </div>
        """
        self.select().html(html)
        self.__toggleVisibility(False)

    def __bindEvents(self):
        self.authenticate.eventLogin.append(self.onAuthenticateLogin)
        self.authenticate.eventLogout.append(self.onAuthenticateLogout)
        self.database.ref(uriThreadSetting(self.dataId))\
            .on("value", self.onThreadSettingUpdated)
        self.select().find('button[name="enable-comment"]')\
            .click(self.onEnableComment)
        self.select().find('button[name="disable-comment"]')\
            .click(self.onDisableComment)

    def __toggleVisibility(self, visible):
        if visible:
            self.select().find(".logged-in").show()
        else:
            self.select().find(".logged-in").hide()

    async def __getAdminUID(self):
        try:
            admin = await self.database.ref(uriAdmin()).once("value")
        except:
            return None
        self.adminUID = admin.val()
        return admin.val()

    async def __updateThreadSetting(self, readonly):
        updates = {}
        updates[uriThreadSetting(self.dataId)] = readonly
        try:
            await firebase.database().ref().js_update(updates)
        except:
            pass

    async def onThreadSettingUpdated(self, update):
        # Listen to /threads/<tid>, which controls the administrative behaviour
        # of this thread.
        val = update.val()
        console.log("Setting for this thread:", val)
        # readonly?
        readonly = (True != val)
        self.eventReadonly.call(readonly)
        self.select().find(".readonly").toggle(readonly)
        self.select().find(".not-readonly").toggle(not readonly)

    async def onAuthenticateLogin(self):
        admin = await self.__getAdminUID()
        console.log("Admin UID", admin)
        if admin != self.getCurrentUser().uid:
            self.__toggleVisibility(False)
            return
        # now update info related to this
        console.log("Logged in as admin.")
        self.__toggleVisibility(True)

    async def onAuthenticateLogout(self):
        self.__toggleVisibility(False)

    async def onDisableComment(self):
        console.log("Disable commenting")
        await self.__updateThreadSetting(False)

    async def onEnableComment(self):
        console.log("Enable commenting")
        await self.__updateThreadSetting(True)
