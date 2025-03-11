import math

def compute_response_time(n, tau, messages):
    response_times = []
    
    messages.sort()
    Bi = 0

    for i in range(n):
        Pi, Ci, Ti = messages[i]  # 取出訊息參數
        
        Bi = max(messages[i:], key=lambda x: x[1])[1]
        Qi = Bi  
        while True:
            new_Qi = Bi + sum(
                math.ceil((Qi + tau) / Tj) * Cj
                for Pj, Cj, Tj in messages if Pj < Pi  # 只計算優先級較高的訊息
            )
            if new_Qi == Qi:  # 收斂條件
                break
            Qi = new_Qi  # 更新 Qi
        
        Ri = round(Qi + Ci, 2)
        response_times.append(Ri)
    
    return response_times

# 讀取 input.dat 並解析
messages = []
with open("input.dat") as f:
    lines = f.readlines()

n = int(lines[0].strip())  
tau = float(lines[1].strip()) 
for i in lines[2:]:
    Pi, Ci, Ti = map(float, i.strip().split())
    messages.append((int(Pi), Ci, Ti))

# 計算並輸出結果
result = compute_response_time(int(n), tau, messages)
for r in result:
    print(r)
