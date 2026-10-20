from django.contrib.auth.models import User
from django.db import models
from django.templatetags.static import static
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('category', kwargs={'category_id': self.pk})


class Game(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to='games/')
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    torrent = models.FileField(upload_to='torrents/', blank=True, null=True)

    def get_absolute_url(self):
        return reverse('game_detail', kwargs={'pk': self.pk})

    def get_image_game(self):
        if self.image:
            return self.image.url
        return static('xgame/img/no-image.svg')

    def get_video(self):
        return self.video.url if self.video else ''

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Author")
    text = models.TextField(verbose_name="comment")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="date of comment")
    game = models.ForeignKey(Game, on_delete=models.CASCADE, verbose_name='Game')

    def __str__(self):
        return f'{self.user} on {self.game}'

    class Meta:
        verbose_name = 'comments'
        verbose_name_plural = "comments"
