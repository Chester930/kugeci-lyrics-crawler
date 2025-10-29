# test_apple_simple_loop.py - 簡化版封閉迴路

def reset_position():
    while get_pos_x() > 0:
        move(West)
    while get_pos_y() > 0:
        move(South)

farm_size = get_world_size()
min_cactus = 100

# 無限循環
while True:
    # 檢查仙人掌
    if num_items(Items.Cactus) < min_cactus:
        for i in range(50):
            do_a_flip()
        continue
    
    # 回到起點
    reset_position()
    
    # 裝備恐龍帽
    change_hat(Hats.Dinosaur_Hat)
    
    # 簡單封閉路徑：S型走完所有行，回到起點
    apples = 0
    
    # 走完每一行
    for row in range(farm_size):
        # 偶數行向東，奇數行向西
        for col in range(farm_size - 1):
            if row % 2 == 0:
                move(East)
            else:
                move(West)
        
        # 向北（除了最後一行）
        if row < farm_size - 1:
            move(North)
    
    # 現在在最後一行
    # 22×22: 第21行（奇數行），在左側 (0,21)
    # 向南回到起點 (0,0)
    for i in range(farm_size - 1):
        move(South)
    
    # 完成封閉迴圈！回到 (0,0)
    # 卸下恐龍帽
    change_hat(Hats.Brown_Hat)
    
    # 等待後繼續
    do_a_flip()

# 封閉迴路完成！
# 理論：484 個蘋果 = 234,256 骨頭
