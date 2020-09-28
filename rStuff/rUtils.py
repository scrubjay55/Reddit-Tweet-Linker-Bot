rBase = "https://www.reddit.com"

# Some stuff.. ------------------
turkish_subs = ["turkey", "turkeyjerky", "testyapiyorum", "kgbtr", "svihs", "gh_ben", "burdurland"]
# -------------------------------


class rNotif:
    def __init__(self, notif):
        # self.kind = notif['kind']  # kind
        content = notif['data']
        self.author = content['author']  # summoner
        self.body = content['body'].lower()  # body lowered
        self.subreddit = content['subreddit'].lower()  # sub
        if self.subreddit in turkish_subs:
            self.lang = 'tur'
        else:
            self.lang = 'eng'
        self.parent_id = content['parent_id']  # the post or mentioner
        self.id_ = content['name']  # answer to this. represents the comment with t1 prefix
        self.rtype = content['type']  # comment_reply or user_mention
        context = content['context']  # /r/SUB/comments/POST_ID/TITLE/COMMENT_ID/
        context_split = str(context).split('/')
        self.post_id = 't3_' + context_split[4]  # post id with t3 prefix added
        # self.id_no_prefix = context_split[6]  # comment id without t1 prefix

    def __repr__(self):
        return f"(NotifObject: {self.id_})"


class rPost:
    def __init__(self, post):
        content = post['data']
        self.id_ = content['name']  # answer to this. represents the post with t3 prefix
        self.is_self = content['is_self']  # text or not
        self.author = content['author']  # author

        gallery_data = content.get('gallery_data')
        if gallery_data is not None:
            gallery_zero_id = gallery_data['items'][0]['media_id']
            try:
                img_m = content['media_metadata'][gallery_zero_id]['m'].split('/')[-1]
            except:
                img_m = 'jpg'
            self.url = f"https://i.redd.it/{gallery_zero_id}.{img_m}"
            self.is_img = True
        else:
            self.url = content['url']  # url
            self.is_img = self._is_img_post()
        self.subreddit = content['subreddit'].lower()
        self.over_18 = content['over_18']
        if self.subreddit in turkish_subs:
            self.lang = 'tur'
        else:
            self.lang = 'eng'
        self.is_saved = content['saved']
        # self.listing = None  # true if from sub feed listener

    def __repr__(self):
        return f"(PostObject: {self.id_})"

    def _is_img_post(self):
        if not self.is_self and self.url.split(".")[-1].lower() in ["jpg", "jpeg", "png", "tiff", "bmp"]:
            return True
        else:
            return False
