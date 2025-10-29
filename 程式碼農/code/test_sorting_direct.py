# test_sorting_direct.py - 直接測試排序函數

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

print("=== 直接測試仙人掌排序函數 ===")
print("")

# 測試橫向排序函數
print("--- 測試1: 橫向排序 (檢查北方) ---")
reset_position()
horizontal_swap_count = 0

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
            
            # 橫向移動：檢查北方仙人掌
            if y < 15:
                north_size = measure(North)
                if north_size != None and current_size > north_size:
                    swap(North)
                    horizontal_swap_count += 1

print("橫向排序完成，交換次數:", horizontal_swap_count)
print("")

# 等待一下
for i in range(3):
    do_a_flip()

# 測試縱向排序函數
print("--- 測試2: 縱向排序 (檢查東方) ---")
reset_position()
vertical_swap_count = 0

for y in range(6, 16):
    for x in range(6, 16):
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
            
            # 縱向移動：檢查東方仙人掌
            if x < 15:
                east_size = measure(East)
                if east_size != None and current_size > east_size:
                    swap(East)
                    vertical_swap_count += 1

print("縱向排序完成，交換次數:", vertical_swap_count)
print("")

print("=== 總結 ===")
print("橫向交換次數:", horizontal_swap_count)
print("縱向交換次數:", vertical_swap_count)
print("總交換次數:", horizontal_swap_count + vertical_swap_count)
print("")

if horizontal_swap_count > 0 or vertical_swap_count > 0:
    print("排序函數可以正常工作！")
    print("建議：將此邏輯整合到主程式")
else:
    print("沒有執行任何交換")
    print("可能原因:")
    print("1. 仙人掌已經排序完成")
    print("2. 仙人掌還未成熟")
    print("3. 仙人掌數量不足")

print("")
print("測試完成！")
