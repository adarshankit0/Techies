from django.contrib import admin
from .models import TestCase
from .models import *

admin.site.register(Problem)


admin.site.register(Submission)
admin.site.register(Leaderboard)
admin.site.register(Certificate)
admin.site.register(TestCase)