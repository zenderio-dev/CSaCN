mac = input("Введите MAC-адрес (например F0-79-59-70-A7-20): ")
prefix = mac.upper().replace("-", "").replace(":", "")[:6]

with open("mac-vendor.txt", encoding="utf-8", errors="ignore") as f:
    for line in f:
        parts = line.split(maxsplit=1)
        if parts and parts[0] == prefix:
            print(parts[1].strip())
            break
    else:
        print("Производитель не найден")
