import csv
import os
from django.conf import settings
from django.db import transaction
# アプリ名とモデル名に合わせてインポートパスを変更
from titanic_search_app.models import Passenger

# --- CSVファイル ---
CSV_FILE_NAME = 'titanic_search_app/to_csv_titnic.csv'
# CSVファイルのエンコーディング
CSV_ENCODING = 'utf-8'

# CSVファイルの絶対パス
# settings.BASE_DIR は manage.py があるプロジェクトのルートディレクトリ
csv_file_path = os.path.join(settings.BASE_DIR, CSV_FILE_NAME)

def run():
    """
    manage.py runscript コマンドで実行される関数
    """
    print(f"CSVデータのインポートを開始。ファイル: {CSV_FILE_NAME}")

    # エラー詳細を記録するためのリスト
    # runscript コマンドはスクリプトの関数 (ここでは run) を実行するので、この関数内で変数を定義
    errors = []
    imported_count = 0
    error_count = 0

    # トランザクション内で実行することで、途中でエラーが発生した場合に全てロールバック
    with transaction.atomic():
        try:

            with open(csv_file_path, mode='r', encoding=CSV_ENCODING) as f:
                reader = csv.reader(f)

                # ヘッダー行をスキップ
                try:
                    header = next(reader)
                    print(f"ヘッダー行をスキップ: {header}")
                except StopIteration:
                    print("警告: CSVファイルが空か、ヘッダー行がありません。")
                    return # ファイルが空の場合は終了

                # 各行を処理
                for row_index, row in enumerate(reader):
                    file_row_num = row_index + 2 # ヘッダー行を1行目、データは2行目から始まるとして +2

                    MIN_COLUMNS = 2 # 必要最低限のカラム数。
                    if not row or len(row) < MIN_COLUMNS:
                        error_count += 1
                        errors.append(f"[行 {file_row_num}] カラム数不足、空行をスキップ: {row}")
                        continue

                    try:
                        # ID (IntegerField, primary_key=True) - 必須
                        passenger_id_data = int(row[0])

                        # name (CharField) - 必須
                        name_data = row[1].strip()
                        if not name_data: # 名前が空白も許容しない場合
                             raise ValueError("Name データが空白です")

                        # sex (BooleanField) - 必須 (1/0 -> True/False)
                        sex_data_str = row[2].strip()
                        if sex_data_str == '1':
                            sex_data = True
                        elif sex_data_str == '0':
                            sex_data = False
                        else:
                            raise ValueError(f"不正な sex データ: '{row[2]}'")

                        # age (IntegerField, null=True) - 欠損値あり (NaN, 空白など)
                        age_data_str = row[3].strip()
                        age_data = None # 初期値を None に設定
                        if age_data_str != '' and age_data_str.lower() != 'nan':
                            try:
                                # float 経由で int に変換
                                age_data = int(float(age_data_str))
                            except ValueError:
                                # 数値変換できず、空白/NaNでもない => エラーとして記録 age_data は None 
                                errors.append(f"[行 {file_row_num}] ageデータ変換エラー: '{row[3]}'")

                        # sibsp (IntegerField, null=True) - 欠損値あり
                        # 数値に変換。変換できない場合は None & 記録。
                        sibsp_data_str = row[4].strip()
                        sibsp_data = None # 初期値を None に設定
                        if sibsp_data_str != '': # 空白でなければ変換を試みる
                            try:
                                sibsp_data = int(sibsp_data_str)
                            except ValueError:
                                errors.append(f"[行 {file_row_num}] sibspデータ変換エラー: '{row[4]}'")
                                # sibsp_data は初期値の None のまま

                        # parch (IntegerField, null=True) - 欠損値あり
                        # 数値に変換。変換できない場合は None & 記録。
                        parch_data_str = row[5].strip()
                        parch_data = None # 初期値を None に設定
                        if parch_data_str != '': # 空白でなければ変換を試みる
                            try:
                                parch_data = int(parch_data_str)
                            except ValueError:
                                errors.append(f"[行 {file_row_num}] parchデータ変換エラー: '{row[5]}'")
                                # parch_data は初期値の None のまま

                        # pclass (IntegerField, null=True) - 欠損値あり
                        # 数値に変換。変換できない場合は None & 記録。
                        pclass_data_str = row[6].strip()
                        pclass_data = None # 初期値を None に設定
                        if pclass_data_str != '': # 空白でなければ変換を試みる
                            try:
                                pclass_data = int(pclass_data_str)
                            except ValueError:
                                errors.append(f"[行 {file_row_num}] pclassデータ変換エラー: '{row[6]}'")
                                # pclass_data は初期値の None のまま

                        # cabin_symbol (CharField, max_length=1, null=True, blank=True)
                        # 空文字列('')の場合は None にする。それ以外のデータはそのまま使用。
                        cabin_symbol_data = row[7].strip() or None

                        # embarked (CharField, max_length=1, null=True, blank=True)
                        # 空文字列('')の場合は None にする。
                        embarked_data = row[8].strip() or None

                        # home.dest (CharField, max_length=255, null=True, blank=True)
                        # 空文字列('')の場合は None にする。
                        home_dest_data = row[9].strip() or None

                        # survived (BooleanField) - 必須 (1/0 -> True/False)
                        # モデルが null=False なので、'1', '0' 以外はエラー。
                        survived_data_str = row[10].strip()
                        if survived_data_str == '1':
                            survived_data = True
                        elif survived_data_str == '0':
                            survived_data = False
                        else:
                            raise ValueError(f"不正または欠損した survived データ: '{row[10]}'")

                        # --- データ変換終わり ---

                        # Passenger インスタンスを作成または更新して保存
                        # ID (primary_key) を使って既存レコードを検索し、存在すれば更新、なければ新規作成
                        passenger, created = Passenger.objects.update_or_create(
                             id=passenger_id_data, # 主キーを使って検索/作成
                             defaults={ # 取得した場合に更新するフィールド、または新規作成時の初期値
                                'name': name_data,
                                'sex': sex_data,
                                'age': age_data,
                                'sibsp': sibsp_data,
                                'parch': parch_data,
                                'pclass': pclass_data,
                                'cabin_symbol': cabin_symbol_data,
                                'embarked': embarked_data,
                                'home_dest': home_dest_data,
                                'survived': survived_data,
                             }
                        )

                        # 成功した場合のみカウント
                        imported_count += 1

                        # 進捗表示
                        if imported_count % 100 == 0:
                            print(f"{imported_count} 件インポートしました...")

                    except Exception as e:
                        # 行全体の処理中にエラーが発生した場合 (上記の raise ValueError やその他の例外)
                        error_count += 1
                        # エラー詳細リストに記録
                        errors.append(f"[行 {file_row_num}] 行処理失敗 (元の行ID: {row[0] if len(row)>0 else '不明'}): {row} - {e}")
                        # このエラーは捕捉されたので、次の行の処理

        except FileNotFoundError:
            print(f"エラー: ファイルが見つかりません: {csv_file_path}")

        except Exception as e:
             # ファイルを開く前やトランザクション中に、上記以外の予期せぬエラーが発生した場合
             print(f"ファイル読み込み中またはトランザクション中に予期せぬエラー: {e}")
             # この例外では、ロールバックされる

    # インポート処理結果
    print("\n--- インポート結果 ---")
    print(f"インポート試行件数 (成功+失敗): {imported_count + error_count}")
    print(f"成功（新規作成または更新）: {imported_count} 件")
    print(f"処理エラー: {error_count} 件")

    if errors:
        print("\n--- エラー詳細 ---")
        for err in errors:
            print(err)

    print("インポート処理が終了しました。")


# runscript コマンドは、このファイルの run() 関数を探して実行。
# ファイル直下には run() 関数の定義だけを置くのが runscript の慣習とのこと。