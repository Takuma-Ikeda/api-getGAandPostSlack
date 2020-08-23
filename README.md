# 手動で実行

```sh
python get_ga_and_post_slack.py
```

# AWS Lambda に配置するとき

## pipenv を使っているとき

- 参考
    - https://qrunch.net/@meteoride/entries/Cfm8BOm0AiZI68Yx
    - https://github.com/pypa/pipenv/issues/2705

1. `Pipfile.lock` から `requirement.txt` を作成する  
1. `pip install` で `dist` にパッケージを出力する
1. `dist` 配下に `index.py` と `key_file.json` をコピーする 
1. `dist` の中身を `lambda_function.zip` としてプロジェクト直下に生成する

```sh
rm -rf dist
mkdir dist
cp -r index.py dist
cp -r key_file.json dist
pipenv lock -r > requirements.txt  
pip install -r requirements.txt -t dist  
cd dist
zip -r ../lambda_function.zip *  
cd ..
rm requirements.txt  
```
