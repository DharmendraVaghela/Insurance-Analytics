import re

#Removes emojis and links from the text
def clean_post(post):
    try:
        # Wide UCS-4 build
        emoji_pattern = re.compile(u'['u'\U0001F300-\U0001F64F'u'\U0001F680-\U0001F6FF'u'\u2600-\u26FF\u2700-\u27BF]+',re.UNICODE)
    except re.error:
        # Narrow UCS-2 build
        emoji_pattern = re.compile(u'('u'\ud83c[\udf00-\udfff]|'u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'u'[\u2600-\u26FF\u2700-\u27BF])+', re.UNICODE)

    cleaned_post= emoji_pattern.sub(r'', post)
    cleaned_post.strip()
    cleaned_post = re.sub(r"http\S+", "", cleaned_post)

    return cleaned_post



#Convert JSON response for FB user posts into lists
def process_fb_json(posts_json):
    message_list=[]
    story_list=[]

    # Get messages and stories
    for post in posts_json:
        for attrib in post:
            if attrib == "message":
                message_list.append(clean_post(post[attrib].lower()))
            if attrib == "story":
                story_list.append(clean_post(post[attrib].lower()))

    return (message_list, story_list)
