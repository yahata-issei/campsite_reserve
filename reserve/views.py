from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Campsite, Booking

def index(request):
    """トップページ：サイト一覧の表示"""
    campsites = Campsite.objects.all()
    context = {'campsites': campsites}
    return render(request, 'reserve/index.html', context)


def create_booking(request):
    """htmxからの予約リクエストを処理し、重複チェックと予約保存を行う"""
    if request.method == 'POST':
        campsite_id = request.POST.get('campsite_id')
        plan_type = request.POST.get('plan_type')
        tent_count = int(request.POST.get('tent_count', 1))
        check_in_str = request.POST.get('check_in')
        check_out_str = request.POST.get('check_out')

        try:
            check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return HttpResponse('<p style="color: red; margin-top: 10px;">⚠️ 日付を正しく指定してください。</p>')

        if check_in >= check_out:
            return HttpResponse('<p style="color: red; margin-top: 10px;">⚠️ チェックアウト日は利用開始日より後の日付を選択してください。</p>')

        campsite = get_object_or_404(Campsite, id=campsite_id)

        overlapping_bookings = Booking.objects.filter(
            campsite=campsite,
            status='CONFIRMED',
            check_in__lt=check_out,
            check_out__gt=check_in
        )

        if overlapping_bookings.exists():
            return HttpResponse(
                f'<p style="color: #d9534f; margin-top: 10px;">'
                f'❌ 申し訳ありません。{campsite.name} は指定された期間（{check_in} 〜 {check_out}）に先客の予約が入っています。'
                f'</p>'
            )

        user = request.user if request.user.is_authenticated else User.objects.first()
        if not user:
            return HttpResponse('<p style="color: red; margin-top: 10px;">⚠️ ユーザー情報が見つかりません。管理画面でスーパーユーザーを作成してください。</p>')

        booking = Booking.objects.create(
            user=user,
            campsite=campsite,
            plan_type=plan_type,
            tent_count=tent_count,
            check_in=check_in,
            check_out=check_out,
            status='CONFIRMED'
        )

        return HttpResponse(
            f'<div style="background-color: #d4edda; color: #155724; padding: 10px; border-radius: 5px; margin-top: 10px;">'
            f'<strong>✅ 予約が完了しました！</strong><br>'
            f'サイト: {campsite.name}（{tent_count}張り / {booking.get_plan_type_display()}）<br>'
            f'期間: {check_in} 〜 {check_out}<br>'
            f'合計金額: <strong>{booking.total_price:,} 円</strong>'
            f'</div>'
        )

    return HttpResponse('<p style="color: red;">不正なアクセスです。</p>')