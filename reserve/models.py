from django.db import models
from django.contrib.auth.models import User  # Django標準のユーザー管理機能を流用
from django.utils import timezone

class Campsite(models.Model):
    """キャンプ場の区画（サイト）情報を管理するテーブル"""
    name = models.CharField("サイト名", max_length=50)  # 例：常設テントサイト、持ち込みテントサイト
    capacity = models.IntegerField("定員（名）", default=4)
    price_stay = models.IntegerField("1泊あたりの料金")
    price_day = models.IntegerField("日帰りの料金", blank=True, null=True)
    description = models.TextField("説明", blank=True, null=True)

    def __str__(self):
        # 管理画面などで表示される名前を設定
        return f"{self.name}（定員: {self.capacity}名）"


class Booking(models.Model):
    """予約情報を管理するテーブル"""
    # 誰が予約したか（Userが削除されたら、紐づく予約も消える設定）
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="予約者")
    
    # どのサイトを予約したか
    campsite = models.ForeignKey(Campsite, on_delete=models.CASCADE, verbose_name="サイト")

    # 宿泊か日帰りか選択
    PLAN_CHOICES = (
        ('STAY', '宿泊'),
        ('DAY', '日帰り'),
    )
    plan_type = models.CharField("利用プラン", max_length=10, choices=PLAN_CHOICES, default='STAY')
    
    # いつからいつまでか
    check_in = models.DateField("チェックイン日")
    check_out = models.DateField("チェックアウト日")
    
    # 予約された日時（自動で現在時刻が入る）
    created_at = models.DateTimeField("予約受付日時", default=timezone.now)

    # 予約の状態（キャンセル機能用）
    STATUS_CHOICES = (
        ('CONFIRMED', '予約確定'),
        ('CANCELLED', 'キャンセル'),
    )
    status = models.CharField("ステータス", max_length=15, choices=STATUS_CHOICES, default='CONFIRMED')

    def __str__(self):
        return f"{self.campsite.name} : {self.check_in} ~ {self.check_out} ({self.user.username}様)"