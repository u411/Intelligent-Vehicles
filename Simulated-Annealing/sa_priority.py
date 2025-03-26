import math
import random
import time

# 計算每則訊息的最壞情形響應時間
def compute_response_time(n, tau, messages, priorities):
    response_times = []
    
    # 根據優先權排序，較小數值（高優先權）排前面
    ordered_messages = [messages[i] for i in sorted(range(n), key=lambda i: priorities[i])]
    Bi = 0
    for i in range(n):
        Pi, Ci, Ti = ordered_messages[i]
        Bi = max(ordered_messages[i:], key=lambda x: x[1])[1]
        Qi = Bi
        while True:
            new_Qi = Bi + sum(
                math.ceil((Qi + tau) / Tj) * Cj
                for j, (Pj, Cj, Tj) in enumerate(ordered_messages) if priorities[j] < priorities[i]
            )
            if new_Qi == Qi:
                break
            Qi = new_Qi
        
        Ri = round(Qi + Ci, 2)
        response_times.append(Ri)
    
    return response_times

# 成本函數：計算總的最壞情形響應時間
def cost_function(messages, priorities, tau):
    response_times = compute_response_time(len(messages), tau, messages, priorities)
    return sum(response_times)

# 模擬退火主程式
def simulated_annealing(messages, tau, init_priorities, max_time=15.0):
    best_priorities = init_priorities[:]
    #print("Best solution :", best_priorities)
    best_cost = cost_function(messages, best_priorities, tau)
    current_priorities = best_priorities[:]
    current_cost = best_cost
    
    # 初始溫度
    T0 = 1000.0
    T = T0
    cooling_rate = 0.995
    start_time = time.time()
    
    while time.time() - start_time < max_time:
        # 產生鄰近解：隨機交換兩則訊息的優先權
        i, j = random.sample(range(len(current_priorities)), 2)
        new_priorities = current_priorities[:]
        new_priorities[i], new_priorities[j] = new_priorities[j], new_priorities[i]
        
        # 計算新解的成本
        new_cost = cost_function(messages, new_priorities, tau)
        delta = new_cost - current_cost
        
        # 若成本降低，或者依照一定機率接受成本上升的解
        if delta < 0 or random.random() < math.exp(-delta / T):
            current_priorities = new_priorities
            current_cost = new_cost
            if new_cost < best_cost:
                best_cost = new_cost
                best_priorities = new_priorities[:]
                #print("Best solution :", best_priorities)
        
        # 降溫
        T *= cooling_rate
        # 若溫度極低，則重設初始溫度
        if T < 1e-8:
            T = T0
    
    return best_priorities, best_cost

def main():
    # 讀取 input.dat 檔案
    with open("input.dat") as f:
        lines = f.readlines()

    n = int(lines[0].strip())  # 訊息數
    tau = float(lines[1].strip())  # tau 
    messages = []
    
    # 讀取每條訊息的資料
    for i in lines[2:]:
        Pi, Ci, Ti = map(float, i.strip().split())
        messages.append((int(Pi), Ci, Ti))  # 優先權 Pi、傳輸時間 Ci、週期 Ti

    # 隨機生成初始優先權（不參考原始優先權）
    init_priorities = random.sample(range(n), n)

    # 使用模擬退火進行優化
    best_priorities, best_cost = simulated_annealing(messages, tau, init_priorities)
    
    # 輸出最佳優先權順序
    for p in best_priorities:
        print(p)
    
    # 輸出最佳目標值（總的最壞情形響應時間）
    print(best_cost)

if __name__ == "__main__":
    main()
