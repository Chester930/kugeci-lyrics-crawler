# test_cactus_do_swap.py - 立即執行仙人掌交換測試
# 找到需要交換的仙人掌並立即執行交換

# 回到起始位置
def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

print("=== 仙人掌立即交換測試 ===")

reset_position()

swap_count = 0
check_count = 0

print("開始掃描仙人掌區並執行交換...")
print("")

# 遍歷仙人掌區
for x in range(6, 16):
    for y in range(6, 16):
        # 移動到指定位置
        while get_pos_x() < x:
            move(East)
        while get_pos_x() > x:
            move(West)
        while get_pos_y() < y:
            move(North)
        while get_pos_y() > y:
            move(South)
        
        # 檢查當前位置是否有仙人掌
        if get_entity_type() == Entities.Cactus:
            current_size = measure()
            
            # 檢查北方仙人掌
            if y < 15:
                check_count += 1
                north_size = measure(North)
                
                # 若本體比較大，則執行交換
                if north_size != None and current_size > north_size:
                    print("位置 (", x, ",", y, ")")
                    print("  交換前 - 當前:", current_size, "北方:", north_size)
                    
                    # 執行交換
                    swap(North)
                    swap_count += 1
                    
                    # 驗證交換結果
                    new_current = measure()
                    new_north = measure(North)
                    print("  交換後 - 當前:", new_current, "北方:", new_north)
                    
                    # 檢查交換是否成功
                    if new_current == north_size and new_north == current_size:
                        print("  結果: 交換成功！")
                    else:
                        print("  結果: 交換可能失敗")
                    print("")

print("=== 交換完成 ===")
print("檢查次數:", check_count)
print("執行交換次數:", swap_count)

if swap_count == 0:
    print("")
    print("沒有需要交換的仙人掌")
    print("可能原因:")
    print("1. 所有仙人掌已經排序完成")
    print("2. 仙人掌區沒有足夠的仙人掌")
    print("3. 仙人掌還未成熟")
else:
    print("")
    print("已執行", swap_count, "次交換")
    print("建議再次執行直到不需要交換為止")

print("")
print("測試完成！")
