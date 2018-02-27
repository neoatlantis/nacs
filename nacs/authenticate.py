__pragma__ ("alias", "S", "$")

from nacs.util import EventDispatcher


class AuthenticationArea:
    
    def __init__(self, area):
        self.select = lambda: S(area)
        self.uiInitialized = False
        self.__initializeUI()
        self.__bindEvents()

        self.eventLogin = EventDispatcher()
        self.eventLogout = EventDispatcher()
        self.resetUI = self.__initializeUI

    def getCurrentUser(self):
        return firebase.auth().currentUser

    def __initializeUI(self):
        if not self.uiInitialized:
            # basic UI
            html = """
                <div name="not-logged-in">
                    <div id="firebaseui-auth-container"></div>
                </div>
                <div name="logged-in">
                    You are currently logged in as
                    &lt;<span name="email" class="email"></span>&gt;
                    <button type="button" name="logout">Logout</button>
                </div>
            """
            self.select().html(html)
            self.uiInitialized = True

        user = self.getCurrentUser()
        if not user:
            if firebaseui.auth.AuthUI.getInstance():
                ui = firebaseui.auth.AuthUI.getInstance()
            else:
                ui = __new__(firebaseui.auth.AuthUI(firebase.auth()))
            uiConfig = {
                "callbacks": {
                    "signInSuccess": lambda: self.onAuthStateChanged() and False,
                },
                "signInFlow": "popup",
                "signInOptions": [
                    firebase.auth.GoogleAuthProvider.PROVIDER_ID,
                    firebase.auth.FacebookAuthProvider.PROVIDER_ID,
                    firebase.auth.TwitterAuthProvider.PROVIDER_ID,
                    firebase.auth.GithubAuthProvider.PROVIDER_ID,
#                    firebase.auth.EmailAuthProvider.PROVIDER_ID,
#                    firebase.auth.PhoneAuthProvider.PROVIDER_ID
                ],
            }
            ui.start("#firebaseui-auth-container", uiConfig)
            self.select().find("[name=\"not-logged-in\"]").show()
            self.select().find("[name=\"logged-in\"]").hide()
        else:
            self.select().find("[name=\"logged-in\"]").show()
            self.select().find("[name=\"not-logged-in\"]").hide()
            self.select().find("[name=\"logged-in\"] [name=\"email\"]").text(
                user.email
            )

    def __bindEvents(self):
        firebase.auth().onAuthStateChanged(self.onAuthStateChanged)
        self.select().find('[name="logged-in"] button[name="logout"]')\
            .on("click", self.onLogout)

    def onAuthStateChanged(self):
        if self.getCurrentUser():
            console.log("Event: login")
            self.eventLogin.call()
        else:
            console.log("Event: logout")
            self.eventLogout.call()
        self.__initializeUI()

    async def onLogout(self):
        console.log("Log user out.")
        firebase.auth().signOut()
