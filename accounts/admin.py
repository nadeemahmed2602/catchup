from django.contrib import admin

# Import the CustomUser model
from .models import *

# Register the CustomUser model with the admin site
admin.site.register(CustomUser)
admin.site.register(Interest)
admin.site.register(Image)
admin.site.register(RejectedCards)
admin.site.register(LikedCards)
admin.site.register(LikedYou)
admin.site.register(Matches)