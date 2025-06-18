from django.db import models

# Create your models here.
from django.db import models

class Passenger(models.Model):
    # ID: 数値, プライマリキー（今回のインポートデータのようにuniqueなID列がある場合の例。
    # そうでない場合は、Djangoが自動で id という連番の主キーを作ってくれるので、この行は不要。
    id = models.IntegerField(primary_key=True)

    # name: テキスト
    name = models.CharField(max_length=255) # max_length は必須

    # sex: 1か0の数値
    sex = models.BooleanField(
        # 1/0 を True/False にマッピングするのはインポートスクリプト側
    )

    # age: 年齢、数値　欠損値が多いデータなので null=True
    age = models.IntegerField(
        null=True, # 欠損値(NaN)がある場合に対応
        blank=True, 
    )

    # sibsp: 同乗している兄弟/配偶者の数　整数。欠損値がある場合対応
    sibsp = models.IntegerField(
        null=True,
        blank=True,
    )

    # parch: 同乗している親/子の数　整数。欠損値がある場合対応
    parch = models.IntegerField(
        null=True,
        blank=True,
    )

    # pclass: 客室クラス 整数。欠損値がある場合対応
    pclass = models.IntegerField(
        null=True,
        blank=True,
    )

    # cabin_symbol: 船室番号の先頭文字。1文字の文字列。欠損値が多いデータなので null=True, blank=True
    cabin_symbol = models.CharField(
        max_length=1,
        null=True,
        blank=True,
    )

    # embarked: アルファベット１文字の記号 (乗船港 S, C, Q)　欠損値がある場合対応
    embarked = models.CharField(
        max_length=1,
        null=True,
        blank=True,
    )

    # home.dest: 100文字程度のテキスト (出身地/目的地)
    home_dest = models.CharField(
        max_length=255, 
        null=True,
        blank=True,
    )

    # survived: 1か0の数値 (生存情報)
    survived = models.BooleanField(
        # 1/0 を True/False にマッピングするのはインポートスクリプト側
    )