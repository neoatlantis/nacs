__pragma__("alias", "S", "$")

from nacs.count import CommentCount
from nacs.comment import CommentArea

def main():
    firebase.initializeApp(nacs_config)
    
    for commentArea in S(".nacs-comment-area"):
        CommentArea( S(commentArea).attr("data-id") )

    for commentCount in S(".nacs-comment-count"):
        CommentCount( S(commentCount).attr("data-id") )

S(main)
