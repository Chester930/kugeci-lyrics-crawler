# test_dinosaur_space_calc.py - 計算恐龍模式需要的空間

print("=== 恐龍模式空間計算器 ===")
print("")

# 參數設定
farm_size = 22
target_tail_length = 200  # 目標尾巴長度

print("農場大小:", farm_size, "x", farm_size)
print("目標尾巴長度:", target_tail_length)
print("")

# 計算總格子數
total_tiles = farm_size * farm_size
print("農場總格子數:", total_tiles)
print("")

# 計算空間需求
print("=== 空間需求分析 ===")
print("")

# 恐龍需要的格子 = 尾巴長度 + 1（頭）
dinosaur_tiles = target_tail_length + 1
print("恐龍佔用格子:", dinosaur_tiles)
print("  - 頭部: 1 格")
print("  - 尾巴:", target_tail_length, "格")
print("")

# 剩餘可用空間
remaining_tiles = total_tiles - dinosaur_tiles
print("剩餘可用格子:", remaining_tiles)
print("")

# 使用率
usage_percent = (dinosaur_tiles * 100) / total_tiles
print("農場使用率:", usage_percent, "%")
print("")

# 建議
print("=== 建議 ===")
print("")

if target_tail_length >= total_tiles:
    print("警告：目標尾巴長度超過農場大小！")
    print("最大可能長度:", total_tiles - 1)
elif target_tail_length > total_tiles * 0.8:
    print("警告：尾巴太長，可能會堵住自己")
    print("建議最大長度:", total_tiles * 0.8)
elif target_tail_length > total_tiles * 0.5:
    print("提示：尾巴較長，需要小心規劃路徑")
    print("當前設定可行，但空間較緊")
else:
    print("設定合理，有足夠的活動空間")

print("")
print("=== 不同尾巴長度的收益對比 ===")
print("")

test_lengths = [50, 100, 150, 200, 250, 300, 400, 484]
for length in test_lengths:
    if length <= total_tiles:
        bones = length * length
        usage = (length * 100) / total_tiles
        print("尾巴", length, ":")
        print("  收益:", bones, "骨頭")
        print("  使用率:", usage, "%")
        if length <= total_tiles * 0.5:
            print("  評價: 安全")
        elif length <= total_tiles * 0.8:
            print("  評價: 適中")
        else:
            print("  評價: 危險")
        print("")

print("=== 推薦設定 ===")
print("")

# 推薦設定
safe_length = total_tiles / 2
optimal_length = total_tiles * 0.7
max_length = total_tiles - 1

print("保守設定:", safe_length)
print("  - 收益:", safe_length * safe_length, "骨頭")
print("  - 風險: 低")
print("")

print("推薦設定:", optimal_length)
print("  - 收益:", optimal_length * optimal_length, "骨頭")
print("  - 風險: 中")
print("")

print("極限設定:", max_length)
print("  - 收益:", max_length * max_length, "骨頭")
print("  - 風險: 高")
print("")

print("測試完成！")
