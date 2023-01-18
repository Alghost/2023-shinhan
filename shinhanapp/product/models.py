from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='회원')
    title = models.CharField(max_length=128, verbose_name='상품명')
    content = models.TextField(verbose_name='상품내용')
    price = models.IntegerField(verbose_name='가격')
    location = models.CharField(max_length=256, verbose_name="위치")

    # 중간에 추가했기 때문에 makemigrations, migrate 실행
    image = models.FileField(null=True, blank=True, verbose_name='이미지')

    class Meta:
        db_table = 'shinhan_product'
        verbose_name = '상품'
        verbose_name_plural = '상품'