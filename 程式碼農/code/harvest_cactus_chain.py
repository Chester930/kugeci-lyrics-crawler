# harvest_cactus_chain.py - 仙人掌連鎖採收程式
# 當所有仙人掌都變綠色（已排序）時執行此程式

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

print("=== 仙人掌連鎖採收程式 ===")
print("")

# 移動到右上角 (15, 15) - 排序目標的最大值位置
print("移動到右上角 (15, 15)...")
reset_position()

target_x = 15
target_y = 15

while get_pos_x() < target_x:
    move(East)
while get_pos_y() < target_y:
    move(North)

print("已到達位置: (", get_pos_x(), ",", get_pos_y(), ")")
print("")

# 檢查當前位置
entity = get_entity_type()
if entity != Entities.Cactus:
    print("錯誤：此位置沒有仙人掌！")
    print("請確認仙人掌區已種滿")
else:
    can_harvest_status = can_harvest()
    if not can_harvest_status:
        print("錯誤：仙人掌還未成熟！")
        print("請等待仙人掌成熟後再執行")
    else:
        # 採收前統計
        print("準備採收...")
        print("當前仙人掌大小:", measure())
        print("")
        
        # 記錄採收前的仙人掌數量
        cactus_before = num_items(Items.Cactus)
        print("採收前仙人掌數量:", cactus_before)
        print("")
        
        print("執行連鎖採收...")
        print("====================")
        
        # 執行採收 - 觸發連鎖反應
        harvest()
        
        print("====================")
        print("")
        
        # 採收後統計
        cactus_after = num_items(Items.Cactus)
        gained = cactus_after - cactus_before
        
        print("採收完成！")
        print("採收後仙人掌數量:", cactus_after)
        print("本次獲得:", gained, "個仙人掌")
        print("")
        
        # 計算連鎖數量
        # 如果是完美 10x10，應該得到 100^2 = 10000
        import math
        chain_count = int(math.sqrt(gained))
        
        print("預估連鎖採收數量: 約", chain_count, "個仙人掌")
        print("收益公式驗證:", chain_count, "^2 =", chain_count * chain_count)
        print("")
        
        if gained >= 10000:
            print("完美！獲得滿額 10x10 連鎖採收！")
        elif gained >= 625:
            print("很好！獲得大範圍連鎖採收！")
        elif gained >= 100:
            print("不錯！獲得中等連鎖採收！")
        else:
            print("提示：可能還有部分仙人掌未排序完成")
        
        print("")
        print("下一步：重新種植仙人掌並繼續排序")

print("")
print("程式結束")
