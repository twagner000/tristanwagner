from django.contrib import admin
from .models import BGGUserSearch, BGGGame, BGGUser, BGGUserRating

class BGGUserSearchAdmin(admin.ModelAdmin):
    model = BGGUserSearch
    list_display = ('__str__', 'search_date')
    
class BGGUserRatingAdmin(admin.ModelAdmin):
    model = BGGUserRating
    list_display = ('user','game','rating','numplays','date_created','date_updated')
    list_filter = ['user','game']

admin.site.register(BGGUserSearch, BGGUserSearchAdmin)
admin.site.register(BGGGame)
admin.site.register(BGGUser)
admin.site.register(BGGUserRating, BGGUserRatingAdmin)