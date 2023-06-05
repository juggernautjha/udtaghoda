import requests
import json
from typing import Dict, Union, List

#! Change it every time you change users/login. It is pretty simple, just follow the following steps.
'''
1. Login to your Instagram Account.
2. Open up the Developer console, switch to the Network tab. 
3. Copy any request with return type json as curl, paste it to Postman and export to python. Copy the "headers" dictionary. 
'''
headers = {
  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/113.0',
  'Accept': '*/*',
  'Accept-Language': 'en-US,en;q=0.5',
  'Accept-Encoding': 'gzip, deflate, br',
  'X-CSRFToken': 'xYNq23ry7gr3AJvW71cZpysXA7CLsq8S',
  'X-IG-App-ID': '936619743392459',
  'X-ASBD-ID': '198387',
  'X-IG-WWW-Claim': 'hmac.AR2eQ_5DwoGO-11wO4xSXyLWsCNuqBW13m3yQoWBYsYNmDft',
  'X-Requested-With': 'XMLHttpRequest',
  'DNT': '1',
  'Connection': 'keep-alive',
  'Referer': 'https://www.instagram.com/brig.behoshi/following/?next=%2F',
  'Cookie': 'ig_did=6A50597C-145C-4245-A107-876FDA84F309; datr=FoV9ZKLkHMkCxnfk6noJUxWZ; csrftoken=xYNq23ry7gr3AJvW71cZpysXA7CLsq8S; mid=ZH2FFgAEAAHIRO5eDeYURVjUIEHT; ig_nrcb=1; rur="EAG\\05449311782709\\0541717483711:01f747451d9596132e746875ea66eb1b1e5b27308bcb060389abd1e03291b40d33ec20d6"; ds_user_id=49311782709; sessionid=49311782709%3ABMjp6k0UtjM2Sh%3A8%3AAYfzRKkUFAFJ7cbC1bJKDUvObzaoBd-P7ou6WHmhtA; shbid="14007\\05449311782709\\0541717483691:01f76a727e1e934d4cfffc57c00dc30eeaf0f0a03b1687c012a9d44e33f98ea4b59cd91d"; shbts="1685947691\\05449311782709\\0541717483691:01f7c8f5cd21d9d22df28defeb7fa743091f2c47b37baa7d07641ca877c514271519d20a"; csrftoken=mqZyNjdCTZL5O7VWYoOiOFzGxzM7GAw9; ds_user_id=49311782709',
  'Sec-Fetch-Dest': 'empty',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Site': 'same-origin',
  'TE': 'trailers'
}


def get_user_data(pk : str) -> Dict:
    '''
    Utility function.\n
    Very useful, contains basically everything on the profile page of the user. It can be used to harvest bios and mutuals (which I am convinced are in some way weighted).\n
    Syntax: get_user_data(pk: str), where pk is the primary key.\n
    'user':
        - 'username', 'full_name', 'follower_count', 'media_count', 'following_count', 'bio_links', 'biography_with_entities', 'profile_context_mutual_follow_ids', 'mutual_followers_count'
    '''
    url = f"https://www.instagram.com/api/v1/users/{pk}/info/"
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    js_resp = json.loads(response.text)
    return js_resp


def read_feed(pk: str, count: int) -> Dict:
    '''
    Utility function.\n
    Very useful, contains basically everything in the feed of the user. Can be used to harvest comments and spot love birds. I just hope this works.\n
    Syntax: read_feed(pk: str, count : int), where pk is the primary key and count is the number of posts you wish to examine. \n
    'items': is a list, every item in items has the following useful characters.
        - 'pk', 'id', 'location', 'like_count', 'top_likers', 'facepile_top_likers', 'caption', 'carousel_media_count', 'carousel_media', 'carousel_media_ids', 'like_count'
    '''
    url = f"https://www.instagram.com/api/v1/feed/user/{pk}/?count={count}"
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    js_resp = json.loads(response.text)
    return js_resp

 
def read_comments(post_id : str) -> Dict:
    '''
    Utility function.\n
    Aforementioned function for harvesting comments and spotting love birds. I just hope this works.\n
    Syntax: read_feed(pk: str, count : int), where pk is the primary key and count is the number of posts you wish to examine. \n
    'comments': is a list, every comment has the following useful attributes.
        - 'text', 'created_at', 'user' (is a dict with 'pk', 'username', 'full_name'), 'is_liked_by_media_owner'
    '''
    url = f"https://www.instagram.com/api/v1/media/{post_id}/comments/"
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    js_resp = json.loads(response.text)
    return js_resp


def get_following(max_id : int, pk : str) -> Union[Dict, List]:
    '''
    Utility function.\n
    Returns a JSON containing atmost 200 users. With some clever (stupid) while-loopery, can be used to get all users.\n
    Syntax: get_following(max_id : int, pk : str), where pk is the primary key and max_id can be anything <= following. If it is X, the function returns 
    ids from X-200 to X.\n
    'users': is a list. every user has the following (uesful) attributes.
        -'pk', 'pk_id', 'username', 'full_name', 'is_private'
    '''
    url = f"https://www.instagram.com/api/v1/friendships/{pk}/following/?max_id={max_id}"
    payload = {}
    response = requests.request("GET", url, headers=headers, data=payload)
    js_resp = json.loads(response.text)
    return js_resp


if __name__ == '__main__':
    pk = '49311782709'
    x = get_user_data(pk)
    print(x)

