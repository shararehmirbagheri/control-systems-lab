provider = "default"
file_path = "C:/temp/udt_usage_report1.csv"

def _get_prop(obj, prop, default=None):
    try:
        if hasattr(obj, prop):
            return getattr(obj, prop)
        return obj.get(prop, default)
    except:
        try:
            return obj[prop]
        except:
            return default

def _type_name_from_fullpath(full_path, provider_name):
    # full_path example: [default]_types_/Folder/MyUdt
    s = str(full_path)
    prefix = "[%s]_types_/" % provider_name
    if s.startswith(prefix):
        return s[len(prefix):]   # keep folders: Folder/MyUdt
    return s

# 1) ALL UDT type definitions (recursive)
udt_defs = system.tag.browse(
    "[%s]_types_" % provider,
    {"recursive": True, "tagType": "UdtType"}
).getResults()

all_udt_types = set()
for r in udt_defs:
    full_path = _get_prop(r, "fullPath") or _get_prop(r, "path")
    if full_path:
        all_udt_types.add(_type_name_from_fullpath(full_path, provider))
    else:
        name = _get_prop(r, "name")
        if name:
            all_udt_types.add(str(name))

# 2) USED UDT types from instances (keep folders if present)
instances = system.tag.browse(
    "[%s]" % provider,
    {"recursive": True, "tagType": "UdtInstance"}
).getResults()

used_udt_types = set()
for r in instances:
    type_id = _get_prop(r, "typeId")
    if type_id:
        # typeId is usually like: Folder/MyUdt (or just MyUdt)
        used_udt_types.add(str(type_id))

# Debug counts
print("UDT types found:", len(all_udt_types))
print("UDT types used :", len(used_udt_types))

# 3) CSV
lines = ['"UDT_Type","Usage"']
for udt_type in sorted(all_udt_types):
    usage = "USED" if udt_type in used_udt_types else "NOT USED"
    safe = str(udt_type).replace('"', '""')
    lines.append('"%s","%s"' % (safe, usage))

system.file.writeFile(file_path, "\n".join(lines), False)
print("CSV file created at:", file_path)