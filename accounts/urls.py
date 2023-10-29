from django.urls import path
from .views import *


urlpatterns = [
    path('createuser',Createuser),
    path('getuser',getuser),
    path('checkemail',checkemail),
    path('getcards',getcards),
    path("reject",reject),
    path("liked",liked),
    path("likedlist",likedlist),
    path("getuserprofilepicture",getuserprofilepicture),
    path("matchedlist",Matchedlist),
    path("addtomatches",addtomatches),
    path("fetch_users_by_interest",fetch_users_by_interest)
]