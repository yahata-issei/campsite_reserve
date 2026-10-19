from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Campsite(models.Model):
    """キャンプ場の区画（サイト）情報を管理するテーブル"""
    name = models.CharField("サイト名", max_length=50)
    capacity = models.IntegerField("定員（名）", default=4)
    
    # 料金設定（1張りあたり）
    price_per_tent_stay = models.IntegerField("宿泊料金（1張りあたり）", default=0)
    price_per_tent_day = models.IntegerField("日帰り料金（1張りあたり）", blank=True, null=True)
    
    description = models.TextField("説明", blank=True, null=True)

    def __str__(self):
        return f"{self.name}（定員: {self.capacity}名）"


class Booking(models.Model):
    """予約情報を管理するテーブル"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="予約者")
    campsite = models.ForeignKey(Campsite, on_delete=models.CASCADE, verbose_name="サイト")
    
    # 宿泊 or 日帰り
    PLAN_CHOICES = (
        ('STAY', '宿泊'),
        ('DAY', '日帰り'),
    )
    plan_type = models.CharField("利用プラン", max_length=10, choices=PLAN_CHOICES, default='STAY')
    
    # テント・タープの数（料金計算に使用）
    tent_count = models.IntegerField("テント・タープの数（張り）", default=1)
    
    check_in = models.DateField("利用開始日")
    check_out = models.DateField("利用終了日")
    created_at = models.DateTimeField("予約受付日時", default=timezone.now)
    
    STATUS_CHOICES = (
        ('CONFIRMED', '予約確定'),
        ('CANCELLED', 'キャンセル'),
    )
    status = models.CharField("ステータス", max_length=15, choices=STATUS_CHOICES, default='CONFIRMED')

    def __str__(self):
        plan_name = dict(self.PLAN_CHOICES).get(self.plan_type)
        return f"[{plan_name}] {self.campsite.name} : {self.check_in} ~ {self.check_out} ({self.tent_count}張り)"

    # 合計金額を自動計算するプロパティ
    @property
    def total_price(self):
        if self.plan_type == 'STAY':
            return self.campsite.price_per_tent_stay * self.tent_count
        elif self.plan_type == 'DAY' and self.campsite.price_per_tent_day:
            return self.campsite.price_per_tent_day * self.tent_count
        return 0