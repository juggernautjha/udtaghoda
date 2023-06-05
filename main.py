import json
from typing import Dict, Union, List
import os
import backbone
from tqdm import tqdm
import pandas as pd
DATA_DIR = "raw_data"

#! Combine Harvester (-\""/-)
'''DOCString for Saver'''
'''
    This is what you want to run when you have shit load of time, and nothing better
    to do. It gets EVERYTHING (but the media, of course. Ethical concerns) and dumps it 
    in a folder names 'username' in the DATA_DIR. The format is as follows:
    DATA_DIR/
        username/
            profile.json -> profile information. stuff like bios and mutuals. 
            followers.json -> followers.
            posts/
                post1.json -> comments, metadata regarding the post.
                post2.json
                ...               

            path = f'{DATA_DIR}/{user_data["username"]}'
            if not os.path.exists(path):
                os.makedirs(path)
'''
relevant_keys = {
       backbone.get_user_data : ['username', 'full_name', 'follower_count', 'media_count', 'following_count', 'bio_links', 'biography_with_entities', 'profile_context_mutual_follow_ids', 'mutual_followers_count'],
       backbone.read_feed : ['pk', 'id', 'location', 'like_count', 'top_likers', 'facepile_top_likers', 'caption', 'carousel_media_count', 'carousel_media', 'carousel_media_ids', 'like_count'],
       backbone.read_comments : ['text', 'created_at', 'user', 'is_liked_by_media_owner'],
       backbone.get_following : ['pk', 'username', 'full_name', 'is_private']
}

def get_user_details(pk : str) -> Dict:    
    user_data = backbone.get_user_data(pk)['user']
    user_data = {i : user_data[i] for i in relevant_keys[backbone.get_user_data] if i in user_data}
    return user_data

def get_following_dataframe(pk : str) -> pd.DataFrame:
    user_data = get_user_details(pk)
    following_count = user_data['following_count']
    curr_poss = 0
    followers = []
    while (curr_poss < following_count):
        tmp = backbone.get_following(min(curr_poss, following_count), pk)['users']
        followers += tmp
        curr_poss += 200
    followers = [{j : i[j] for j in relevant_keys[backbone.get_following]} for i in followers]
    great_dict = {
        i : [k[i] for k in followers] for i in relevant_keys[backbone.get_following]
    }
    mydf = pd.DataFrame(great_dict)
    user_data = [get_user_details(pk) for pk in tqdm(great_dict['pk'])]
    minor_dict = {
        i : [k[i] for k in user_data if i in k] for i in relevant_keys[backbone.get_user_data]
    }
    deets_df = pd.DataFrame(minor_dict)    
    mydf = pd.merge(mydf, deets_df, on='username')
    mydf.to_csv('ess.csv', index=False)
    return mydf







if __name__ == '__main__':
    pk = '49311782709'
    get_following_dataframe(pk)
