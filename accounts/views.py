from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token  # Import the Token model
from .models import *
from .serializer import *
import os
import base64
import uuid

@api_view(["POST"])
def Createuser(request):
    existing_user = CustomUser.objects.filter(email=request.data["email"]).first()
    
    if existing_user:
        return Response({"error": "User with this email already exists.", "status": False})

    user_data = {
        "email": request.data["email"],
        "name": request.data["name"],
        "birthday": request.data["dob"],
        "gender": request.data["gender"],
    }

    # Create a CustomUser object
    account_obj = CustomUser(**user_data)
    account_obj.save()

    selected_images = request.data.get('selectedImages', [])
    selected_images_list = [str(item.strip()) for item in selected_images.strip('[]').split(',')]

    print("Number of images received:", len(selected_images_list))

    for image_data in selected_images_list:
        ext = "jpg"
        image_data = base64.b64decode(image_data)

        # Save the image to a folder
        image_directory = "profileimages"
        if not os.path.exists(image_directory):
            os.makedirs(image_directory)

        # Generate a unique filename for each image
        image_filename = f"{account_obj.id}_{uuid.uuid4()}.{ext}"
        image_path = os.path.join(image_directory, image_filename)

        with open(image_path, "wb") as f:
            f.write(image_data)

        # Create an Image object for each image and associate it with the user
        image, created = Image.objects.get_or_create(image=image_path)
        account_obj.image.add(image)

    selected_buttons = request.data.get('selectedButtons', [])  # Get selectedButtons as a list
    selected_buttons_list = [int(item.strip()) for item in selected_buttons.strip('[]').split(',')]

    interest_mapping = {
        0: 'Gaming',
        1: 'Dancing',
        2: 'Language',
        3: 'Music',
        4: 'Movie',
        5: 'Photography',
        6: 'Architecture',
        7: 'Fashion',
        8: 'Book',
        9: 'Writing',
        10: 'Nature',
        11: 'Painting',
        12: 'Football',
        13: 'People',
        14: 'Animals',
        15: 'Gym & Fitness',
        # Add more mappings as needed
    }

    interest_names = [interest_mapping.get(number, 'Unknown') for number in selected_buttons_list]

    for interest_name in interest_names:
        interest, created = Interest.objects.get_or_create(name=interest_name)
        account_obj.interest.add(interest)

    # Generate a token for the user
    token, _ = Token.objects.get_or_create(user=account_obj)

    # Return the token in the response
    response_data = {
        "status": True,
        "token": token.key  # Include the token in the response
    }

    return Response(response_data)


@api_view(["get"])
def getuser(request):
        accountserializer=CustomUserSerializer(request.user).data
        # print(accountserializer)

        return Response(accountserializer)

@api_view(["post"])
def checkemail(request):
        existing_user = CustomUser.objects.filter(email=request.data["email"]).first()
        if existing_user:
           account_obj=CustomUser.objects.get(email=request.data["email"])
           token, _ = Token.objects.get_or_create(user=account_obj)

           return Response({"error": "User with this email already exists.", "status": False,"token": token.key})
        
        else:
               return Response({"status":True})
        

@api_view(["GET"])
def getcards(request):
    account_obj = request.user
    gender = account_obj.gender
    # gender="Female"

    rejected_ids = [rejected.user for rejected in account_obj.rejected.all()]
    liked_ids = [liked.user for liked in account_obj.liked.all()]
    matched_ids = [matches.user for matches in account_obj.matches.all()]

    print(matched_ids)

    if gender == "Male":
        getuser = CustomUser.objects.filter(gender="Female").exclude(id__in=rejected_ids).exclude(id__in=liked_ids).exclude(id__in=matched_ids)
    else:
        getuser = CustomUser.objects.filter(gender="Male").exclude(id__in=rejected_ids).exclude(id__in=liked_ids).exclude(id__in=matched_ids)

    if getuser.exists():
        print("Users found")
    else:
        print("No users found")

    serialized_users = CustomUserSerializer(getuser, many=True).data

    return Response({"cards": serialized_users}) 

@api_view(["POST"])
def reject(request):
     print(request.data["rejectedid"])

     account_obj=request.user

     reject, created = RejectedCards.objects.get_or_create(user=request.data["rejectedid"])
     account_obj.rejected.add(reject)

     return Response(True)

@api_view(["POST"])
def liked(request):
     print(request.data["likedid"])

     account_obj=request.user

     liked, created = LikedCards.objects.get_or_create(user=request.data["likedid"])
     account_obj.liked.add(liked)

     user_obj=CustomUser.objects.get(id=request.data["likedid"])
     
     likedUser, created = LikedYou.objects.get_or_create(user=account_obj.id)
     
     user_obj.likedyou.add(likedUser)

     return Response(True)


@api_view(["GET"])
def likedlist(request):
     account_obj=request.user

     liked_ids = [liked.user for liked in account_obj.likedyou.all()]
     data=CustomUser.objects.filter(id__in=liked_ids)

     serializeddata=CustomUserSerializer(data,many=True).data

     return Response(serializeddata)


@api_view(["GET"])
def getuserprofilepicture(request):
     account_obj=request.user

     image_obj=ImageSerializer(account_obj.image,many=True).data

     return Response(image_obj[0])
     

@api_view(["POST"])
def addtomatches(request):
     account_obj=request.user


     matched, created = Matches.objects.get_or_create(user=request.data["matchedid"])
     account_obj.matches.add(matched)

     account_obj.likedyou.filter(user=request.data["matchedid"]).delete()

     user_obj=CustomUser.objects.get(id=request.data["matchedid"])
     
     matches, created = Matches.objects.get_or_create(user=account_obj.id)
     
     user_obj.matches.add(matches)

     user_obj.liked.filter(user=account_obj.id).delete()
     

     image_obj=ImageSerializer(account_obj.image,many=True).data

     details={
          "yourprofilepicture":image_obj[0]
     }

     return Response({"status":True,"details":details})

@api_view(["GET"])
def Matchedlist(request):
     account_obj=request.user

     matches_ids = [matches.user for matches in account_obj.matches.all()]
     data=CustomUser.objects.filter(id__in=matches_ids)

     serializeddata=CustomUserSerializer(data,many=True).data

     return Response(serializeddata)

@api_view(["GET"])
def fetch_users_by_interest(request):
    current_user = request.user
    user_gender = current_user.gender  # Assuming the current user's gender is already set

    # Determine the opposite gender based on the current user's gender
    opposite_gender = "Female" if user_gender == "Male" else "Male"

    # Get the current user's interests
    current_user_interests = current_user.interest.all()

    # Create a dictionary to store users by interests
    user_interest_categories = {}

    # Find users of the opposite gender who share at least one interest with the current user
    matching_users = CustomUser.objects.filter(
        gender=opposite_gender,  # Filter by opposite gender
        interest__in=current_user_interests  # Filter by shared interests
    ).exclude(id=current_user.id)  # Exclude the current user from the results

    # Organize users by interests
    for user in matching_users:
        user_interests = user.interest.all()

        for interest in user_interests:
            interest_name = interest.name

            if interest_name not in user_interest_categories:
                user_interest_categories[interest_name] = []

            # Check if the user is already in the list for this interest
            if (
                user not in user_interest_categories[interest_name] and
                user not in current_user.liked.all() and  # Exclude liked users
                user not in current_user.likedyou.all() and  # Exclude users who liked the current user
                user not in current_user.matches.all()  # Exclude matched users
            ):
                user_interest_categories[interest_name].append(user)

    # Create a dictionary for each category and add it to the categories list
    categories = []
    for interest, users in user_interest_categories.items():
        category = {
            "title": interest,
            "users": CustomUserSerializer(users, many=True).data
        }
        categories.append(category)

    return Response(categories)