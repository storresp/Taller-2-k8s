import datetime
from django.utils import timezone
from django.db import models


class Answer(models.Model):
    answer_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", default=timezone.now)

    def __str__(self):
        return self.answer_text
    
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)