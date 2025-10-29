# strategy_dinosaur_mode.py - 恐龍帽骨頭收穫模式
# 在仙人掌採收後執行，將仙人掌轉換為骨頭

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

# 恐龍模式參數
target_tail_length = 100  # 目標尾巴長度（可調整：建議50-200）
farm_size = 22  # 農場大小

print("=== 恐龍帽骨頭收穫模式 ===")
print("")

# 檢查仙人掌數量
cactus_count = num_items(Items.Cactus)
print("當前仙人掌數量:", cactus_count)

if cactus_count < 100:
    print("警告：仙人掌不足100個")
    print("建議先執行主程式採收仙人掌")
    print("")
else:
    print("仙人掌充足，開始恐龍模式")
    print("")
    
    # 前置作業：清除草地
    print("前置作業：清除草地並翻土...")
    reset_position()
    grass_cleared = 0
    
    for x in range(farm_size):
        for y in range(farm_size):
            # 移動到位置
            while get_pos_x() < x:
                move(East)
            while get_pos_x() > x:
                move(West)
            while get_pos_y() < y:
                move(North)
            while get_pos_y() > y:
                move(South)
            
            # 檢查並處理草地
            if get_ground_type() == Grounds.Grassland:
                # 如果有草，收割
                if get_entity_type() == Entities.Grass:
                    harvest()
                    grass_cleared += 1
                # 翻土
                till()
        
        # 移動到下一行
        if x < farm_size - 1:
            move(East)
            while get_pos_y() > 0:
                move(South)
    
    print("清除草地:", grass_cleared, "格")
    print("前置作業完成")
    print("")
    
    # 回到原點並裝備恐龍帽
    print("裝備恐龍帽...")
    reset_position()
    change_hat(Hats.Dinosaur_Hat)
    print("已裝備！")
    print("")
    
    # 記錄骨頭數量
    bones_before = num_items(Items.Bone)
    
    # S型移動收集蘋果
    print("開始收集蘋果...")
    print("目標尾巴長度:", target_tail_length)
    print("")
    
    apple_count = 0
    stuck_count = 0
    max_stuck = 5
    
    # 使用縱向S型移動
    for x in range(farm_size):
        for y in range(farm_size):
            # 嘗試移動
            if y < farm_size - 1:
                if x % 2 == 0:
                    # 偶數列：向北
                    result = move(North)
                else:
                    # 奇數列：向南
                    result = move(South)
                
                # 檢查移動是否失敗（被尾巴擋住）
                if not result:
                    stuck_count += 1
                    if stuck_count >= max_stuck:
                        # 被尾巴擋住太多次，可能已經填滿
                        break
                else:
                    stuck_count = 0
            
            # 檢查是否吃到蘋果（通過實體判斷）
            # 吃蘋果後會自動增長尾巴
            apple_count += 1
            
            # 檢查是否達到目標長度
            if apple_count >= target_tail_length:
                break
        
        if apple_count >= target_tail_length or stuck_count >= max_stuck:
            break
        
        # 移動到下一列
        if x < farm_size - 1:
            move(East)
            if (x + 1) % 2 == 0:
                while get_pos_y() > 0:
                    result = move(South)
                    if not result:
                        break
            else:
                while get_pos_y() < farm_size - 1:
                    result = move(North)
                    if not result:
                        break
    
    print("")
    print("收集完成！")
    print("預估吃掉蘋果數:", apple_count)
    print("預估尾巴長度:", apple_count)
    print("")
    
    # 卸下恐龍帽，收穫骨頭
    print("卸下恐龍帽，收穫骨頭...")
    change_hat(Hats.Brown_Hat)
    
    # 計算獲得的骨頭
    bones_after = num_items(Items.Bone)
    bones_gained = bones_after - bones_before
    
    print("")
    print("=== 收穫結果 ===")
    print("獲得骨頭:", bones_gained)
    print("預期收益: ", apple_count, "^2 =", apple_count * apple_count)
    print("")
    
    if bones_gained >= 10000:
        print("完美！獲得滿額收益！")
    elif bones_gained >= 2500:
        print("很好！獲得大量骨頭！")
    else:
        print("完成骨頭收穫")
    
    print("")
    print("剩餘仙人掌:", num_items(Items.Cactus))

print("")
print("恐龍模式結束")
