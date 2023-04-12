import csv
import datetime as dt
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response 
from insta_stamp.models import InstaStampList
from .models import InstaStampResult, InstaKeywords
from rest_framework.exceptions import NotFound
from insta_stamp.serializers import InstaStampListSerializer
from .serializers import InstaStampResultSerializer, KeywordsSerializer



class KeywordsUpdate(APIView): 
    
    def get_object(self, pk):
        try: 
            return InstaKeywords.objects.get(pk=pk)
        except InstaKeywords.DoesNotExist:
            raise NotFound
    
    def get(self, request): 
        keywords = InstaKeywords.objects.get(pk=1)
        serializer = KeywordsSerializer(keywords)
        return Response({"data": serializer.data, "ok": "True", })
    
    def put(self, request):
        pk = 1
        keywords = request.data.get("keywords")
        serializer = KeywordsSerializer(
            self.get_object(pk),
            data={
              "keywords": keywords,
            },
            partial=True,
        )
        if serializer.is_valid():
            serializer.save()

        return Response({"keywords": keywords})     
    

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
        all_insta_stamp = InstaStampList.objects.all()
        count = len(all_insta_stamp)

        comments = 0
        likes = 0 
        friends = 0
        for insta_list in all_insta_stamp: 
            comments += insta_list.comments_cnt
            likes += insta_list.likes_cnt
            friends += insta_list.friends_cnt
        

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

        

        
        

        
            
        
