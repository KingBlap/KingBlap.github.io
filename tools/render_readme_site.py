#!/usr/bin/env python3
"""Render the repository README as the GitHub Pages landing page."""
import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def inline_markdown(text):
    value = html.escape(text, quote=True)
    value = re.sub(r"`([^`]+)`", r"<code>\1</code>", value)
    value = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)
    value = re.sub(
        r"\[([^\]]+)\]\(([^)]+)\)",
        lambda match: '<a href="{}">{}</a>'.format(
            html.escape(match.group(2), quote=True), match.group(1)
        ),
        value,
    )
    return value


def table_cells(line):
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def render_markdown(source):
    lines = source.splitlines()
    output = []
    index = 0

    while index < len(lines):
        line = lines[index]
        if not line.strip():
            index += 1
            continue

        if line.startswith("    ") or line.startswith("\t"):
            code = []
            while index < len(lines) and (lines[index].startswith("    ") or lines[index].startswith("\t")):
                code.append(lines[index][4:] if lines[index].startswith("    ") else lines[index][1:])
                index += 1
            output.append("<pre><code>{}</code></pre>".format(html.escape("\n".join(code))))
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", line)
        if heading:
            level, text = len(heading.group(1)), heading.group(2).strip()
            slug = re.sub(r"\s+", "-", re.sub(r"[^a-z0-9 -]", "", text.lower())).strip("-")
            output.append('<h{0} id="{1}">{2}</h{0}>'.format(level, slug, inline_markdown(text)))
            index += 1
            continue

        if (
            line.strip().startswith("|")
            and index + 1 < len(lines)
            and re.match(r"^\s*\|?\s*:?-{3,}", lines[index + 1])
        ):
            headers = "".join("<th>{}</th>".format(inline_markdown(cell)) for cell in table_cells(line))
            output.append('<div class="table-scroll"><table><thead><tr>{}</tr></thead><tbody>'.format(headers))
            index += 2
            while index < len(lines) and lines[index].strip().startswith("|"):
                cells = "".join("<td>{}</td>".format(inline_markdown(cell)) for cell in table_cells(lines[index]))
                output.append("<tr>{}</tr>".format(cells))
                index += 1
            output.append("</tbody></table></div>")
            continue

        list_match = re.match(r"^\s*(?:[-*+]\s+|\d+\.\s+)", line)
        if list_match:
            ordered = bool(re.match(r"^\s*\d+\.\s+", line))
            tag = "ol" if ordered else "ul"
            pattern = r"^\s*\d+\.\s+(.*)$" if ordered else r"^\s*[-*+]\s+(.*)$"
            output.append("<{}>".format(tag))
            while index < len(lines):
                item = re.match(pattern, lines[index])
                if not item:
                    break
                output.append("<li>{}</li>".format(inline_markdown(item.group(1).strip())))
                index += 1
            output.append("</{}>".format(tag))
            continue

        paragraph = []
        while index < len(lines) and lines[index].strip():
            candidate = lines[index]
            if (
                re.match(r"^(#{1,6})\s+", candidate)
                or re.match(r"^\s*(?:[-*+]\s+|\d+\.\s+)", candidate)
                or candidate.startswith("    ")
                or candidate.startswith("\t")
                or (
                    candidate.strip().startswith("|")
                    and index + 1 < len(lines)
                    and re.match(r"^\s*\|?\s*:?-{3,}", lines[index + 1])
                )
            ):
                break
            paragraph.append(candidate.strip())
            index += 1
        if paragraph:
            output.append("<p>{}</p>".format(inline_markdown(" ".join(paragraph))))
        else:
            index += 1

    return "\n".join(output)


def main():
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    body = render_markdown(readme)
    page = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="KingBlap Kodi Repository setup instructions, wizard build details, downloads, release history, and package inventory.">
  <title>KingBlap Kodi Repository</title>
  <style>
    :root { color-scheme: dark; --accent:#49d9e6; --line:#2d4761; }
    * { box-sizing:border-box; }
    body { margin:0; background:radial-gradient(circle at 82% 8%,#164c67 0,transparent 32%),linear-gradient(135deg,#081326,#0c2138); color:#f3f7ff; font:16px/1.65 system-ui,Segoe UI,Arial,sans-serif; }
    main { max-width:1000px; margin:0 auto; padding:36px 24px 72px; }
    .kodi-links { display:flex; flex-wrap:wrap; gap:10px; margin:0 0 28px; padding:18px; border:1px solid var(--line); border-radius:16px; background:#0d1b2ee8; }
    .kodi-links a { display:inline-block; padding:9px 13px; border-radius:9px; background:#13273e; color:#a5eff4; font-weight:700; text-decoration:none; }
    .kodi-links a:first-child { background:var(--accent); color:#061522; }
    article { padding:32px; border:1px solid var(--line); border-radius:20px; background:#0d1b2ee8; box-shadow:0 20px 60px #02091666; overflow-wrap:anywhere; }
    h1,h2,h3,h4 { line-height:1.2; margin:1.45em 0 .55em; }
    h1 { font-size:clamp(2.2rem,6vw,3.6rem); margin-top:0; }
    h2 { padding-bottom:.35em; border-bottom:1px solid #29415a; }
    h3 { color:#d8f8fa; }
    p,li { color:#e0e9f5; }
    li { padding:.22em 0; }
    a { color:#8cecf0; }
    code { color:#a5eff4; background:#13273e; padding:.12em .35em; border-radius:5px; }
    pre { overflow:auto; padding:16px; border:1px solid var(--line); border-radius:10px; background:#081326; }
    pre code { padding:0; background:transparent; }
    .table-scroll { overflow-x:auto; margin:20px 0; }
    table { border-collapse:collapse; width:100%; min-width:540px; }
    th,td { padding:9px 12px; border:1px solid var(--line); text-align:left; vertical-align:top; }
    th { background:#13273e; color:#d8f8fa; }
    tbody tr:nth-child(even) { background:#102038; }
    @media (max-width:640px) { main { padding:16px 12px 40px; } article { padding:20px 16px; } .kodi-links { padding:12px; } }
  </style>
</head>
<body>
  <main>
    <nav class="kodi-links" aria-label="Kodi links">
      <a href="/repository.kingblap-1.0.0.zip">repository.kingblap-1.0.0.zip</a>
      <a href="/repo/zips/addons.xml">Kodi add-on catalog</a>
      <a href="/builds.txt">Wizard build list</a>
      <a href="/README.md">README</a>
    </nav>
    <article>
{body}
    </article>
  </main>
</body>
</html>
""".replace("{body}", body)
    (ROOT / "index.html").write_text(page, encoding="utf-8", newline="\n")
    print("Rendered README.md to index.html with Kodi install links preserved.")


if __name__ == "__main__":
    main()
