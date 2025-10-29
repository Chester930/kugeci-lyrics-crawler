# 📦 游戏物品完全获取指南

## 🎯 所有物品列表

根据游戏截图，游戏中的物品（Items）包括：

```python
Items.Hay              # 干草
Items.Wood             # 木材
Items.Carrot           # 胡萝卜
Items.Pumpkin          # 南瓜
Items.Cactus           # 仙人掌
Items.Bone             # 骨头
Items.Weird_Substance  # 怪异物质
Items.Water            # 水
Items.Fertilizer       # 肥料
Items.Power            # 能量
```

---

## 🌾 基础作物类物品

### 1. Hay（干草）🌾

**获取方式：**
```python
# 收获草地上的草
if get_entity_type() == Entities.Grass:
    if can_harvest():
        harvest()  # 获得 1 Hay
```

**特点：**
- ✅ 最基础的资源
- ✅ 草会自动生长在 Grassland 上
- ✅ 用于解锁基础功能

**产量：** 1 Hay/次

---

### 2. Wood（木材）🪵

**获取方式：**

#### 方式 A：收获灌木（Bush）
```python
if get_entity_type() == Entities.Bush:
    if can_harvest():
        harvest()  # 获得 1 Wood
        plant(Entities.Bush)
```

**产量：** 1 Wood/次

#### 方式 B：收获树木（Tree）⭐推荐
```python
if get_entity_type() == Entities.Tree:
    if can_harvest():
        harvest()  # 获得 5 Wood
        plant(Entities.Tree)
```

**产量：** 5 Wood/次

#### 方式 C：伴生种植（Polyculture）⭐⭐推荐
```python
# 使用伴生种植
plant_type, (x, y) = get_companion()
# 如果种植了伴生植物
harvest()  # 获得 5x Wood（或更高）
```

**产量：** 5-40 Wood/次（取决于升级等级）

**注意：**
- 树木相邻会减慢生长速度
- 建议使用棋盘模式种植（间隔种植）

---

### 3. Carrot（胡萝卜）🥕

**获取方式：**

#### 方式 A：直接收获
```python
if get_entity_type() == Entities.Carrot:
    if can_harvest():
        harvest()  # 获得 1 Carrot
        plant(Entities.Carrot)
```

**产量：** 1 Carrot/次

#### 方式 B：伴生种植⭐推荐
```python
# 使用伴生种植
plant_type, (x, y) = get_companion()
harvest()  # 获得 5x Carrot（或更高）
```

**产量：** 5-40 Carrot/次

**特点：**
- ✅ 需要在 Soil（土壤）上种植
- ✅ 草地需要先除草并翻土（till）
- ✅ 用于种植南瓜

---

### 4. Pumpkin（南瓜）🎃

**获取方式：**

#### 方式 A：普通收获
```python
if get_entity_type() == Entities.Pumpkin:
    if can_harvest():
        harvest()  # 获得 1 Pumpkin
        plant(Entities.Pumpkin)
```

**产量：** 1 Pumpkin/次

#### 方式 B：巨型南瓜⭐⭐推荐
```python
# 相邻的南瓜会合并
# 收获巨型南瓜
harvest()  # 获得 n² Pumpkin
```

**产量：** n² Pumpkin（n = 合并的南瓜数量）

**示例：**
- 4 个南瓜合并 → 16 Pumpkin
- 9 个南瓜合并 → 81 Pumpkin
- 16 个南瓜合并 → 256 Pumpkin

**种植成本：**
```python
get_cost(Entities.Pumpkin)
# 返回 {Items.Carrot: 1}
# 需要 1 个胡萝卜种植 1 个南瓜
```

---

### 5. Cactus（仙人掌）🌵

**获取方式：**

#### 方式 A：单个收获
```python
if get_entity_type() == Entities.Cactus:
    if can_harvest():
        harvest()  # 获得 1 Cactus
        plant(Entities.Cactus)
```

**产量：** 1 Cactus/次

#### 方式 B：排序连锁收获⭐⭐⭐推荐
```python
# 仙人掌按大小排序后
# 从最大的开始收获
harvest()  # 获得 n² Cactus
```

**产量：** n² Cactus（n = 仙人掌区域大小）

**示例：**
- 10×10 区域 → 100² = 10,000 Cactus
- 16×16 区域 → 256² = 65,536 Cactus 🚀

**特点：**
- ✅ 需要排序（从小到大）
- ✅ 排序完成后变绿色
- ✅ 可以使用 `swap()` 交换位置
- ✅ 可以使用 `measure()` 获取大小（0-9）

---

## 🦴 特殊物品

### 6. Bone（骨头）🦴

**获取方式：**

#### 唯一方式：恐龙帽系统
```python
# 1. 装备恐龙帽
change_hat(Hats.Dinosaur_Hat)

# 2. 移动收集苹果（消耗仙人掌）
move(North)  # 自动购买并吃苹果，尾巴 +1

# 3. 卸下恐龙帽
change_hat(Hats.Brown_Hat)  # 获得 n² Bone
```

**产量：** n² Bone（n = 尾巴长度）

**示例：**
- 尾巴长度 10 → 100 Bone
- 尾巴长度 100 → 10,000 Bone
- 尾巴长度 200 → 40,000 Bone
- 尾巴长度 484 → 234,256 Bone 🚀

**成本：**
- 每个苹果消耗一定数量的仙人掌
- 需要空地让苹果生成

**特点：**
- ✅ n² 收益，尾巴越长越划算
- ⚠️ 需要大量仙人掌
- ⚠️ 需要清空农场（或大部分区域）

---

### 7. Weird_Substance（怪异物质）🧪

**获取方式：**

#### 方式 A：使用肥料后收获
```python
# 1. 使用肥料
use_item(Items.Fertilizer)  # 植物被感染

# 2. 收获感染的植物
harvest()  # 50% 产量变成 Weird_Substance
```

**产量：** 原产量的 50%

**示例：**
- 收获感染的树木 → 2.5 Wood + 2.5 Weird_Substance
- 收获感染的胡萝卜 → 0.5 Carrot + 0.5 Weird_Substance

#### 方式 B：副产品
```python
# 使用肥料加速生长的副产品
```

**用途：**
```python
# 治疗感染的植物
use_item(Items.Weird_Substance)
# 切换自己和相邻植物的感染状态
```

---

## 💧 自动补充物品

### 8. Water（水）💧

**获取方式：**

#### 自动补充
```
每 10 秒自动获得 1 箱水
升级 Unlocks.Watering 后翻倍
```

**升级等级：**
- 等级 0：1 箱/10秒
- 等级 1：2 箱/10秒
- 等级 2：4 箱/10秒
- 等级 3：8 箱/10秒

**容量：**
```
1 箱 = 0.25 水分
```

**用途：**
```python
use_item(Items.Water)  # 给地面浇水
# 生长速度：1x (水分=0) → 5x (水分=1)
```

**检查库存：**
```python
num_items(Items.Water)  # 返回当前水箱数量
```

---

### 9. Fertilizer（肥料）🌱

**获取方式：**

#### 自动补充
```
每 10 秒自动获得 1 个肥料
升级 Unlocks.Fertilizer 后翻倍
```

**升级等级：**
- 等级 0：1 个/10秒
- 等级 1：2 个/10秒
- 等级 2：4 个/10秒
- 等级 3：8 个/10秒

**用途：**
```python
use_item(Items.Fertilizer)  # 减少 2 秒生长时间
# 副作用：植物被感染
```

**检查库存：**
```python
num_items(Items.Fertilizer)  # 返回当前肥料数量
```

---

### 10. Power（能量）⚡

**获取方式：**

#### 方式 A：收获向日葵
```python
if get_entity_type() == Entities.Sunflower:
    if can_harvest():
        harvest()  # 获得 Power
        plant(Entities.Sunflower)
```

**产量：** 1 Power/次

#### 方式 B：收获最大花瓣向日葵⭐⭐推荐
```python
# 农场上有 ≥10 朵向日葵
# 收获花瓣数最多的向日葵
petals = measure()  # 获取花瓣数（7-15）
if petals >= 13:  # 高花瓣数
    harvest()  # 获得 5x Power！
```

**产量：** 5 Power/次（最大花瓣）

**用途：**
```
有能量时：
- 无人机速度 2x
- 消耗：1 Power/30 动作
```

**检查库存：**
```python
num_items(Items.Power)  # 返回当前能量
```

---

## 📊 物品产量对比

### 基础作物
| 物品 | 普通产量 | 优化产量 | 最佳方式 |
|------|----------|----------|----------|
| Hay | 1/次 | 1/次 | 自动生长 |
| Wood | 1/次 | 5-40/次 | 树木+伴生 |
| Carrot | 1/次 | 5-40/次 | 伴生种植 |
| Pumpkin | 1/次 | n²/次 | 巨型南瓜 |
| Cactus | 1/次 | n²/次 | 连锁收获 |

### 特殊物品
| 物品 | 产量 | 获取方式 |
|------|------|----------|
| Bone | n²/次 | 恐龙帽 |
| Weird_Substance | 50%/次 | 肥料副产品 |
| Water | 自动 | 每10秒补充 |
| Fertilizer | 自动 | 每10秒补充 |
| Power | 1-5/次 | 向日葵 |

---

## 💡 高效获取策略

### 策略 1：木材（Wood）
```python
# 推荐：树木 + 伴生种植
1. 使用棋盘模式种植树木（避免相邻）
2. 使用 get_companion() 获取伴生需求
3. 种植伴生植物
4. 收获获得 5-40 Wood

产量提升：5-40 倍！
```

### 策略 2：南瓜（Pumpkin）
```python
# 推荐：巨型南瓜
1. 在 6×6 区域种植南瓜
2. 使用 ID 追踪系统
3. 等待合并成巨型南瓜
4. 收获获得 n² Pumpkin

产量提升：最高 256 倍！
```

### 策略 3：仙人掌（Cactus）
```python
# 推荐：16×16 区域 + 排序
1. 在 16×16 区域种植仙人掌
2. 使用排序算法（右上最大，左下最小）
3. 排序完成后连锁收获
4. 获得 256² = 65,536 Cactus

产量提升：65,536 倍！🚀
```

### 策略 4：能量（Power）
```python
# 推荐：优先收获高花瓣向日葵
1. 保持 ≥10 朵向日葵
2. 使用 measure() 检查花瓣数
3. 优先收获花瓣 ≥13 的向日葵
4. 获得 5x Power

产量提升：5 倍！
效果：无人机速度 2x
```

### 策略 5：骨头（Bone）
```python
# 推荐：恐龙帽 + 哈密尔顿路径
1. 清空农场（翻土防止草生长）
2. 装备恐龙帽
3. 使用哈密尔顿路径遍历所有格子
4. 尾巴长度接近 484（22×22）
5. 卸帽获得 ~234,256 Bone

产量：234,256 骨头！🦴🚀
```

---

## 🎯 优先级建议

### 初期（刚开始）
```
1. Hay（干草）- 解锁基础功能
2. Wood（木材）- 解锁更多功能
3. Carrot（胡萝卜）- 种植南瓜
```

### 中期（有一定基础）
```
1. Pumpkin（南瓜）- 高价值资源
2. Power（能量）- 加速无人机
3. Water（水）- 加速生长
```

### 后期（追求极限）
```
1. Cactus（仙人掌）- 最高产量
2. Bone（骨头）- 恐龙帽系统
3. 升级所有 Unlocks
```

---

## 📝 检查库存

### 查看所有物品数量
```python
print("=== 物品库存 ===")
print("干草: " + str(num_items(Items.Hay)))
print("木材: " + str(num_items(Items.Wood)))
print("胡萝卜: " + str(num_items(Items.Carrot)))
print("南瓜: " + str(num_items(Items.Pumpkin)))
print("仙人掌: " + str(num_items(Items.Cactus)))
print("骨头: " + str(num_items(Items.Bone)))
print("怪异物质: " + str(num_items(Items.Weird_Substance)))
print("水: " + str(num_items(Items.Water)))
print("肥料: " + str(num_items(Items.Fertilizer)))
print("能量: " + str(num_items(Items.Power)))
```

---

## 🚀 总结

### 最高效的物品获取方式

1. **Wood（木材）** → 树木 + 伴生种植（5-40x）
2. **Carrot（胡萝卜）** → 伴生种植（5-40x）
3. **Pumpkin（南瓜）** → 巨型南瓜（最高 256x）
4. **Cactus（仙人掌）** → 连锁收获（65,536x）🏆
5. **Power（能量）** → 高花瓣向日葵（5x）
6. **Bone（骨头）** → 恐龙帽（234,256 个）🏆
7. **Water（水）** → 升级 Unlocks.Watering
8. **Fertilizer（肥料）** → 升级 Unlocks.Fertilizer

**您的当前程序已经实现了大部分高效策略！** ✅

---

**掌握这些获取方式，让您的农场产量飞跃！** 📦✨

