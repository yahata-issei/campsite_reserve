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

        # 1. 日付の妥当性チェック
        try:
            check_in = datetime.strptime(check_in_str, '%Y-%m-%d').date()
            check_out = datetime.strptime(check_out_str, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            return render(request, 'reserve/booking_result.html', {
                'error': True, 'message': '⚠️ 日付を正しく指定してください。'
            })

        if check_in >= check_out:
            return render(request, 'reserve/booking_result.html', {
                'error': True, 'message': '⚠️ チェックアウト日は利用開始日より後の日付を選択してください。'
            })

        campsite = get_object_or_404(Campsite, id=campsite_id)

        # 2. 日付の重複判定ロジック
        overlapping_bookings = Booking.objects.filter(
            campsite=campsite,
            status='CONFIRMED',
            check_in__lt=check_out,
            check_out__gt=check_in
        )

        if overlapping_bookings.exists():
            return render(request, 'reserve/booking_result.html', {
                'error': True, 
                'message': f'❌ 申し訳ありません。{campsite.name} は指定された期間に先客の予約が入っています。'
            })

        # 3. ユーザー情報の取得（開発用）
        user = request.user if request.user.is_authenticated else User.objects.first()
        if not user:
            return render(request, 'reserve/booking_result.html', {
                'error': True, 'message': '⚠️ ユーザー情報が見つかりません。管理画面でスーパーユーザーを作成してください。'
            })

        # 4. 予約の作成・保存
        booking = Booking.objects.create(
            user=user,
            campsite=campsite,
            plan_type=plan_type,
            tent_count=tent_count,
            check_in=check_in,
            check_out=check_out,
            status='CONFIRMED'
        )

        # 5. 予約成功のデータをHTMLに渡して返す
        return render(request, 'reserve/booking_result.html', {
            'error': False,
            'campsite': campsite,
            'tent_count': tent_count,
            'plan_name': booking.get_plan_type_display(),
            'check_in': check_in,
            'check_out': check_out,
            'total_price': f"{booking.total_price:,}"
        })

    return HttpResponse('<p style="color: red;">不正なアクセスです。</p>')