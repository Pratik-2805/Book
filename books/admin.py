from django.contrib import admin
from .models import Books, Review, User
from django.utils.html import format_html


# Register your models here.
admin.site.register(Books)
admin.site.register(User)

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'gold_stars', 'comment', 'updated_at')

    def gold_stars(self, obj):
        return format_html(''.join([
            '<span style="color:gold;">&#9733;</span>' if i < obj.rating else '<span style="color:#ccc;">&#9733;</span>'
            for i in range(5)
        ]))
    gold_stars.short_description = 'Rating'

admin.site.register(Review, ReviewAdmin)