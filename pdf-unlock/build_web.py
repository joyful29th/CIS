#!/usr/bin/env python3
"""web/template.html に qpdf(WASM) を埋め込み、単体で動く pdf-unlock.html を作る（開発者用）。

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
html = (here / "web/template.html").read_text(encoding="utf-8")
html = html.replace("/*__QPDF_JS__*/", js, 1).replace("/*__QPDF_WASM__*/", b64, 1)
(here / "pdf-unlock.html").write_text(html, encoding="utf-8")
print("wrote", here / "pdf-unlock.html", f"{len(html)/1e6:.1f}MB")
