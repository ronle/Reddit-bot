# This file will connect to specific subreddit and "listen" to provided comments
# Once a comment with specific triggers is detected, it will log that message to json file
# for ease of future lookup. If this is new comment of existing logged user, the comment will be appended to that same user


import praw
import json
import os

carryOn = True

triggers_1 = ["test","test 2"]              

# Put your bot's reddit id here. It will be used in several funtions.
credentials = 'credentials.json'

with open(credentials) as f:
    creds = json.load(f)

bot_id = creds["username"]    

# Connecting your bot to your personal script app and logging in
reddit = praw.Reddit(
    client_id=creds['client_id2'],
    client_secret=creds['client_secret2'],
    username = creds['username'],
    password = creds['password'],
    user_agent = creds['user_agent']
    )

jsonfilename = 'testjson2.json'

if not os.path.exists(jsonfilename):
    with open(jsonfilename, 'w') as f:
        
        template = """
        [
            {
            "id": 1,
            "author_name": "John Doe",
            "author_id": "JohnDoe",
            "commentsList":[
                "None"
                ]
            }
        ]"""
        
        f.write(template)
        # json.dump(template, f)
        f.close()

with open("log.txt", "w") as log:

    with open(jsonfilename)as rf: # Opens json in all actions allowed mode    
        data = json.load(rf)
        while carryOn:
            try:    
                # Begins the comment stream, scans for new comments
                for comment in reddit.subreddit('all').stream.comments(skip_existing=True):
                            
                    reddit_author_name = str(comment.author.name) # Fetch author name
                    reddit_author_id = str(comment.author.id) # Fetch author id
                    reddit_comment_lower = comment.body.lower() # Fetch comment body and convert to lowercase
                                
                    if any(word in reddit_comment_lower for word in triggers_1): #Checks for keywords in comment
                        
                        #Terminal print
                        print("##### NEW COMMENT #####")
                        print(comment.author)
                        print(comment.author.id)    
                        print(comment.body.lower())
                        print("           ")
                        
                        #check if OP is already in data file
                        try:
                                    
                            match = next(user for user in data if user['author_id'] == reddit_author_id)
                            # if user['author_id'] == reddit_author_id: #Checks if OP already exist in data file, if he does append only new comment
                            
                            if reddit_comment_lower not in match['commentsList']: #record with same user already exist, adding the new comment
                                match["commentsList"].append(reddit_comment_lower)            
                                # json.dump(op, rf)
                            
                        except:
                            #Record does not exist, write new record to JSON file
                            last_id = max(data, key=lambda x: x['id'])
                            newRecord = {
                                "id": last_id['id']+1,
                                "author_name": reddit_author_name,
                                "author_id": reddit_author_id,
                                "commentsList": [
                                    reddit_comment_lower
                                    ]
                                }
                            data.append(newRecord)

                    with open("testJSON2.json", "w") as f:
                        json.dump(data, f)
            
            except Exception:
                traceback.print_exc(file=log)
                # carryOn = True
