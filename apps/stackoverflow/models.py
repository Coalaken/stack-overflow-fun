from django.db import models

from apps.utils.models import Timestamps
from django.conf import settings


class Question(Timestamps):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='user_questions', on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    question = models.TextField()
    
    def __str__(self) -> str:
        return self.title

    class Meta:
        indexes = [
            models.Index(fields=["user"])
        ]


class QuestionImage(Timestamps):
    question = models.ForeignKey(
        Question, related_name='question_images', on_delete=models.CASCADE
    )
    url = models.URLField()


class Answer(Timestamps):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='questions', on_delete=models.CASCADE
    )
    question = models.ForeignKey(
        Question, related_name='answers', on_delete=models.CASCADE
    )
    answer = models.TextField()


class AnswerImage(Timestamps):
    answer = models.ForeignKey(
        Question, related_name='images', on_delete=models.CASCADE
    )
    url = models.URLField()


