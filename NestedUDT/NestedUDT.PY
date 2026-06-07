
provider = "default"
file_path = "C:/temp/Nested_ASH2_DC1_udt_usage_report.csv"

import re

try:
    system
except NameError:
    raise RuntimeError("This script must run in Ignition. `system` is not available.")

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
        return s[len(prefix):]   # returns Folder/MyUdt
    return s

def _normalize_typeid(tid):
    s = str(tid).strip()
    try:
        s = re.sub(r'^\[.*?\]_types_/?', '', s)
        s = re.sub(r'^\[.*?\]/?', '', s)
        s = s.lstrip('/')
    except:
        pass
    return s

def _collect_nested_type_ids(obj, nested_set):
    """
    Recursively scan configuration structure to find nested UDT typeIds.
    """
    try:
        if isinstance(obj, dict):
            type_id = _get_prop(obj, "typeId")
            if type_id:
                nid = _normalize_typeid(type_id)
                if nid:
                    nested_set.add(nid)

            for value in obj.values():
                _collect_nested_type_ids(value, nested_set)

        elif isinstance(obj, (list, tuple)):
            for item in obj:
                _collect_nested_type_ids(item, nested_set)
    except Exception as e:
        print("Nested parse error:", e)

# 1) Get all UDT definitions
udt_defs = system.tag.browse(
    "[%s]_types_" % provider,
    {"recursive": True, "tagType": "UdtType"}
).getResults()

all_udt_types = set()
nested_udt_types = set()
debug_count = 0

for r in udt_defs:
    full_path = _get_prop(r, "fullPath") or _get_prop(r, "path")
    if not full_path:
        name = _get_prop(r, "name")
        if name:
            all_udt_types.add(str(name))
        continue

    full_path = str(full_path)
    type_name = _type_name_from_fullpath(full_path, provider)
    all_udt_types.add(type_name)

    try:
        # IMPORTANT: pass a STRING path, not a list
        config_results = system.tag.getConfiguration(full_path, True)

        if debug_count < 3:
            print("DEBUG Config for", full_path, ":", config_results)
            debug_count += 1

        _collect_nested_type_ids(config_results, nested_udt_types)

    except Exception as e:
        print("Error getting config for %r : %s" % (full_path, str(e)))

# 2) Get used UDT types from instances
instances = system.tag.browse(
    "[%s]" % provider,
    {"recursive": True, "tagType": "UdtInstance"}
).getResults()

used_udt_types = set()

for i, r in enumerate(instances):
    try:
        type_id = _get_prop(r, "typeId")
        if type_id:
            used_udt_types.add(_normalize_typeid(type_id))
    except Exception as e:
        print("Bad instance at index %s: %s" % (i, str(e)))

# Debug counts
print("UDT types found:", len(all_udt_types))
print("UDT types used :", len(used_udt_types))
print("Nested UDT types:", len(nested_udt_types))

# 3) Write CSV
lines = ['"UDT_Type","Usage","Nested UDT"']

for udt_type in sorted(all_udt_types):
    if udt_type in used_udt_types:
        usage = "USED"
    elif udt_type in nested_udt_types:
        usage = "NESTED"
    else:
        usage = "NOT USED"

    nested = "YES" if udt_type in nested_udt_types else "NO"
    safe = str(udt_type).replace('"', '""')
    lines.append('"%s","%s","%s"' % (safe, usage, nested))

system.file.writeFile(file_path, "\n".join(lines), False)
print("CSV file created at:", file_path)