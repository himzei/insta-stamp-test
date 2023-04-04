from rest_framework.views import APIView
from rest_framework.response import Response 
from insta_stamp.models import InstaStampList
from insta_stamp.serializers import InstaStampListSerializer
from .serializers import InstaStampResultSerializer
from .models import InstaStampResult
import requests
from bs4 import BeautifulSoup
import re
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
        data = soup.find("meta", {"name": "description"})["content"]
        likes = data.split("Likes,")[0].strip()
        likes = likes.replace(",","")
        comments = data.split("Comments")[0].split("Likes,")[1].strip()
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
            
    

class AdminInstaStampList(APIView): 
    
    def get(self, request): 
        all_insta_stamp = InstaStampList.objects.all()
        count = len(all_insta_stamp)

        comments = 0
        likes = 0 
        friends = 0
        for list in all_insta_stamp: 
            comments += list.comments_cnt
            likes += list.likes_cnt
            friends += list.friends_cnt
        


        serializer = InstaStampListSerializer(
            all_insta_stamp, 
            many=True, 
        )
        return Response({
            "count":count, 
            "friends": friends, 
            "likes": likes, 
            "comments": comments, 
            "instaRegister": serializer.data} )

class AdminInataStampResult(APIView): 
    

    def get(self, request):
        all_list = InstaStampResult.objects.order_by("-created_at")
        serializer = InstaStampResultSerializer(all_list, many=True)
        return Response(serializer.data)
    
    def post(self, request): 
        all_insta_stamp = InstaStampList.objects.all()
        count = len(all_insta_stamp)

        comments = 0
        likes = 0 
        friends = 0
        for list in all_insta_stamp: 
            comments += list.comments_cnt
            likes += list.likes_cnt
            friends += list.friends_cnt
        
        serializer = InstaStampResultSerializer(
            data = {
                "total_insta": count, 
                "total_likes": likes, 
                "total_comments": comments, 
                "total_friends": friends,
            }
        )

        if serializer.is_valid():
            result = serializer.save()
            return Response(InstaStampResultSerializer(result).data)
        else: 
            return Response(serializer.errors)

        

        
        

        
            
        
