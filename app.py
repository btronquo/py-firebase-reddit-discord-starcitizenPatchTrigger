import config
import praw
from dhooks import Webhook, Embed
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Service account (config here: https://console.developers.google.com/projectselector2/iam-admin/serviceaccounts?pli=1&supportedpurview=project&project&folder&organizationId)
serviceAccountConfig = credentials.Certificate('/home/pi/dev/serviceAccountConfig.json')
firebase_admin.initialize_app(serviceAccountConfig)

db = firestore.client()

# reddit praw config
reddit = praw.Reddit(user_agent=config.data['user_agent'],
                     client_id=config.data['client_id'], client_secret=config.data['client_secret'],
                     username=config.data['username'], password=config.data['password'])
# discord webhook
hook = Webhook(config.data['discord_webhook'])

imgBig = 'https://i.imgur.com/9sv9ZUu.jpg'
imgIcon = 'https://i.imgur.com/oNg2zU2.png'

# select firebase-firestore collection
posts = db.collection(u'posts')

# test get score posts
for submission in reddit.subreddit('starcitizen').search('title:patch note', sort='new', time_filter='week'):
        print(submission.created)
        print(submission.title)
        print(submission.url)
        # check in db
        postId = submission.id
        postCreated = str(submission.created)
        postTitle = str(submission.title)

        if posts.document(u''+ postCreated + '').get().exists == True:
            print('Post' + str(postCreated) + ' exist')
        else:
            print('Missing post: ' + str(postCreated))
            doc_ref = db.collection(u'posts').document(u'' + postCreated + '')
            doc_ref.set({
                u'id': u''+ postId  +'',
                u'created': u''+ postCreated  +'',
                u'title': u''+  postTitle  +''
            })

            # Send message to Discord server
            embed = Embed(
                color=14177041,
                timestamp='now',
            )
            embed.set_title(title=':smiley:  -> Un nouveau patch est dispo!', url=''+ submission.url  +'')
            embed.add_field(name='Info Patch', value=''+ postTitle  +'')
            embed.set_footer(text='Script by Luicid', icon_url=imgIcon)
            embed.set_image(imgBig)
            hook.send(embed=embed)
            #hook.send("@everyone")

print('fin')
