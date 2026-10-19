from django.contrib import admin
from .models import Campsite, Booking

# Campsiteの管理画面カスタマイズ
class CampsiteAdmin(admin.ModelAdmin):
    # 一覧画面に表示する列を指定
    list_display = ('name', 'capacity', 'price_per_tent_stay', 'price_per_tent_day')

# Booking（予約）の管理画面カスタマイズ
class BookingAdmin(admin.ModelAdmin):
    # 一覧画面をエクセル表のように列で並べる
    list_display = ('campsite', 'plan_type', 'user', 'check_in', 'check_out', 'tent_count', 'status')
    
    # 右側に「ステータス」や「プラン」で絞り込むフィルターメニューを追加
    list_filter = ('status', 'plan_type', 'campsite')
    
    # ユーザー名で検索できる検索窓を追加
    search_fields = ('user__username',)
    
    # 上部に「日付」で絞り込めるカレンダーナビゲーションを追加
    date_hierarchy = 'check_in'

# カスタマイズした設定を適用して登録
admin.site.register(Campsite, CampsiteAdmin)
admin.site.register(Booking, BookingAdmin)