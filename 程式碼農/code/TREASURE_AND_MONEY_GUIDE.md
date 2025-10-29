# 💰 宝箱与金钱系统完全指南

## 🤔 您的问题

> **"有任何可以得到宝箱或金钱的方法吗？我在技能树中有看到需要花费的图示。但我不知道那是什么？"**

---

## 📋 答案总结

### ❌ **游戏中没有"金钱"系统**

根据所有官方文档和游戏机制，**"程式碼農"游戏中不存在传统的"金钱"或"货币"系统**。

### ✅ **技能树的"花费"是指物品（Items）**

您在技能树中看到的"花费图示"，指的是**游戏物品（Items）**，而不是金钱。

---

## 💎 解锁系统详解

### 技能树解锁机制

#### 1. **解锁需要消耗物品**
```python
# 查询解锁成本
cost = get_cost(Unlocks.Loops)
# 返回：{Items.Hay: 5}
# 意思：解锁循环功能需要 5 个干草
```

#### 2. **不同解锁需要不同物品**
```python
# 示例：
get_cost(Unlocks.Loops, 0)      # {Items.Hay: 5}
get_cost(Unlocks.Speed, 0)      # {Items.Wood: 10}
get_cost(Unlocks.Expand, 0)     # {Items.Pumpkin: 100}
get_cost(Unlocks.Watering, 0)   # {Items.Water: 50}
```

#### 3. **解锁等级越高，成本越高**
```python
# 第 0 级（第一次解锁）
get_cost(Unlocks.Speed, 0)  # {Items.Wood: 10}

# 第 1 级（第二次升级）
get_cost(Unlocks.Speed, 1)  # {Items.Wood: 50}

# 第 2 级（第三次升级）
get_cost(Unlocks.Speed, 2)  # {Items.Wood: 200}
```

---

## 🎯 如何获取"花费"所需的物品

### 常见解锁成本物品

| 物品 | 获取方式 | 产量 | 难度 |
|------|---------|------|------|
| **Hay（干草）** | 收获草地上的草 | 1/次 | ⭐ 简单 |
| **Wood（木材）** | 收获树木 | 5/次 | ⭐⭐ 简单 |
| **Carrot（胡萝卜）** | 种植并收获胡萝卜 | 1/次 | ⭐⭐ 中等 |
| **Pumpkin（南瓜）** | 种植并收获南瓜 | 1-20736/次 | ⭐⭐⭐ 中等 |
| **Cactus（仙人掌）** | 种植并收获仙人掌 | 1-160000/次 | ⭐⭐⭐⭐ 困难 |
| **Bone（骨头）** | 恐龙帽系统 | n²/次 | ⭐⭐⭐⭐⭐ 高级 |

---

### 1. Hay（干草）🌾

**用途：** 解锁基础功能（循环、变量、函数等）

**获取方式：**
```python
# 收获草地上的草
if get_entity_type() == Entities.Grass:
    if can_harvest():
        harvest()  # 获得 1 Hay
```

**特点：**
- ✅ 最基础的资源
- ✅ 草会自动生长
- ✅ 无需种植

---

### 2. Wood（木材）🪵

**用途：** 解锁中级功能（速度、扩展等）

**获取方式：**

#### 方式 A：收获树木（推荐）
```python
if get_entity_type() == Entities.Tree:
    if can_harvest():
        harvest()  # 获得 5 Wood
        plant(Entities.Tree)
```

#### 方式 B：伴生种植（高产）
```python
# 使用伴生种植系统
plant_type, (x, y) = get_companion()
# 种植伴生植物后
harvest()  # 获得 5-40 Wood（取决于升级等级）
```

**产量：** 5-40 Wood/次

---

### 3. Pumpkin（南瓜）🎃

**用途：** 解锁高级功能（扩展、仙人掌等）

**获取方式：**

#### 方式 A：直接收获
```python
plant(Entities.Pumpkin)  # 需要 1 Carrot
# 等待成熟
harvest()  # 获得 1 Pumpkin
```

#### 方式 B：巨型南瓜（推荐）
```python
# 在 6×6 区域种植南瓜
# 等待合并成巨型南瓜
harvest()  # 获得 n*n*6 Pumpkin（最高 20,736）
```

**产量：** 1-20,736 Pumpkin/次

---

### 4. Cactus（仙人掌）🌵

**用途：** 解锁顶级功能（恐龙帽等）

**获取方式：**

#### 方式 A：直接收获
```python
plant(Entities.Cactus)
# 等待成熟
harvest()  # 获得 1 Cactus
```

#### 方式 B：连锁收获（推荐）
```python
# 在 20×20 区域种植仙人掌
# 使用排序算法排序
# 从右上角触发连锁收获
harvest()  # 获得 400² = 160,000 Cactus
```

**产量：** 1-160,000 Cactus/次

---

### 5. Bone（骨头）🦴

**用途：** 解锁最高级功能（未知）

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
- 尾巴长度 100 → 10,000 Bone
- 尾巴长度 484 → 234,256 Bone

---

## 🗺️ 宝箱（Treasure）系统

### ❓ **宝箱在哪里？**

根据您之前提供的图片和文档，**宝箱（Entities.Treasure）** 是游戏中的一种特殊实体。

### 📍 **如何获得宝箱？**

#### 方式：种植迷宫

```python
# 1. 在灌木（Bush）上使用 Weird_Substance
if get_entity_type() == Entities.Bush:
    use_item(Items.Weird_Substance)
    # 灌木会生长成迷宫

# 2. 迷宫中会出现宝箱（Treasure）
# 3. 收获宝箱获得奖励
if get_entity_type() == Entities.Treasure:
    harvest()  # 获得奖励（具体内容未知）
```

---

### 🧪 **如何获得 Weird_Substance？**

#### 方式 A：使用肥料后收获
```python
# 1. 使用肥料
use_item(Items.Fertilizer)  # 植物被感染

# 2. 收获感染的植物
harvest()  # 50% 产量变成 Weird_Substance
```

**示例：**
- 收获感染的南瓜 → 0.5 Pumpkin + 0.5 Weird_Substance
- 收获感染的仙人掌 → 0.5 Cactus + 0.5 Weird_Substance

#### 方式 B：使用 f3.py 或 f4.py 策略
```python
# f3.py：直接采收模式
# 产量：~20,000 Weird_Substance/小时

# f4.py：排序+连锁模式（推荐）
# 产量：~100,000 Weird_Substance/小时
```

---

## 🎯 解锁优先级建议

### 初期（刚开始）
```
1. Unlocks.Variables（变量）- 需要 Hay
2. Unlocks.Loops（循环）- 需要 Hay
3. Unlocks.Functions（函数）- 需要 Hay
4. Unlocks.Plant（种植）- 需要 Hay
```

### 中期（有一定基础）
```
1. Unlocks.Speed（速度）- 需要 Wood
2. Unlocks.Expand（扩展）- 需要 Pumpkin
3. Unlocks.Watering（浇水）- 需要 Water
4. Unlocks.Polyculture（伴生种植）- 需要 Wood
```

### 后期（追求极限）
```
1. Unlocks.Cactus（仙人掌）- 需要 Cactus
2. Unlocks.Dinosaurs（恐龙帽）- 需要 Bone
3. Unlocks.Fertilizer（肥料）- 需要 Fertilizer
4. 升级所有 Unlocks 到最高等级
```

---

## 🔧 自动解锁系统

### 使用 `unlock()` 函数

```python
# 1. 查询解锁成本
cost = get_cost(Unlocks.Speed)
# 返回：{Items.Wood: 10}

# 2. 检查是否有足够物品
if num_items(Items.Wood) >= cost[Items.Wood]:
    # 3. 执行解锁
    unlock(Unlocks.Speed)
```

### 完整自动解锁示例

```python
def auto_unlock(unlock_type):
    # 查询成本
    cost = get_cost(unlock_type)
    
    # 如果已经最高等级
    if cost == None:
        return True  # 已解锁
    
    # 检查是否有足够物品
    can_unlock = True
    for item in cost:
        if num_items(item) < cost[item]:
            can_unlock = False
            break
    
    # 执行解锁
    if can_unlock:
        unlock(unlock_type)
        return True
    else:
        return False  # 物品不足

# 使用示例
auto_unlock(Unlocks.Speed)
auto_unlock(Unlocks.Expand)
auto_unlock(Unlocks.Watering)
```

---

## 📊 技能树花费总览

### 常见解锁及其成本（估计）

| 解锁功能 | 第 0 级成本 | 第 1 级成本 | 第 2 级成本 |
|---------|-----------|-----------|-----------|
| **Variables** | Hay: 5 | Hay: 20 | Hay: 100 |
| **Loops** | Hay: 5 | Hay: 20 | Hay: 100 |
| **Functions** | Hay: 10 | Hay: 50 | Hay: 200 |
| **Speed** | Wood: 10 | Wood: 50 | Wood: 200 |
| **Expand** | Pumpkin: 100 | Pumpkin: 500 | Pumpkin: 2000 |
| **Watering** | Water: 50 | Water: 200 | Water: 1000 |
| **Cactus** | Cactus: 1000 | Cactus: 5000 | Cactus: 20000 |
| **Dinosaurs** | Bone: 10000 | Bone: 50000 | Bone: 200000 |

**注意：** 以上成本为估计值，实际成本请使用 `get_cost()` 函数查询。

---

## 🎉 总结

### 关键要点

#### 1. **没有"金钱"系统**
```
游戏中不存在传统的货币或金钱
所有"花费"都是指游戏物品（Items）
```

#### 2. **技能树花费 = 物品**
```
使用 get_cost() 查询解锁成本
返回的是物品字典，例如 {Items.Hay: 5}
```

#### 3. **宝箱获取方式**
```
1. 使用 Weird_Substance 在灌木上生成迷宫
2. 迷宫中会出现宝箱（Treasure）
3. 收获宝箱获得奖励
```

#### 4. **Weird_Substance 获取**
```
方式 A：使用肥料感染植物，收获时获得
方式 B：使用 f3.py 或 f4.py 策略大量生产
```

#### 5. **解锁优先级**
```
初期：Hay（干草）→ 基础功能
中期：Wood（木材）→ 速度和扩展
后期：Pumpkin/Cactus → 高级功能
顶级：Bone（骨头）→ 恐龙帽系统
```

---

## 🔍 查询成本的实用工具

### 创建成本查询程序

```python
# cost_checker.py - 成本查询工具

def check_unlock_cost(unlock_type, level=None):
    """查询解锁成本"""
    if level == None:
        cost = get_cost(unlock_type)
    else:
        cost = get_cost(unlock_type, level)
    
    if cost == None:
        # 已达到最高等级
        return None
    
    return cost

def check_can_afford(unlock_type, level=None):
    """检查是否有足够物品解锁"""
    cost = check_unlock_cost(unlock_type, level)
    
    if cost == None:
        return True  # 已最高等级
    
    for item in cost:
        if num_items(item) < cost[item]:
            return False
    
    return True

# 使用示例
# cost = check_unlock_cost(Unlocks.Speed, 0)
# can_afford = check_can_afford(Unlocks.Speed, 0)
```

---

## 📝 常见问题 FAQ

### Q1: 我在技能树看到的图示是什么？
**A:** 那是**物品图标**，表示解锁该功能需要消耗的物品类型和数量。

### Q2: 游戏中有金钱或货币吗？
**A:** **没有**。游戏中所有交易和解锁都使用物品（Items），不存在传统的金钱系统。

### Q3: 如何获得宝箱？
**A:** 使用 `Items.Weird_Substance` 在灌木（Bush）上生成迷宫，迷宫中会出现宝箱（Treasure）。

### Q4: 宝箱里有什么？
**A:** 根据官方文档，宝箱是一种特殊实体，收获后会获得奖励，但具体内容未在文档中详细说明。

### Q5: 如何快速获得大量物品？
**A:** 使用高级策略：
- **Wood**: 伴生种植（5-40/次）
- **Pumpkin**: 巨型南瓜（最高 20,736/次）
- **Cactus**: 连锁收获（最高 160,000/次）
- **Bone**: 恐龙帽系统（最高 1,048,576/次）

### Q6: 我应该先解锁什么？
**A:** 建议顺序：
1. 基础功能（Variables, Loops, Functions）
2. 速度升级（Speed）
3. 地图扩展（Expand）
4. 浇水系统（Watering）
5. 高级作物（Cactus, Dinosaurs）

---

**希望这份指南解答了您的疑问！** 💰✨🎯

