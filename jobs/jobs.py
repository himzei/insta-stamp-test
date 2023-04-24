import re
import requests
from bs4 import BeautifulSoup
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.response import Response
from insta_stamp.models import InstaStampList
from insta_admin.models import InstaSetting
from insta_stamp.serializers import InstaStampListSerializer
from insta_admin.serializers import InstaStampResultSerializer

def get_object(insta_ref): 
    try: 
        return InstaStampList.objects.get(insta_ref=insta_ref)
    except InstaStampList.DoesNotExist:
        raise NotFound
    
def removeComma(stringLikes):
    if ',' or "K" or "M" in stringLikes: 
        return stringLikes.replace(",","").replace("K", "000").replace("M","000000")
    else: 
        return stringLikes

def schedule_api():
    
    all_insta_url = InstaStampList.objects.values_list("insta_url")
    all_insta_stamp = InstaStampList.objects.all()

    for url in all_insta_url: 
        response = requests.get(url[0])
        insta_ref = url[0].split("/p/")[1].split("/")[0]

        try:
            soup = BeautifulSoup(response.text, "html.parser")
            dataUser = soup.find("title").text 
        except: 
            # 삭제했을 때는 좋아요 0
            serializer_stamp = InstaStampListSerializer(
                get_object(insta_ref),
                data = {
                  "likes_cnt": int(0), 
                  "comments_cnt": int(0), 
                  "friends_cnt": int(0),
                },
                partial=True,
            )
            if serializer_stamp.is_valid(): 
                serializer_stamp.save()
            continue


        # 친구 소환
        pattern = '@([0-9a-zA-Z가-힣_]*)'
        hash_f = re.compile(pattern)
        friends = hash_f.findall(dataUser)
        friends = list(filter(None, friends))

        # 좋아요, 커멘트 수 크롤링
        try: 
            data = soup.find("meta", {"name": "description"})["content"]
        except: 
            continue

    
        try: 
            if 'Likes' in data: 
                likes = data.split("Likes,")[0].strip().split(" ")[-1]
                comments = data.split("Comments")[0].strip().split(' ')[-1]
            elif 'likes' in data: 
                likes = data.split("likes,")[0].strip().split(" ")[-1]
                comments = data.split("comments")[0].strip().split(' ')[-1]
            else: 
                raise ParseError()
        except: 
            continue
      
        likes = removeComma(likes)
        comments = removeComma(comments)

        serializer = InstaStampListSerializer(
            get_object(insta_ref),
            data = {
              "likes_cnt": likes, 
              "comments_cnt": comments, 
              "friends_cnt": len(friends),
            },
            partial=True,
        )

        if serializer.is_valid(): 
            serializer.save()

    count = len(all_insta_stamp)
    comments = 0
    likes = 0
    friends = 0 

    current_events_name = InstaSetting.objects.get(events_name="엑스코 취업박람회")
    hashtags_selected = current_events_name.hashtags_selected

    for insta_list in all_insta_stamp: 
        comments += insta_list.comments_cnt
        likes += insta_list.likes_cnt
        friends += insta_list.friends_cnt
    
    serializer_admin = InstaStampResultSerializer(
        data = {
            "total_insta": count, 
            "total_likes": likes, 
            "total_comments": comments, 
            "total_friends": friends,
            "hashtags": hashtags_selected,
        }
    )

    if serializer_admin.is_valid():
        result = serializer_admin.save()
        return Response(InstaStampResultSerializer(result).data)        
    else: 
        return Response(serializer.errors)