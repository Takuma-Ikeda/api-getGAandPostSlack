# api-getGAandPostSlack

- Google Analytics からメトリクスを取得して Slack チャンネルに投稿します
- AWS Lambda に zip ファイルアップロードすることで利用可能です
- `index.lambda_handler` をハンドラ設定してください
- `.env` に環境変数を設定してください
- 解説記事
    - [【Lambda】Google Analytics集計を自動化する](https://suwaru.tokyo/%e3%80%90lambda%e3%80%91google-analytics%e9%9b%86%e8%a8%88%e3%82%92%e8%87%aa%e5%8b%95%e5%8c%96%e3%81%99%e3%82%8b/)

## 開発環境

- Python 3.8.5

'''sh
pipenv shell
'''

## 手動実行

```sh
python index.py
```

## デプロイ方法
### pipenv を利用した場合

- 参考
    - https://qrunch.net/@meteoride/entries/Cfm8BOm0AiZI68Yx
    - https://github.com/pypa/pipenv/issues/2705

1. `Pipfile.lock` から `requirement.txt` を作成する
1. `pip install` で `dist` にパッケージを出力する
1. `dist` 配下に `index.py` と `ga.py` と `key_file.json` と `.env` をコピーする
1. `dist` の中身を `lambda_function.zip` としてプロジェクト直下に生成する

下記 zsh スクリプト一発で `lambda_function.zip` を生成します

```sh
./deploy_pipenv.sh
```

### pip を利用した場合

下記 zsh スクリプト一発で `lambda_function.zip` を生成します

```sh
./deploy_pip.sh
```
