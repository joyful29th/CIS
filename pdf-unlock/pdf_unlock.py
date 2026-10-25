#!/usr/bin/env python3
"""PDFの制限（印刷・コピー・編集の禁止など）を外して、制限なしのPDFとして保存するツール。

- 開くだけならパスワード不要のPDF（所有者パスワードによる制限のみ）: そのまま解除できます。
- 開くときにパスワードが必要なPDF: パスワードを知っている場合のみ -p で指定してください。
  パスワードの総当たり（解読）は行いません。

使い方:
  python pdf_unlock.py 入力.pdf                  -> 入力_unlocked.pdf を作成
  python pdf_unlock.py 入力.pdf -o 出力.pdf
  python pdf_unlock.py 入力.pdf -p パスワード
  python pdf_unlock.py フォルダ/                 -> フォルダ内の全PDFを処理

自分が所有する、または編集する権利のあるPDFにのみ使用してください。
"""
import argparse
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.errors import PdfReadError


def unlock(src: Path, dst: Path, password: str | None) -> str:
    """成功時は結果メッセージを返す。失敗時は例外。"""
    reader = PdfReader(str(src))
    was_encrypted = reader.is_encrypted
    if was_encrypted:
        # 空パスワードで開ければ所有者制限のみ。開けなければ指定パスワードを使う。
        if reader.decrypt("") == 0:
            if not password:
                raise PermissionError("開くのにパスワードが必要です（-p で指定してください）")
            if reader.decrypt(password) == 0:
                raise PermissionError("パスワードが違います")
    writer = PdfWriter(clone_from=reader)  # 暗号化せずに書き出す＝制限なし
    with open(dst, "wb") as f:
        writer.write(f)
    return "制限を解除しました" if was_encrypted else "制限はありませんでした（そのままコピー）"


def main() -> int:
    ap = argparse.ArgumentParser(description="PDFの制限（シークレット機能）を解除します")
    ap.add_argument("input", type=Path, help="PDFファイル、またはPDFの入ったフォルダ")
    ap.add_argument("-o", "--output", type=Path, help="出力先（ファイル入力時のみ）")
    ap.add_argument("-p", "--password", help="開くためのパスワード（知っている場合のみ）")
    args = ap.parse_args()

    if args.input.is_dir():
        if args.output:
            ap.error("フォルダ入力では -o は使えません")
        files = sorted(p for p in args.input.glob("*.pdf") if not p.stem.endswith("_unlocked"))
    elif args.input.is_file():
        files = [args.input]
    else:
        print(f"見つかりません: {args.input}", file=sys.stderr)
        return 2

    failed = 0
    for src in files:
        dst = args.output if args.output else src.with_name(src.stem + "_unlocked.pdf")
        if dst.resolve() == src.resolve():
            print(f"NG  {src}: 入力と同じ場所には保存できません", file=sys.stderr)
            failed += 1
            continue
        try:
            print(f"OK  {src} -> {dst}  {unlock(src, dst, args.password)}")
        except (PermissionError, PdfReadError, OSError, ValueError) as e:
            dst.unlink(missing_ok=True)
            print(f"NG  {src}: {e}", file=sys.stderr)
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
