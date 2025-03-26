import math
import random

# 定義計算回應時間的函數
def compute_response_time(n, tau, messages):
    response_times = []
    
    #messages.sort()
    Bi = 0

    for i in range(n):
        Pi, Ci, Ti = messages[i]  
        
        Bi = max(messages[i:], key=lambda x: x[1])[1]
        Qi = Bi  
        while True:
            new_Qi = Bi + sum(
                math.ceil((Qi + tau) / Tj) * Cj
                for Pj, Cj, Tj in messages if Pj < Pi  
            )
            if new_Qi == Qi:  
                break
            Qi = new_Qi  
        
        Ri = round(Qi + Ci, 2)
        response_times.append(Ri)
    
    return response_times

# 模擬退火算法來優化任務優先順序
def simulated_annealing(messages, tau, t_start=1000, t_end=1e-3, alpha=0.95, max_iter=1000):
    n = len(messages)
    
    # 隨機打亂任務順序，這樣可以從不同的初始解開始
    current_solution = list(range(n))
    random.shuffle(current_solution)  # 打亂順序
    
    current_response_time = sum(compute_response_time(n, tau, [messages[i] for i in current_solution]))
    best_solution = current_solution[:]
    best_response_time = current_response_time
    
    t = t_start  # 初始溫度

    for _ in range(max_iter):
        # 隨機生成一個鄰居解，通過交換兩個任務位置
        new_solution = current_solution[:]
        i, j = random.sample(range(n), 2)
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
        
        # 計算新解的回應時間
        new_response_time = sum(compute_response_time(n, tau, [messages[i] for i in new_solution]))

        # 接受準則：如果新解的回應時間更小，直接接受
        if new_response_time < current_response_time:
            current_solution = new_solution
            current_response_time = new_response_time
            # 如果新解的回應時間更小，更新最優解
            if new_response_time < best_response_time:
                best_solution = new_solution
                best_response_time = new_response_time
        else:
            # 否則，以某種概率接受較差的解
            delta_cost = new_response_time - current_response_time
            acceptance_prob = math.exp(-delta_cost / t)
            if random.random() < acceptance_prob:
                current_solution = new_solution
                current_response_time = new_response_time

        # 降低溫度
        t *= alpha
        if t < t_end:
            break

    return best_solution, best_response_time

# 讀取輸入數據
messages = []
with open("input.dat") as f:
    lines = f.readlines()

n = int(lines[0].strip())
tau = float(lines[1].strip())
for i in lines[2:]:
    Pi, Ci, Ti = map(float, i.strip().split())
    messages.append((int(Pi), Ci, Ti))

# 使用模擬退火優化任務順序
best_solution, best_response_time = simulated_annealing(messages, tau)

# 輸出最優的任務順序及對應的回應時間
print("Best task order:", best_solution)
print("Best total response time:", best_response_time)

# 顯示每個任務的回應時間
response_times = compute_response_time(n, tau, [messages[i] for i in best_solution])
for i, r in enumerate(response_times):
    print(f"Task {best_solution[i]} response time: {r}")
