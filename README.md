# api-getGAandPostSlack

- Google Analytics からメトリクスを取得して Slack チャンネルに投稿します
- AWS Lambda に zip ファイルアップロードすることで利用可能です
- `index.lambda_handler` をハンドラ設定してください
- `.env` に環境変数を設定してください
- `key_file.json` に GCP の情報を設定してください。下記フォーマットが想定されます

```json
{
  "type": "*****",
  "project_id": "*****",
  "private_key_id": "*****",
  "private_key": "*****",
  "client_email": "*****",
  "client_id": "*****",
  "auth_uri": "*****",
  "token_uri": "*****",
  "auth_provider_x509_cert_url": "*****",
  "client_x509_cert_url": "*****"
}

```

- 解説記事を作成しました
    - [【Lambda】Google Analytics集計を自動化する](https://suwaru.tokyo/%e3%80%90lambda%e3%80%91google-analytics%e9%9b%86%e8%a8%88%e3%82%92%e8%87%aa%e5%8b%95%e5%8c%96%e3%81%99%e3%82%8b/)

## 開発環境

- Python 3.8.5

```sh
pipenv shell
```

## 手動実行

```sh
python index.py
```

## デプロイ方法
### pipenv を利用した場合

下記 zsh スクリプト一発で `lambda_function.zip` を生成します

```sh
./deploy_pipenv.sh
```

- シェルスクリプトの中身は下記を参考にしました
    - https://qrunch.net/@meteoride/entries/Cfm8BOm0AiZI68Yx
    - https://github.com/pypa/pipenv/issues/2705

### pip を利用した場合

下記 zsh スクリプト一発で `lambda_function.zip` を生成します

```sh
./deploy_pip.sh
```
