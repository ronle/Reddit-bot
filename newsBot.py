
import praw
import random
import time
import json
import argparse

parser = argparse.ArgumentParser(
    prog="newsBot",
    argument_default=argparse.SUPPRESS
)
parser.add_argument("-s","--subReddit", nargs='?', default="test")

args = parser.parse_args()
subRedditStr = args.subReddit
print("Listening to [" + subRedditStr +"] subReddit")




triggers_1 = ["test",
              "test 2"]
                
# triggers_2 = ["word_4",
#               "word_5",
#               "word_6"]

# Put your bot's reddit id here. It will be used in several funtions.
bot_id = "FinalEngineering4720"
credentials = 'credentials.json'

with open(credentials) as f:
    creds = json.load(f)
    
# Connecting your bot to your personal script app and logging in
reddit = praw.Reddit(
    client_id=creds['client_id'],
    client_secret=creds['client_secret'],
    # username = creds['username'],
    # password = creds['password'],
    user_agent = creds['user_agent']
    )

# Begins the comment stream, scans for new comments
#for comment in reddit.subreddit(subRedditStr).comments(limit=10):
for comment in reddit.subreddit(subRedditStr).stream.comments(skip_existing=True):
    
    author_name = str(comment.author.name) # Fetch author name
    author_id = str(comment.author.id) # Fetch author id
    comment_lower = comment.body.lower() # Fetch comment body and convert to lowercase
    
    with open('ignore_list.txt', 'r')as rf: # Opens ignore_list in read only mode
    
        rf_contents = rf.read() # Reads the contents of ignore list
        
        if author_id not in rf_contents and author_id != bot_id: #Checks comment against ignore list and bot id
            
            if "!ignore" in comment_lower: # Looks for the word "ignore" in the comment and checks length of comment to prevent misfire.
                
                print("Checking for bot_id")
                
                if comment.parent().author.id == bot_id: # Checks if comment is a reply to your bot
        
                    with open('ignore_list.txt', 'a') as f: # Opens ignore list in append mode
                        
                        print("##### NEW COMMENT #####")
                        print(comment.author)
                        print(comment.author.id)    
                        print(comment.body.lower())
                        print("           ")
                        
                        # Writes Username and ID of user to the ignore list
                        f.write(author_name)
                        f.write("\n")
                        f.write(author_id)
                        f.write("\n")
                        f.write("\n")
                        
                        print(" ")
                        print("User Added to Ignore List")
                        print(" ")
                        
                        # Replies to user comment
                        comment.reply("User Added to Ignore List.")
                        
                else: # if ignore is not in response to your bot, prints a false alarm message and does not add name to ignore list
                    
                    print("##### NEW COMMENT #####")
                    print(comment.author)
                    print(comment.author.id)    
                    print(comment.body.lower())
                    print("           ")
                    
                    print("           ")
                    print("&&&& False Alarm &&&&")
                    print("           ")
                    
                
            else: # If 'ignore' not present in comment body, prceeds to checking for keywords and other bot functions
                
                # This section just prints out the comment and author information
                print("##### NEW COMMENT #####")
                print(comment.submission.title)
                print("          ")
                print(comment.author)
                print(comment.author.id)    
                print(comment.body.lower())
                print("           ")
                
                if all(word in comment_lower for word in triggers_1): #Checks for keywords in comment

                    with open('responses_1.txt', 'r', encoding='utf-8') as tf:
                        
                        # quote_selection = tf.read().splitlines()
                
                        print("===== Generating Reply =====")
                        generated_reply = (f"I agree with you, {comment.author}. {comment.body}")
                        # generated_reply_unadjusted = random.choice(quote_selection) # Fetch random quote from list
                        # generated_reply = generated_reply_unadjusted.replace("username", author_name)
                        comment.reply(generated_reply) # Replies to comment with random quote
                        print("  ")
                        print(generated_reply) # Prints random quote from reply
                        print("  ")
                        print("===== Reply Posted ======")
                        print("  ")
                        time.sleep(60) # Cooldown in seconds
                          
                # elif any(word in comment_lower for word in triggers_2): #Checks for keywords in comment
                    
                #     # This function rolls a die and returns true on 1
                #     roll_die = random.randint(1, 8)
                #     print("Dice Roll: ", roll_die)
                #     roll_die_string = str(roll_die)
                #     if roll_die_string == "1":
                        
                #         with open('responses_2.txt', 'r', encoding='utf-8') as tf:
                            
                #             quote_selection = tf.read().splitlines()

                #             print("===== Generating Reply =====")
                #             generated_reply_unadjusted = random.choice(quote_selection) # Fetch random quote from list
                #             generated_reply = generated_reply_unadjusted.replace("username", author_name)
                #             comment.reply(generated_reply) # Replies to comment with random quote
                #             print("  ")
                #             print(generated_reply) # Prints random quote from reply
                #             print("  ")
                #             print("===== Reply Posted ======")
                #             print("  ")
                #             time.sleep(60) # Cooldown in seconds
                  
                #     else: # on a failed die roll, the comment is ignored.
                        
                #         print("  ")
                #         print("Roll failed, ignoring comment")
                #         print("  ")
                
                    
        else: # If user on ignore list, prints User Ignored, and does not reply to comment
            
            print("##### NEW COMMENT #####")
            print(comment.author)
            print(comment.author.id)    
            print(comment.body.lower())
            print("           ")
            
            print ("!!!!!!!! User Ignored !!!!!!!!")
