"""输出无副作用的 Looma Skill 脚本运行时验证结果。"""

import json
import sys


result = {
    "plugin": "looma-test-plugin",
    "skill": "verify-looma-plugin",
    "runtime": "skill-script",
    "status": "success",
    "args": sys.argv[1:],
}

print(json.dumps(result, ensure_ascii=False))
