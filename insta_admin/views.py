import csv
import datetime as dt
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response 
from insta_stamp.models import InstaStampList
from .models import InstaStampResult, InstaKeywords, InstaSetting
from rest_framework.exceptions import NotFound
from insta_stamp.serializers import InstaStampListSerializer
from .serializers import InstaStampResultSerializer, KeywordsSerializer, InstaSettingSerializer
from django.core.paginator import Paginator

# 팔로워 아이디 확인
import time 
import sys 
from selenium import webdriver
from bs4 import BeautifulSoup





class KeywordsUpdate(APIView): 
    
    def get_object(self, pk):
        try: 
            return InstaSetting.objects.get(pk=pk)
        except InstaKeywords.DoesNotExist:
            raise NotFound
    
    def get(self, request): 
        events_name = request.query_params.get("name")

        insta_setting = InstaSetting.objects.get(events_name=events_name)
        serializer = InstaSettingSerializer(insta_setting)

        hashtags = InstaKeywords.objects.filter(insta_setting_ref=insta_setting.pk)
        serializer_hashtags = KeywordsSerializer(hashtags, many=True)
        hashtags_one = [item for item in hashtags if item.pk == insta_setting.hashtags_selected]

        hashtags_one = str(hashtags_one[0])

        return Response({
            "hashtag": hashtags_one,
            "data": serializer.data, 
            "hashtags": serializer_hashtags.data, 
            })
    
    def put(self, request):
        hashtags_selected = request.data.get("hashtag")
        data_id = request.data.get("dataId")

        serializer = InstaSettingSerializer(
            self.get_object(data_id),
            data={
              "hashtags_selected": hashtags_selected,
            },
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()

        return Response({"ok": True})   

    def arrays_equal(self, arr1, arr2): 
        if len(arr1) != len(arr2): 
            return False 

        for i in range(len(arr1)):
            if arr1[i] != arr2[i]:
                return False

        return True
      
    
    def post(self, request): 
        data_id = request.data.get("dataId")
        keywords = request.data.get("keywords")

        existed_hashtags = InstaKeywords.objects.values('keywords').filter(insta_setting_ref=data_id)
        
        
        print(list(existed_hashtags))



        serializer = KeywordsSerializer( 
            data = {
              "keywords": keywords, 
              "insta_setting_ref": data_id,
            }
        )

        if serializer.is_valid():
            result = serializer.save()
            return Response(KeywordsSerializer(result).data)
        else: 
            return Response(serializer.errors)
    

class ChartView(APIView): 
    
    def get(self, request): 
        data = InstaStampResult.objects.filter(created_at__gte=dt.datetime(2023, 4, 10)).order_by("created_at")[:20]
        serializer = InstaStampResultSerializer(data, many=True)
        
        
        return Response(serializer.data)


class CSVDownloadView(APIView):

    def get(self, request): 
        data = InstaStampResult.objects.all()
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="result.csv"'
        writer = csv.writer(response)

        writer.writerow([
            "작성시간", 
            "총 인스타 수", 
            "총 좋아요 수", 
            "총 댓글 수", 
            "총 친구소환 수",
        ])

        for row in data: 
            writer.writerow([
                row.created_at, 
                row.total_insta, 
                row.total_likes, 
                row.total_comments, 
                row.total_friends,
            ])

        return response
    

class AdminInstaStampList(APIView): 
    
    def get(self, request): 
        hashtags_id = request.query_params.get("hashtagsId")

        try: 
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError: 
            page = 1

        all_insta_stamp = InstaStampList.objects.filter(hashtags=hashtags_id)
        page_size = 20
        count = len(all_insta_stamp)

        comments = 0
        likes = 0 
        friends = 0
        for insta_list in all_insta_stamp: 
            comments += insta_list.comments_cnt
            likes += insta_list.likes_cnt
            friends += insta_list.friends_cnt
        
        paginator = Paginator(all_insta_stamp, page_size, orphans=5)
        serializer = InstaStampListSerializer(
            paginator.get_page(page), 
            many=True, 
        )
        return Response({
            "count": count, 
            "friends": friends, 
            "likes": likes, 
            "comments": comments, 
            "instaRegister": serializer.data
        })


class AdminInataStampResult(APIView): 

    def get(self, request):
        hashtags_id = request.query_params.get("hashtagsId")
        try: 
            page = request.query_params.get("page", 1)
            page = int(page)
        except ValueError: 
            page = 1

        all_list = InstaStampResult.objects.filter(hashtags=hashtags_id).order_by("-created_at")

        page_size = 20
        # 왜 2배수가 잡히는 지 모르겠음
        total_page = len(all_list) 

        
        paginator = Paginator(all_list, page_size, orphans=5)
        serializer = InstaStampResultSerializer(paginator.get_page(page), many=True)
        return Response({"data": serializer.data, "totalPage": total_page})
    
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

        

        
        

        
            
        
