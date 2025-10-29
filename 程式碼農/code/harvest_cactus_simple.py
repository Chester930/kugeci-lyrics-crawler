# harvest_cactus_simple.py - 簡單版仙人掌連鎖採收
# 當所有仙人掌都變綠色時執行

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

print("=== 仙人掌連鎖採收 ===")
print("")

# 移動到右上角 (15, 15)
print("移動到右上角...")
reset_position()

for i in range(15):
    move(East)
for i in range(15):
    move(North)

print("位置: (", get_pos_x(), ",", get_pos_y(), ")")
print("")

# 檢查
entity = get_entity_type()
if entity == Entities.Cactus and can_harvest():
    # 記錄數量
    before = num_items(Items.Cactus)
    print("採收前:", before)
    print("")
    print("執行採收...")
    
    # 採收！
    harvest()
    
    # 結果
    after = num_items(Items.Cactus)
    gained = after - before
    
    print("")
    print("採收後:", after)
    print("獲得:", gained, "個")
    print("")
    
    if gained >= 9000:
        print("完美連鎖！")
    else:
        print("完成採收")
else:
    print("無法採收")
    print("請確認仙人掌已成熟且已排序")

print("")
print("完成")
