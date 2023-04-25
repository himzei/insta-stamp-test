import re
import requests
import json 
import csv
from django.http import HttpResponse
from rest_framework.views import APIView 
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework import status
from bs4 import BeautifulSoup
from .serializers import InstaStampListSerializer
from .models import InstaStampList
from insta_admin.models import InstaKeywords, InstaSetting
from insta_admin.serializers import KeywordsSerializer

import pandas as pd 


class DataForceInsert(APIView): 
    
    def get(self, request): 

        file = pd.read_excel(
            '/Users/himzei/Documents/Github/insta-stamp-test/insta_stamp/insta_list.xlsx', 
            header=None,
            sheet_name='Sheet1', 
            engine='openpyxl'
        )
        return Response({"file": file})
    
    def post(self, request): 
        file = pd.read_excel(
            '/Users/himzei/Documents/Github/insta-stamp-test/insta_stamp/insta_list.xlsx', 
            header=None,
            sheet_name='Sheet1', 
            engine='openpyxl'
        )

        for url in file[0]: 
            try:
                stamp = False

                url = f"{url}?__a=1" # 크롤링할 게시물 URL
                response = requests.get(url)
                soup = BeautifulSoup(response.text, 'html.parser')
                        
                insta_ref = url.split("/p/")[1].split("/")[0]
                

                insta_date = soup.find("script", {"type": "application/ld+json"}).text
                insta_date = json.loads(insta_date)
                insta_date = insta_date["dateCreated"][0:16]

                data = soup.find("title").text

                userid = data.split("on Instagram")[0].strip()


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
                    serializer.save()
            except:
                continue
            
        
        return Response({"ok": "true"})
    

class RankingList(APIView): 
    
    def get(self, request): 
        # 포론트에서 행사명을 받아온다 
        # 행사명으로 현재 선택되어진 해시택크 id를 구한다
        events_name = request.query_params.get("name")
        events = InstaSetting.objects.get(events_name=events_name)


        data = InstaStampList.objects.filter(hashtags=events.hashtags_selected).order_by('-likes_cnt')[:10]
        serializer = InstaStampListSerializer(
            data, 
            many=True,
        )
        return Response(serializer.data)
        


class CSVDownloadView(APIView):

    def get(self, request): 
        data = InstaStampList.objects.all()
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="result.csv"'
        writer = csv.writer(response)

        writer.writerow([
            "인스타 아이디", 
            "전화번호", 
            "인스타 URL", 
            "인증시간", 
            "인증여부", 
            "좋아요(개)", 
            "댓글(개)", 
            "친구소환(명)"
            ])
        
        for row in data: 
            writer.writerow([
                row.insta_name, 
                row.phone, 
                row.insta_url, 
                row.created_at, 
                row.insta_stamp, 
                row.likes_cnt, 
                row.comments_cnt, 
                row.friends_cnt,
                ])

        
        return response
    

class Crawling(APIView): 
    
    def get_object(self, insta_ref): 
        try: 
            return InstaStampList.objects.get(insta_ref=insta_ref)
        except InstaStampList.DoesNotExist:
            raise NotFound
        
    def removeComma(self, stringLikes):
        if ',' or "K" or "M" in stringLikes: 
            return stringLikes.replace(",","").replace("K", "000").replace("M","000000")
        else: 
            return stringLikes
    
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

            if data is None:
                ParseError("포스팅 된 글이 없습니다.")

            if 'Likes' in data: 
                likes = data.split("Likes,")[0].strip().split(" ")[-1]
                comments = data.split("Comments")[0].strip().split(' ')[-1]
            else: 
                likes = data.split("likes,")[0].strip().split(" ")[-1]
                comments = data.split("comments")[0].strip().split(' ')[-1]
            
            likes = self.removeComma(likes)
            comments = self.removeComma(comments)
            
            print(likes)
            print(comments)

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

    def check_array_element_match(self, array1, array2):
        return all(elements in array1 for elements in array2)
  
    def post(self, request): 
        
        url = request.data.get("url")
        events_name = request.data.get("ADM_EVENTS_NAME")
        print(url, events_name)
        stamp = False

        # 넘어온 이벤트 이름 값으로 
        # 해시태그 확인
        events = InstaSetting.objects.get(events_name=events_name)

        
        db_keywords = InstaKeywords.objects.get(pk=events.hashtags_selected)
       
        serializer_keywords = KeywordsSerializer(db_keywords)

        keywords = serializer_keywords.data.get("keywords").split(",")
        keywords = [element.strip() for element in keywords]

        pattern = '#([0-9a-zA-Z가-힣]*)'
        hash_w = re.compile(pattern)

        stamp_url = url
        url = f"{stamp_url}?__a=1" # 크롤링할 게시물 URL
        response = requests.get(url)

        soup = BeautifulSoup(response.text, 'html.parser')

                
        insta_ref = url.split("/p/")[1].split("/")[0]
        

        insta_date = soup.find("script", {"type": "application/ld+json"}).text
        insta_date = json.loads(insta_date)
        insta_date = insta_date["dateCreated"][0:16]

        data = soup.find("title").text
        hashtags = hash_w.findall(data)

        userid = data.split("on Instagram")[0].strip()
        stamp = self.check_array_element_match(hashtags, keywords)


        if stamp == False: 
            return Response(
                status=status.HTTP_405_METHOD_NOT_ALLOWED, 
                )
        

        serializer = InstaStampListSerializer(
            data={
              "insta_url": url,
              "insta_name": userid, 
              "insta_date": insta_date,
              "insta_stamp": stamp, 
              "insta_ref": insta_ref,
              "hashtags": events.hashtags_selected,
            }, 
        )
        if serializer.is_valid(): 
            insta_stamp = serializer.save()
            return Response({
                "data":InstaStampListSerializer(insta_stamp).data, 
                "keywords": keywords
                })
        else: 
            return Response(serializer.errors)
        

        




