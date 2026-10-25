#!/usr/bin/env python3
"""web/template.html に qpdf(WASM) を埋め込み、単体で動く pdf-unlock.html を作る（開発者用）。
--artifact <出力先> を付けると、Claude の Artifact 用（head なしの本文断片）も書き出す。

  npm install @jspawn/qpdf-wasm   # 別の作業フォルダで
  python build_web.py <node_modules/@jspawn/qpdf-wasm のパス>
"""
import base64
import sys
from pathlib import Path

lib = Path(sys.argv[1])
here = Path(__file__).parent
js = (lib / "qpdf.js").read_text(encoding="utf-8")
assert "</script" not in js.lower()
b64 = base64.b64encode((lib / "qpdf.wasm").read_bytes()).decode()
body = (here / "web/template.html").read_text(encoding="utf-8")
body = body.replace("/*__QPDF_JS__*/", js, 1).replace("/*__QPDF_WASM__*/", b64, 1)
head = (
    '<!doctype html>\n<html lang="ja"><head><meta charset="utf-8">\n'
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">\n'
    # 通信を禁止する（PDFやパスワードが外に出ないことを保証）
    '<meta http-equiv="Content-Security-Policy" content="default-src \'none\'; script-src \'unsafe-inline\' '
    '\'wasm-unsafe-eval\'; style-src \'unsafe-inline\'; img-src data: blob:">\n'
    "<style>body{margin:0}</style>\n</head><body>\n"
)
html = head + body + "\n</body></html>\n"
(here / "pdf-unlock.html").write_text(html, encoding="utf-8")
if len(sys.argv) > 3 and sys.argv[2] == "--artifact":
    Path(sys.argv[3]).write_text(body, encoding="utf-8")
print("wrote", here / "pdf-unlock.html", f"{len(html)/1e6:.1f}MB")
