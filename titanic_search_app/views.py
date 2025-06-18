from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Passenger

def search_view(request):

    # 検索条件を格納する変数を初期化
    selected_age_category = request.GET.get('age_category') # HTMLのname属性に合わせる
    selected_sex = request.GET.get('sex')
    selected_pclass = request.GET.get('pclass')
    selected_survived = request.GET.get('survived')

    # 検索結果と件数を初期化 (最初は検索結果なしの状態)
    search_results = None
    result_count = 0
    error_message = None # エラーメッセージ表示用

    # 年齢区分の定義
    AGE_RANGES = {
        '0-4': (0, 4),
        '5-14': (5, 14),
        '15-24': (15, 24),
        '25-44': (25, 44),
        '45-64': (45, 64),
        '65+': (65, 200), # 上限は適当に大きめの値
    }

    # 検索が実行されたかどうかを判定
    is_search = selected_age_category is not None # age_category が request.GET に含まれていたらTrue
    print(is_search)

    # 検索処理
    if is_search:
    # 年齢の必須検証
        if not selected_age_category: # value="" が送信された場合など
            error_message = "＊年齢を選択してください。年齢は必須選択項目です。" 
            
        else:
            # Django ORM クエリの開始
            queryset = Passenger.objects.all()

            # --- 各条件でフィルタリング（AND検索）---
            # 年齢
            age_range = AGE_RANGES.get(selected_age_category)
            if age_range:
                queryset = queryset.filter(age__range=age_range)

            # 性別
            if selected_sex in ['0', '1']: # 有効な値かチェック
                queryset = queryset.filter(sex=(selected_sex == '1')) # 1 なら True, 0 なら False に変換

            # 旅客クラス
            if selected_pclass in ['1', '2', '3']: 
                queryset = queryset.filter(pclass=int(selected_pclass)) # 文字列を整数に変換

            # 生存状況
            if selected_survived in ['0', '1']: 
                queryset = queryset.filter(survived=(selected_survived == '1')) # 1 なら True, 0 なら False に変換
            # --- フィルタリング終了 ---

            # 検索結果を取得（クエリセット実行）
            search_results = queryset.all() # .all() 明示的に結果を取得する意図

            # 検索結果の件数を取得
            result_count = search_results.count() # または queryset.count()

    # context に検索結果などを追加してテンプレートに渡す
    context = {
        'title': 'タイタニック号乗客者検索', 
        # 'form_options': AGE_RANGES.keys(), # テンプレートで年齢区分の選択肢を再表示するために渡す
        'selected_age_category': selected_age_category, # 選択状態を保持するために渡す
        'selected_sex': selected_sex,
        'selected_pclass': selected_pclass,
        'selected_survived': selected_survived,
        'search_results': search_results, # 検索結果のリスト (検索してない場合は None)
        'result_count': result_count, # 検索結果の件数
        'error_message': error_message, # エラーメッセージ
    }
    return render(request,'search.html',context)
