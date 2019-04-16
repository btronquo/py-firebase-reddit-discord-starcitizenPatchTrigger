import os
import config
import praw
from dhooks import Webhook, Embed
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# for test only
testMode = False

current_path = config.current_path
print('current path ===' + current_path)

# Service account (config here: https://console.developers.google.com/projectselector2/iam-admin/serviceaccounts?pli=1&supportedpurview=project&project&folder&organizationId)
serviceAccountConfig = credentials.Certificate(current_path + '/serviceAccountConfig.json')
firebase_admin.initialize_app(serviceAccountConfig)
db = firestore.client()

# select firebase-firestore collection
posts = db.collection(u'posts')

# reddit praw config
reddit = praw.Reddit(user_agent=config.data['user_agent'],
                     client_id=config.data['client_id'], client_secret=config.data['client_secret'],
                     username=config.data['username'], password=config.data['password'])

# discord webhook
hook = Webhook(config.data['discord_webhook'])
hook_septra = Webhook(config.data['discord_webhook_septra'])

# img to illustrate Discord post
imgBig = 'https://i.imgur.com/9sv9ZUu.jpg'
imgIcon = 'https://i.imgur.com/oNg2zU2.png'

for submission in reddit.subreddit('starcitizen').search('title:(patch note) OR (star citizen alpha out)', sort='new', time_filter='week'):

    print(submission.created)
    print(submission.title)
    postId = submission.id
    postCreated = str(submission.created)
    postTitle = str(submission.title)

    # if the post links to spectrum
    if 'https://robertsspaceindustries.com/spectrum/' in submission.url:

        if posts.document(u''+ postCreated + '').get().exists == False:
            doc_ref = posts.document(u'' + postCreated + '')
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

            if testMode == False:
                hook.send(embed=embed)
                hook_septra.send(embed=embed)
                hook.send("@everyone")
            else:
                print('Test Mode enabled - don\'t send discord msg')


        else:
            print('The document: ' + postCreated + ' for the post ' + postId + ' exist in the database')
    else:
        print('Document with title "' + submission.title + '" is ignored as is not a spectrum post)')