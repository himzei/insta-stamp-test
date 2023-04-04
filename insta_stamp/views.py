import re
import requests
import json 
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from bs4 import BeautifulSoup
from .serializers import InstaStampListSerializer
from .models import InstaStampList


class Crawling(APIView): 
    
    def get_object(self, insta_ref): 
        try: 
            return InstaStampList.objects.get(insta_ref=insta_ref)
        except InstaStampList.DoesNotExist:
            raise NotFound
    
    def put(self, request): 
        
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
                self.get_object(insta_ref),
                data = {
                  "likes_cnt": likes, 
                  "comments_cnt": comments, 
                  "friends_cnt": len(friends),
                },
                partial=True,
            )

            if serializer.is_valid(): 
                serializer.save()
                
        
        return Response({"ok": "True"})


    
    def post(self, request): 
        url = request.data.get("url")
        print(url)
        stamp = False

        keyword = ["코딩", "스탬프인증"]
        pattern = '#([0-9a-zA-Z가-힣]*)'
        hash_w = re.compile(pattern)

        stamp_url = url
        url = f"{stamp_url}?__a=1" # 크롤링할 게시물 URL
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if url.split("/p/")[1].split("/")[0]:
            insta_ref = url.split("/p/")[1].split("/")[0]
        else: 
            insta_ref = ""
        
        insta_date = soup.find("script", {"type": "application/ld+json"}).text
        insta_date = json.loads(insta_date)
        insta_date = insta_date["dateCreated"][0:16]

        data = soup.find("title").text
        hashtags = hash_w.findall(data)

        userid = data.split("on Instagram")[0].strip()
      
        if any(x in hashtags for x in keyword): 
            stamp = True


        serializer = InstaStampListSerializer(
            data={
              "insta_url": url,
              "insta_name": userid, 
              "insta_date": insta_date,
              "insta_stamp": stamp, 
              "insta_ref": insta_ref,
            }, 


        )
        if serializer.is_valid(): 
            insta_stamp = serializer.save()
            return Response(InstaStampListSerializer(insta_stamp).data)
        else: 
            return Response(serializer.errors)
        

        




