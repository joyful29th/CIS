# PDFロック解除

パスワードを知っているPDF（および印刷・コピー・編集の制限つきPDF）を、パスワードなしのPDFに変換するツールです。
自分が編集する権利のあるPDFにのみ使ってください。パスワードの総当たり（解読）は行いません。

## 1. pdf-unlock.html（スタンドアローン・おすすめ）
インストール不要。`pdf-unlock.html` を1ファイルだけ端末に保存し、ブラウザで開いてPDFをドロップします。
- ネット接続不要（PDF解除エンジン qpdf を WebAssembly として内蔵）。
- PDFもパスワードも外部へ送信されません（CSPで通信を禁止）。
- パスワードが必要なPDFは、欄に入力して「もう一度試す」。結果は `○○_unlocked.pdf` として保存。

## 2. pdf_unlock.py（コマンドライン版）
`pip install -r requirements.txt` のあと `python pdf_unlock.py ファイル.pdf`。詳細は `-h`。

## 開発者向け
`pdf-unlock.html` は `web/template.html` と qpdf-wasm（Apache-2.0）から `build_web.py` で生成します。
