# # **Starcitizen Patch Trigger**!

Because CGI refuse to give free access to their api, I Made this python program to be notified on **Discord** when a reddit user post a '**Patch note**' in the subreddit **/r/starcitizen**.

## What you'll need

- Firebase Firestore Project (it's free)
- Valid Discord webhook
- Reddit registered app ([https://www.reddit.com/prefs/apps/](https://www.reddit.com/prefs/apps/))

## Quick-Start
1. Clone this repo
2. Remove 'EXAMPLE' to the **config.py** and **serviceAccountConfig.json** files 
3. Update **config.py** and **serviceAccountConfig.json** files with your data
4.   `python3 app.py`

That's it!

## Author
Boris Tronquoy

## Thanks
[PRAW](https://github.com/praw-dev/praw)
[DHOOKS](https://github.com/kyb3r/dhooks)