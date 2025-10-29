# test_cactus_green_check.py - 檢查仙人掌為什麼不是綠色

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

print("=== 仙人掌綠色狀態診斷 ===")
print("")

reset_position()

# 隨機檢查幾個仙人掌的狀態
test_positions = [
    (6, 6),   # 左下角
    (10, 10), # 中央
    (15, 15), # 右上角
    (6, 15),  # 左上角
    (15, 6)   # 右下角
]

print("檢查關鍵位置的仙人掌狀態...")
print("")

for pos_x, pos_y in test_positions:
    # 移動到指定位置
    while get_pos_x() < pos_x:
        move(East)
    while get_pos_x() > pos_x:
        move(West)
    while get_pos_y() < pos_y:
        move(North)
    while get_pos_y() > pos_y:
        move(South)
    
    # 檢查狀態
    entity = get_entity_type()
    
    print("位置 (", pos_x, ",", pos_y, ")")
    
    if entity != Entities.Cactus:
        print("  狀態: 沒有仙人掌")
        print("")
        continue
    
    # 仙人掌存在
    can_harvest_status = can_harvest()
    current_size = measure()
    
    print("  仙人掌大小:", current_size)
    print("  是否成熟:", can_harvest_status)
    
    # 檢查四個方向的鄰居
    neighbors_info = []
    
    # 北方
    if pos_y < 15:
        north_size = measure(North)
        north_entity = None  # 無法直接檢查，但可以看大小
        if north_size != None:
            neighbors_info.append(("北", north_size, current_size <= north_size))
        else:
            neighbors_info.append(("北", "無/未成熟", False))
    
    # 東方
    if pos_x < 15:
        east_size = measure(East)
        if east_size != None:
            neighbors_info.append(("東", east_size, current_size <= east_size))
        else:
            neighbors_info.append(("東", "無/未成熟", False))
    
    # 南方
    if pos_y > 6:
        south_size = measure(South)
        if south_size != None:
            neighbors_info.append(("南", south_size, current_size >= south_size))
        else:
            neighbors_info.append(("南", "無/未成熟", False))
    
    # 西方
    if pos_x > 6:
        west_size = measure(West)
        if west_size != None:
            neighbors_info.append(("西", west_size, current_size >= west_size))
        else:
            neighbors_info.append(("西", "無/未成熟", False))
    
    # 顯示鄰居資訊
    print("  鄰居檢查:")
    all_sorted = True
    for direction, size, is_sorted in neighbors_info:
        status_text = "OK" if is_sorted else "NG"
        print("    ", direction, "方:", size, "-", status_text)
        if not is_sorted:
            all_sorted = False
    
    # 判斷是否應該是綠色
    if can_harvest_status and all_sorted:
        print("  => 應該是綠色")
    elif not can_harvest_status:
        print("  => 棕色原因: 自己未成熟")
    elif not all_sorted:
        print("  => 棕色原因: 鄰居未滿足排序條件")
    
    print("")

print("=== 診斷完成 ===")
print("")
print("綠色條件:")
print("1. 自己已成熟")
print("2. 北方和東方 >= 自己大小")
print("3. 南方和西方 <= 自己大小")
print("4. 所有鄰居都已成熟")
print("")
print("相同大小不需要交換！")
