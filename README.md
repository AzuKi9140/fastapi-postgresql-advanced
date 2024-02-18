# FastAPI + PostgreSQL 初学者向けプロジェクト

## 概要
これは、FastAPIとPostgreSQLを統合した初学者向けのスタータープロジェクトです。FastAPI, PostgreSQL, および他のいくつかの技術を使用して効果的にバックエンドシステムを構築するためのガイドとして設計されています。

## 特徴
- FastAPIを使用したAPI構築
- リレーショナルデータベースとしてのPostgreSQL
- SQLAlchemyを使用したORM
- データベースマイグレーション用のAlembic
- コンテナ化のためのDocker
- パッケージ管理のためのPipenv
- ASGIサーバーとしてのUvicorn
- データベース管理ツールとしてのDBeaver

## 前提条件
- オペレーティングシステム: 例: Windows, macOS, Linux
- テキストエディタまたはIDE: 例: VSCode, PyCharm
- ウェブブラウザ: 例: Chrome, Firefox
- コマンドラインツール: Terminal (macOS, Linux), コマンドプロンプトまたはPowerShell (Windows)
- Python (バージョン3.7以上)
- Docker
- Pipenv

## セットアップとインストール

### リポジトリのクローン
```sh
git clone https://github.com/AzuKi9140/fastapi-postgresql-starter.git
cd https://github.com/AzuKi9140/fastapi-postgresql-starter.git
```

### 依存関係のインストール
```sh
pipenv install
```

### PostgreSQLのDockerコンテナの開始
```sh
docker-compose up -d
```

### Alembicマイグレーションの実行
```sh
pipenv run alembic upgrade head
```

### FastAPIアプリケーションの開始
```sh
pipenv run start
```

## 使い方
ウェブブラウザで`http://127.0.0.1:8000/docs`に移動して、APIと対話するためのSwagger UIにアクセスしてください。

## 著者
Mikami Kazuki

## 免責事項
これは初学者向けのプロジェクトで、私の最初の記事です。すべての情報が正しいとは保証できませんので、開発する際には各公式ドキュメントも参照してください。わからないことがあれば、随時検索して確認することをお勧めします。
