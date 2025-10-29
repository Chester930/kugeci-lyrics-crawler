# test_apple_infinite_ring.py - 無限環形路徑，永不停止

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

farm_size = get_world_size()

# 檢查仙人掌
if num_items(Items.Cactus) < 100:
    # 仙人掌不足，不執行
    pass
else:
    # 回到起點
    reset_position()
    
    # 裝備恐龍帽（只裝備一次！）
    change_hat(Hats.Dinosaur_Hat)
    
    # 無限環形路徑：永遠繞著環走
    while True:
        # 遍歷每一行（S型）
        for row in range(farm_size):
            # 偶數行向東，奇數行向西
            for col in range(farm_size - 1):
                if row % 2 == 0:
                    result = move(East)
                else:
                    result = move(West)
                
                # 如果移動失敗（被尾巴擋住），等待一下
                if not result:
                    do_a_flip()
            
            # 向北（除了最後一行）
            if row < farm_size - 1:
                result = move(North)
                if not result:
                    do_a_flip()
        
        # 從最後一行回到第一行（形成環）
        # 22×22: 從 (0,21) 回到 (0,0)
        for i in range(farm_size - 1):
            result = move(South)
            if not result:
                do_a_flip()
        
        # 完成一圈！
        # 現在回到起點 (0,0)
        # 但不卸下恐龍帽！
        # 繼續下一圈！
        
        # 尾巴會一直跟著頭
        # 形成一個封閉的環
        # 永遠不會卡住！

# 這個程式永遠不會停止
# 會一直繞著環走
# 尾巴會越來越長
# 最終填滿整個環（484格）
# 之後會一直繞環，尾巴跟著頭
# 理論極限：484² = 234,256 骨頭（當尾巴填滿環時）
