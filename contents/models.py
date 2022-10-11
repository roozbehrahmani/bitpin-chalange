from django.db import models

from users.models import User


# Create your models here.
class Content(models.Model):
    title = models.CharField(
        max_length=100,
        verbose_name="title",
    )
    text = models.TextField(
        blank=True,
        verbose_name="text",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="created at",
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "content"
        verbose_name_plural = "contents"


class UserContentReview(models.Model):
    One = 1
    Two = 2
    Tree = 3
    Four = 4
    Five = 5

    STAR_CHOICES = (
        (One, 'One'),
        (Two, 'Two'),
        (Tree, 'Tree'),
        (Four, 'Four'),
        (Five, 'Five'),
    )

    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        null=True,
        related_name='users',
        verbose_name="user",
    )
    content = models.ForeignKey(
        to=Content,
        on_delete=models.CASCADE,
        null=True,
        related_name='contents',
        verbose_name="content",
    )
    star = models.IntegerField(
        choices=STAR_CHOICES,
        null=True,
        verbose_name='star'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="created at",
    )
    updated_at = models.DateTimeField(
        auto_now_add=True,
        null=True,
        verbose_name="updated at",
    )

    class Meta:
        verbose_name = "Users Contents Review "
        verbose_name_plural = "User Content Review"
