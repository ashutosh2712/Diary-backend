from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Diary
from .serializers import DiarySerializer


# Create your views here.


@api_view(["POST"])
def registerUser(request):
    if request.method == "POST":
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        confirmPassword = request.data.get("confirmPassword")

        if password != confirmPassword:
            return Response(
                {"error": "passwords dont matech"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
        except IntegrityError:
            return Response(
                {"error": "User Already exists!"}, status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {"success": "User created successfully"}, status=status.HTTP_201_CREATED
        )


@api_view(["POST"])
def loginUser(request):
    if request.method == "POST":
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return Response(
                {"success": "user loged in successfully!"}, status=status.HTTP_200_OK
            )

        else:
            return Response(
                {"error": "Invalid credintial"}, status=status.HTTP_401_UNAUTHORIZED
            )


@api_view(["POST"])
def logoutUser(request):
    if request.method == "POST":
        logout(request)

    return Response(
        {"success": "user logged out successfully"}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
def getRoutes(request):
    return Response("Wellcome to Backend Of Diary App!")


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
