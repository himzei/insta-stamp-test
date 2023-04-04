import re
import requests
from bs4 import BeautifulSoup
from insta_stamp.models import InstaStampList
from insta_stamp.serializers import InstaStampListSerializer
from rest_framework.exceptions import NotFound

def get_object(insta_ref): 
    try: 
        return InstaStampList.objects.get(insta_ref=insta_ref)
    except InstaStampList.DoesNotExist:
        raise NotFound

def schedule_api():
    
    all_insta_url = InstaStampList.objects.values_list("insta_url")

    for url in all_insta_url: 
        
        response = requests.get(url[0])
        insta_ref = url[0].split("/p/")[1].split("/")[0]

        soup = BeautifulSoup(response.text, "html.parser")

        dataUser = soup.find("title").text 

        # 친구 소환
        pattern = '@([0-9a-zA-Z가-힣_]*)'
        hash_f = re.compile(pattern)
        friends = hash_f.findall(dataUser)
        friends = list(filter(None, friends))

        # 좋아요, 커멘트 수 크롤링
        data = soup.find("meta", {"name": "description"})
        likes = data.split("Likes,")[0].strip()
        likes = likes.replace(",","")
        comments = data.split("comments")[0].split("likes,")[1]
        comments = comments.replace(",","")

        

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
            
    
    return