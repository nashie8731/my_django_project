# タイタニック号乗客者検索

このプロジェクトは、PythonのWebフレームワーク **Django** を使用してタイタニック号の乗客データを検索するアプリケーションです。Python学習用の教材として作成しました。開発はLinux (Ubuntu)、PowerShell、VS Codeを組み合わせたSSH接続によるフローを想定しています。

＊Data obtained from http://hbiostat.org/data courtesy of the Vanderbilt University Department of Biostatistics.（[参考記事](https://atmarkit.itmedia.co.jp/ait/articles/2007/02/news016.html)）

-----

## 1\. プロジェクトディレクトリの作成

`my_django_project` など任意の名前でプロジェクトディレクトリを作成します。

```bash
mkdir my_django_project
```

-----

## 2\. 仮想環境 (venv) の作成と有効化

手順1で作成したディレクトリの直下で仮想環境を作成し、仮想環境を有効化 (activate) します。

```bash
cd my_django_project
python3 -m venv venv
source venv/bin/activate
```

-----

## 3\. Django のインストール

ターミナルのプロンプトの先頭に (venv) と表示されることを確認し、Djangoをインストールします。

```bash
pip install Django
```

-----

## 4\. Djangoプロジェクトの作成（＆動作確認）

基盤となるプロジェクト構造と設定ファイルを生成します。プロジェクトのルートディレクトリで実行してください。

```bash
django-admin startproject config .
```
> [!NOTE]
> プロジェクト名は `config` としていますが、他の名前でも構いません。ただし、`myapp` は名前が衝突する可能性があるため避けることを推奨します。末尾の「`.`」を忘れないでください。成功すると `config/` (プロジェクト設定用のディレクトリ) と `manage.py` が作成されます。

プロジェクトが正しく作成されたか、起動してみましょう。

```bash
python3 manage.py runserver
```

上記のコマンドを実行後、ブラウザで `http://127.0.0.1:8000/` にアクセスし、Djangoのロケット画像が表示されればOKです。

-----

## 5\. アプリケーションの作成（検索アプリ）

`manage.py` があるディレクトリで実行します。（アプリ名を `titanic_search_app` とした場合）

```bash
python3 manage.py startapp titanic_search_app
```

成功すると `titanic_search_app/` ディレクトリと、その中に `models.py`, `views.py` などのファイルが作成されます。

**ディレクトリ参考**
```
my_django_project/            # プロジェクト全体のトップレベルディレクトリ
+-- venv/                     # 仮想環境
+-- config/                   # Djangoプロジェクトの設定ファイルなどが格納されるディレクトリ (configという名前で作成した場合)
|   +-- __init__.py
|   +-- asgi.py
|   +-- settings.py           # 設定ファイル
|   +-- urls.py               # プロジェクト全体のURL設定
|   +-- wsgi.py
+-- titanic_search_app/       # アプリケーションのディレクトリ (タイタニック乗客検索)
|   +-- migrations/
|   +-- static/
|   +-- __init__.py
|   +-- admin.py
|   +-- apps.py
|   +-- models.py             # モデル定義
|   +-- tests.py
|   +-- views.py              # ビュー定義
+-- manage.py                 # Django管理コマンド実行用ファイル
+-- requirements.txt          # プロジェクトの依存パッケージをリストしたファイル (pip freeze > requirements.txt で生成)
+-- .gitignore                # Gitで管理しないファイルを指定するファイル (venv/ などを含める)
```

アプリケーションのディレクトリが生成されたかを確認し、問題なければ、`config/settings.py` の `INSTALLED\_APPS` にアプリ名を追加します。

**config/settings.py**
```
INSTALLED_APPS = [
    # ... 他のアプリ ...
    'titanic_search_app', # 検索アプリ名 ★これを追加★
    'config',             # 4.で作成したプロジェクトアプリ名 ★これを追加★
]
```

-----

## 6\. モデルの定義とデータベースマイグレーション

### (1) モデルの定義
`titanic_search_app/models.py` を編集します。インポートしたいデータ（CSV）に合わせて、フィールドとデータ型をDjangoのモデルフィールドを使って記述してください。（[Codeを参照](titanic_search_app/models.py)）

### (2) マイグレーションファイルの作成
モデルの定義を元にマイグレーションファイルを生成します。

```bash
python3 manage.py makemigrations titanic_search_app
```

### (3) データベースへの適用
生成されたマイグレーションファイルをデータベースに適用し、テーブルを作成します。

```bash
python3 manage.py migrate
```

-----

## 7\. データのインポート

データの投入方法は様々なので、インポートデータの形式に合わせて手法を選択し、スクリプトを作成する必要があります。単純なインポートであれば、`my_django_project` 直下で以下のコマンドにてシェルを立ち上げ、CSVインポート用のPythonコードを入力し実行します。

```bash
python3 manage.py shell
```

インポートが完了したら、`exit()` でシェルを終了します。

インポートの際のスクリプトのコード量が多い場合は、次の 「**django-extensions**（Djangoの機能を拡張してくれるライブラリ）」 を使用する方法がおすすめです。

### (1) django-extensionsで、`manage.py runscript` コマンドを使う準備
venvをアクティベートした状態でインストールします。

```bash
pip install django-extensions
```

`config/settings.py`の`INSTALLED_APPS`に以下を追加します。
```
INSTALLED_APPS = [
    # ... 他のアプリ ...
    'django_extensions', # ★これを追加★
    'titanic_search_app',
    'config', # プロジェクトアプリ名
]
```

### (2) スクリプトディレクトリに、スクリプトファイルを作成して実行

#### ① スクリプトを配置する `scripts` ディレクトリを作成します。<br/>
**`my_django_project/scripts`**
> [!NOTE]
>必ず `scripts` という名前でルートに作成してください。

#### ② CSVファイルを配置します。<br/>
`my_django_project/titanic_search_app/to_csv_titnic.csv` などにアップロードしてください。（[加工済CSV](titanic_search_app/to_csv_titnic.csv)）

#### ③ スクリプトファイルを作成します。
作成したファイルは`my_django_project/scripts/import_titanic_data.py` に配置します。（[インポートスクリプト(import_titanic_data.py)](scripts/import_titanic_data.py)）

準備が整ったら、`my_django_project` 直下で以下のコマンドを実行します。

```bash
python3 manage.py runscript import_titanic_data
```

### (3) データがインポートされたか確認（管理画面）

管理画面にアクセスし、データがインポートされたか確認します。そのため、管理画面の設定（モデル登録とユーザー作成）を行います。
まずは、`titanic_search_app/admin.py` に以下のコードを追加し、モデルを登録します。
```
from django.contrib import admin

# Register your models here.

from .models import Passenger # ★これを追加 ★
admin.site.register(Passenger) # ★これを追加 ★
```

次に、以下のコマンドからスーパーユーザーのアカウントを作成します。

```bash
python3 manage.py createsuperuser
```

  * **ユーザー名**: 任意の名前を入力（例: `admin`）
  * **メールアドレス**: 空欄でもOK
  * **パスワード**: 画面には入力した文字は表示されません。確認のため再入力が必要です。

ユーザーが作成できたら、Djangoを起動させた状態で、`http://127.0.0.1:8000/admin/` にアクセスし、作成したアカウントでログインします。

**サーバー起動のコマンド**
```bash
python3 manage.py runserver
```

ログインしたホーム画面に「Titanic\_Search\_App Passengers」項目ができていて、Passengersのページに各データが存在していればOKです。

-----

## 8\. プログラミング (ビュー、テンプレート、URLルーティング)

### (1) ビュー関数

`titanic_search_app/views.py` を編集します。ユーザーからのリクエストを受け取り、データベースからデータを検索し、テンプレートに渡すためのPython関数を記述します。
（[Codeを参照](titanic_search_app/views.py)）

### (2) static（画像やCSS）ファイルを扱う準備

画像やCSS、JavaScriptなどの外部ファイルを扱う場合も設定が必要になります。
`config/settings.py` に `STATICFILES_DIRS` を追加しましょう。
デフォルトで `STATIC_URL` が設定されているはずなので、その下に以下のコードを追加します。（os モジュールのimportも必要です。）
```bash
import os
STATICFILES_DIRS = (
    [
        os.path.join(BASE_DIR, "static"),
    ]
)
```

次に、画像やCSS、JavaScriptを準備します。`titanic_search_app/static` となるように配置してください。（[画像やCSS、JavaScriptなど(titanic_search_app/static)](https://github.com/nashie8731/my_django/tree/main/titanic_search_app/static)）

```
+-- titanic_search_app/       # アプリケーションのディレクトリ (タイタニック乗客検索)
|   +-- static/
|   |   +-- css/
|   |   +-- img/
|   |   +-- js/
```
> [!NOTE]
> 複数のアプリケーションを作成しデプロイまで行う場合は、`static/` は全アプリケーションで統合されるため、衝突を防ぐためにディレクトリの名前付けには工夫が必要ですが、今回はデバッグサーバーでの表示が目標なので、上記のような形で進めます。

### (3) テンプレートファイル（HTML）

まずはテンプレートを配置するフォルダを作成します。`titanic_search_app/templates`
※必ず `templates` という名前で作成してください。
テンプレートはHTMLで作成し、今回は `search.html` というファイル名で配置します。
このHTMLでビューから渡されたデータを表示します。（[Codeを参照](titanic_search_app/templates/search.html)）

### (4) URLルーティング

`titanic_search_app` に `urls.py` ファイルを作成し、検索ページのURLパスを定義します。プロジェクト全体の `config/urls.py` から、アプリの `urls.py` を参照するように設定します。

**新規に作成 `titanic_search_app/urls.py`**<br/>
アプリ固有のURLパターンを定義し、対応するビューにマッピングします。
```bash
from django.urls import path
from . import views

urlpatterns = [
    path('', views.search_view, name='search'),
]
```

**既存を編集 `config/urls.py`**<br/>
プロジェクトのメインURL設定で、アプリのURL設定をインクルードします。
```bash
from django.contrib import admin
from django.urls import path
from django.urls import path, include # ★これを追加 ★

urlpatterns = [
    path('admin/', admin.site.urls),
    path('titanic/', include('titanic_search_app.urls')), # ★これを追加 ★
]
```

-----

## 9\. 開発環境での表示 (デバッグサーバーでの表示)

プロジェクトのルートディレクトリ`my_django_project`で以下を実行し、サーバーを起動します。

```bash
python3 manage.py runserver
```

Webブラウザを開き、`http://127.0.0.1:8000/titanic/` にアクセスし、アプリの動作を確認してください。
