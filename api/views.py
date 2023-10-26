from django.shortcuts import render
from rest_framework import viewsets
from .serializers import DelaySerializer
from .models import Delay
from crawling.crawling_metro import search
from django.db.models import Q
import datetime

# Create your views here.
class DelayViewSet(viewsets.ModelViewSet):
    queryset = Delay.objects.all()
    # queryset = Delay.objects.filter(number="4호선")

    serializer_class = DelaySerializer

    def get_queryset(self) :
        number = self.request.query_params.get("number", None)

        today = datetime.datetime.today().date()

        q = Q(number=number, start__lte=today, end__gte=today)
       

        # queryset = Delay.objects.filter(q)

        if number is not None:

            queryset = Delay.objects.filter(q)
        else :
            queryset = Delay.objects.all()

        return queryset


# 스케줄링 메소드 (메 시간 실행됨)
def crawling():
    search()

    # 날짜 지난 데이터 삭제 하기
    today = datetime.datetime.now()
    # today = datetime.datetime.strptime("2023-09-20", "%Y-%m-%d")

    q = Delay.objects.filter(end__lt=today)
    q.delete()