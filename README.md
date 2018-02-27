NeoAtlantis Commenting System
=============================

This project intends to replace commenting systems like Disqus(or its
self-hosting alternative Isso) to a Firebase backended solution.

## Usage

1. On Firebase, create a realtime database with following rules:

```json
{
    "rules": {
      "admin": {
          ".read": true,
          ".write": false
      },
      "threads": {
          "$tid": {
            ".read": true,
            ".write": "root.child('admin').val() == auth.uid",
            ".validate": "newData.isBoolean()"
          }
      },
      "comments": {
          "$tid": {
            ".read": true,
            "$cid": {
              ".write": "auth.uid != null && !data.exists() && newData.exists()",
              ".validate": "
              	  newData.hasChildren(['uid', 'email', 'content', 'timestamp']) &&
                  root.child('threads').hasChild($tid) &&
                  root.child('threads').child($tid).val() != false
              ",
              "uid": { ".validate": "newData.val() == auth.uid" },
              "email": { ".validate": "newData.val() == auth.token.email" },
              "timestamp": { ".validate": "newData.val() <= now" },
              "content": { ".validate": "
                  newData.isString() 
                  && newData.val().length > 5
                  && newData.val().length < 500
                "
              }
            }
          }
      }
    }
}
```

2. Put following code into a `.js` file.

```javascript
var nacs_config = {
    apiKey: "...",
    authDomain: "??????.firebaseapp.com",
    databaseURL: "https://?????.firebaseio.com",
};
```

This is the configuration file. Replace its values accordingly to your project
at Firebase.

3. Modify your code, import javascript and CSS stylesheets like this:

```html
<script src="https://www.gstatic.com/firebasejs/4.8.2/firebase.js"></script>
<script src="https://cdn.firebase.com/libs/firebaseui/2.5.1/firebaseui.js"></script>
<link type="text/css" rel="stylesheet" href="https://cdn.firebase.com/libs/firebaseui/2.5.1/firebaseui.css" />
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
<script src="nacs.config.js"></script>
<link type="text/css" rel="stylesheet" href="nacs.css" />
<script src="__javascript__/nacs_start.js"></script>
```

`nacs_start.js` in folder `/__javascript__` is standalone and can be moved to
anywhere else.

4. To display a commenting box below your blog entry, use

```<div class="nacs-comment-area" data-id="some-id"></div>```

where `some-id` should be a unique ID(compatiable with URL and without `/`s)
for your page.

Put following code to somewhere that needs to display a count:

```<span class="nacs-comment-count" data-id="some-id"></span>```

5. Log in to your Firebase console. Add an item `admin` to the root entry in
database, which is a string containing the UID of your admin user.

**The admin is only user that can disable/enable comments for a given page.
Each new page has comments by default disabled and must be enabled manually.**
