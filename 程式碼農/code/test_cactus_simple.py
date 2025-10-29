# test_cactus_simple.py - 簡單的仙人掌交換測試
# 不使用任何需要解鎖的功能

# 回到起始位置
def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

print("=== 簡單仙人掌交換測試 ===")

reset_position()

# 移動到仙人掌區 (假設農場大小至少為 16x16)
# 移動到 (10, 10) 位置
for i in range(10):
    move(East)
for i in range(10):
    move(North)

print("當前位置: (10, 10)")

# 檢查當前位置
current_entity = get_entity_type()
print("當前實體類型:", current_entity)

if current_entity == Entities.Cactus:
    print("找到仙人掌！")
    
    # 測量當前仙人掌大小
    current_size = measure()
    print("當前仙人掌大小:", current_size)
    
    # 測量北方仙人掌大小
    north_size = measure(North)
    print("北方仙人掌大小:", north_size)
    
    # 測試交換
    if north_size != None:
        if current_size > north_size:
            print("當前仙人掌較大，執行交換...")
            swap(North)
            
            # 檢查交換結果
            new_current = measure()
            new_north = measure(North)
            print("交換後 - 當前:", new_current, "北方:", new_north)
            
            if new_current == north_size and new_north == current_size:
                print("交換成功！")
            else:
                print("交換可能失敗")
        else:
            print("當前仙人掌不大於北方，不需要交換")
    else:
        print("北方沒有仙人掌")
else:
    print("當前位置不是仙人掌")
    print("請確保 (10, 10) 位置有仙人掌")

print("")
print("測試完成！")
