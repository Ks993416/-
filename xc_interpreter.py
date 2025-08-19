import re
import sys

def run_xc(path):
    variables = {}
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    for i, raw in enumerate(lines, start=1):
        line = raw.strip()

        # Убираем комментарии после #
        if "#" in line:
            line = line.split("#", 1)[0].strip()
        if not line:
            continue

        try:
            # SAY "text"
            m = re.fullmatch(r'SAY\s+"(.*)"', line)
            if m:
                print(m.group(1))
                continue

            # SET name number
            m = re.fullmatch(r'SET\s+([A-Za-z_]\w*)\s+(-?\d+)', line)
            if m:
                name, num = m.group(1), int(m.group(2))
                variables[name] = num
                continue

            # ADD name number
            m = re.fullmatch(r'ADD\s+([A-Za-z_]\w*)\s+(-?\d+)', line)
            if m:
                name, num = m.group(1), int(m.group(2))
                if name not in variables:
                    raise ValueError(f"Переменная '{name}' не создана")
                variables[name] += num
                continue

            # SUB name number
            m = re.fullmatch(r'SUB\s+([A-Za-z_]\w*)\s+(-?\d+)', line)
            if m:
                name, num = m.group(1), int(m.group(2))
                if name not in variables:
                    raise ValueError(f"Переменная '{name}' не создана")
                variables[name] -= num
                continue

            # SHOW name
            m = re.fullmatch(r'SHOW\s+([A-Za-z_]\w*)', line)
            if m:
                name = m.group(1)
                if name not in variables:
                    raise ValueError(f"Переменная '{name}' не создана")
                print(variables[name])
                continue

            # IF name op number THEN SAY "text"
            m = re.fullmatch(
                r'IF\s+([A-Za-z_]\w*)\s*(==|>|<)\s*(-?\d+)\s*THEN\s*SAY\s+"(.*)"',
                line
            )
            if m:
                name, op, num, text = m.group(1), m.group(2), int(m.group(3)), m.group(4)
                if name not in variables:
                    raise ValueError(f"Переменная '{name}' не создана")
                val = variables[name]
                cond = (val == num) if op == "==" else (val > num) if op == ">" else (val < num)
                if cond:
                    print(text)
                continue

            # Ничего не подошло — синтаксическая ошибка
            raise SyntaxError("Не понимаю эту строку")

        except Exception as e:
            print(f"[Строка {i}] Ошибка: {e}\n  -> {raw.rstrip()}")
            return

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Использование: python xc_interpreter.py путь/к/файлу.xc")
    else:
        run_xc(sys.argv[1])
