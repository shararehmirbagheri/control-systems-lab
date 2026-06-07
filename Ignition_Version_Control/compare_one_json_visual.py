from pathlib import Path
import json
import html

EAM_FOLDER = "EAM_UDT_Definitions_20260605"
IAD_FOLDER = "IAD2_DC2_UDT_Definitions_20260605"

FILE_NAME = "AAON_RN_AB_v3.json"   # change this

OUTPUT_FILE = "smarter_json_difference.html"


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def compare(eam, iad, path="root"):
    diffs = {}

    if isinstance(eam, dict) and isinstance(iad, dict):
        keys = set(eam.keys()) | set(iad.keys())

        for key in keys:
            new_path = f"{path}.{key}"

            if key not in eam:
                diffs[new_path] = "iad_only"
            elif key not in iad:
                diffs[new_path] = "eam_only"
            else:
                diffs.update(compare(eam[key], iad[key], new_path))

    elif isinstance(eam, list) and isinstance(iad, list):
        max_len = max(len(eam), len(iad))

        for i in range(max_len):
            new_path = f"{path}[{i}]"

            if i >= len(eam):
                diffs[new_path] = "iad_only"
            elif i >= len(iad):
                diffs[new_path] = "eam_only"
            else:
                diffs.update(compare(eam[i], iad[i], new_path))

    else:
        if eam != iad:
            diffs[path] = "changed"

    return diffs


def render_json(data, diffs, source, path="root", indent=0):
    lines = []
    space = " " * indent

    if isinstance(data, dict):
        lines.append(space + "{")

        items = list(data.items())

        for index, (key, value) in enumerate(items):
            child_path = f"{path}.{key}"
            comma = "," if index < len(items) - 1 else ""

            rendered_value = render_json(value, diffs, source, child_path, indent + 4)

            key_text = html.escape(json.dumps(key))

            highlight = ""
            if child_path in diffs:
                diff_type = diffs[child_path]
                if diff_type == "changed":
                    highlight = "changed"
                elif diff_type == "eam_only" and source == "EAM":
                    highlight = "eam_only"
                elif diff_type == "iad_only" and source == "IAD2":
                    highlight = "iad_only"

            if len(rendered_value) == 1:
                line = " " * (indent + 4) + f"{key_text}: {rendered_value[0].lstrip()}{comma}"
                if highlight:
                    line = f'<span class="{highlight}">{line}</span>'
                lines.append(line)
            else:
                first_line = " " * (indent + 4) + f"{key_text}: {rendered_value[0].lstrip()}"
                if highlight:
                    first_line = f'<span class="{highlight}">{first_line}</span>'
                lines.append(first_line)
                lines.extend(rendered_value[1:-1])
                lines.append(rendered_value[-1] + comma)

        lines.append(space + "}")

    elif isinstance(data, list):
        lines.append(space + "[")

        for index, value in enumerate(data):
            child_path = f"{path}[{index}]"
            comma = "," if index < len(data) - 1 else ""

            rendered_value = render_json(value, diffs, source, child_path, indent + 4)

            highlight = ""
            if child_path in diffs:
                diff_type = diffs[child_path]
                if diff_type == "changed":
                    highlight = "changed"
                elif diff_type == "eam_only" and source == "EAM":
                    highlight = "eam_only"
                elif diff_type == "iad_only" and source == "IAD2":
                    highlight = "iad_only"

            if len(rendered_value) == 1:
                line = rendered_value[0] + comma
                if highlight:
                    line = f'<span class="{highlight}">{line}</span>'
                lines.append(line)
            else:
                if highlight:
                    rendered_value[0] = f'<span class="{highlight}">{rendered_value[0]}</span>'
                lines.extend(rendered_value[:-1])
                lines.append(rendered_value[-1] + comma)

        lines.append(space + "]")

    else:
        value_text = html.escape(json.dumps(data))
        line = space + value_text

        if path in diffs:
            if diffs[path] == "changed":
                line = f'<span class="changed">{line}</span>'
            elif diffs[path] == "eam_only" and source == "EAM":
                line = f'<span class="eam_only">{line}</span>'
            elif diffs[path] == "iad_only" and source == "IAD2":
                line = f'<span class="iad_only">{line}</span>'

        lines.append(line)

    return lines


base = Path(__file__).parent

eam_file = base / EAM_FOLDER / FILE_NAME
iad_file = base / IAD_FOLDER / FILE_NAME

eam_json = load_json(eam_file)
iad_json = load_json(iad_file)

diffs = compare(eam_json, iad_json)

eam_rendered = "\n".join(render_json(eam_json, diffs, "EAM"))
iad_rendered = "\n".join(render_json(iad_json, diffs, "IAD2"))

html_output = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Smart JSON Difference</title>
<style>
body {{
    font-family: Arial, sans-serif;
}}
.container {{
    display: flex;
    gap: 20px;
}}
.panel {{
    width: 50%;
}}
pre {{
    background: #f8f8f8;
    padding: 15px;
    overflow-x: auto;
    font-family: Consolas, monospace;
    font-size: 13px;
}}
.changed {{
    background-color: #fff3a3;
    color: #000000;
}}
.eam_only {{
    background-color: #ffd6d6;
    color: #800000;
}}
.iad_only {{
    background-color: #d6ffd6;
    color: #006000;
}}
</style>
</head>
<body>

<h2>Smart JSON Difference Report</h2>
<p><b>File:</b> {FILE_NAME}</p>
<p><span class="changed">Yellow</span> = value changed</p>
<p><span class="eam_only">Red</span> = exists only in EAM</p>
<p><span class="iad_only">Green</span> = exists only in IAD2</p>

<div class="container">
    <div class="panel">
        <h3>EAM</h3>
        <pre>{eam_rendered}</pre>
    </div>

    <div class="panel">
        <h3>IAD2</h3>
        <pre>{iad_rendered}</pre>
    </div>
</div>

</body>
</html>
"""

output_path = base / OUTPUT_FILE
output_path.write_text(html_output, encoding="utf-8")

print("Smart JSON difference report created:")
print(output_path)
print(f"Number of actual different fields: {len(diffs)}")