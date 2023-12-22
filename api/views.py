from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Diary
from .serializers import DiarySerializer


# Create your views here.
@api_view(["GET"])
def getRoutes(request):
    return Response("Wellcome to Backend dor Diary App!")


@api_view(["GET"])
def getDiaryEntries(request):
    diaryEntries = Diary.objects.all()
    serializer = DiarySerializer(diaryEntries, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getDiaryEntry(request, pk):
    diaryentry = Diary.objects.get(id=pk)
    serializer = DiarySerializer(diaryentry, many=False)
    return Response(serializer.data)


@api_view(["POST"])
def createDiaryEntry(request):
    data = request.data
    diaryentry = Diary.objects.create(body=data["body"])
    serializer = DiarySerializer(diaryentry, many=False)
    return Response(serializer.data)


@api_view(["PUT"])
def updateDiaryEntry(request, pk):
    data = request.data
    diaryentry = Diary.objects.get(id=pk)
    serializer = DiarySerializer(instance=diaryentry, data=data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(["DELETE"])
def deleteDiaryEntry(request, pk):
    diaryentry = Diary.objects.get(id=pk)
    diaryentry.delete()

    return Response("Entries was deleted!")
