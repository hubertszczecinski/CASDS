# CASDS | zadanie: codenet_p01116 | trudność: medium
#
# # ML Competency Optimization for Project Delivery
#
# To excel as an AI Engineer, a diverse set of technical competencies is required. Each
# competency contributes to the overall System Performance Score (SPS), and these skills
# possess varying levels of strategic importance. The total SPS is calculated by summing
# the products of a module's proficiency level and its assigned importance degree.
#
# Your team is undergoing an intensive upskilling program focused on critical technologies
# (e.g., TensorFlow, NLP, Data Engineering). The organization offers modules covering
# various technical domains. Investing in a module increases the team's proficiency level
# proportionally to the allocated training budget (one level per unit of investment).
# However, each technical module has a defined maximum proficiency cap; further spending
# on an already saturated skill yields no additional benefit.
#
# Crucially, these technical skills are interdependent: to enroll in an advanced module, a
# minimum proficiency level must first be achieved in its prerequisite foundational skill.
# Your objective is to maximize the total System Performance Score within a strict,
# limited resource allocation budget.
#
# ## Wejście
#
# The input consists of no more than 100 datasets, each in the following format.
#
# n k
#
# h 1  ... h n
#
# s 1  ... s n
#
# p 2  ... p n
#
# l 2  ... l n
#
# The first line has two integers,
# n, the number of different skills between 2 and 100, inclusive, and
# k, the budget amount available between 1 and 10 5 , inclusive.
# In what follows, skills are numbered 1 through n.
#
# The second line has n integers
# h 1 ...h n ,
# in which h i  is the maximum level of the skill i,
# between 1 and 10 5 , inclusive.
#
# The third line has n integers
# s 1 ...s n ,
# in which s i  is the importance degree of the skill i,
# between 1 and 10 9 , inclusive.
#
# The fourth line has n−1 integers
# p 2 ...p n ,
# in which p i  is the prerequisite skill of the skill i,
# between 1 and i−1, inclusive.
# The skill 1 has no prerequisites.
#
# The fifth line has n−1 integers
# l 2 ...l n ,
# in which l i  is the least level of prerequisite skill
# p i  required to learn the skill i,
# between 1 and h p i   , inclusive.
#
# The end of the input is indicated by a line containing two zeros.
#
# ## Wyjście
#
# For each dataset, output a single line containing one integer,
# which is the highest programming competence measure achievable,
# that is,
# the maximum sum of the products of
# levels and importance degrees of the skills,
# within the given tuition budget,
# starting with level zero for all the skills.
# You do not have to use up all the budget.
#
# ## Przykład 1
#
# Wejście:
#
# 3 10
# 5 4 3
# 1 2 3
# 1 2
# 5 2
# 5 40
# 10 10 10 10 8
# 1 2 3 4 5
# 1 1 2 3
# 10 10 10 10
# 5 10
# 2 2 2 5 2
# 2 2 2 5 2
# 1 1 2 2
# 2 1 2 1
# 0 0
#
# Wyjście:
#
# 18
# 108
# 35
#
# Czytaj dane ze standardowego wejścia (stdin) i wypisz wynik na standardowe wyjście (stdout).

import sys

# Prealokacja tablic, aby uniknąć problemów z czasem i pamięcią 
# (K <= 100 000, max liczba bloków M <= 2 * 100 = 200).
MAX_M = 205
MAX_K = 100005
dp = [[0] * MAX_K for _ in range(MAX_M)]
q = [0] * MAX_K

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    iterator = iter(input_data)
    
    while True:
        try:
            n_str = next(iterator)
            k_str = next(iterator)
        except StopIteration:
            break
            
        n = int(n_str)
        k = int(k_str)
        
        if n == 0 and k == 0:
            break
            
        h = [0] + [int(next(iterator)) for _ in range(n)]
        s = [0] + [int(next(iterator)) for _ in range(n)]
        
        if n > 1:
            p = [0, 0] + [int(next(iterator)) for _ in range(n - 1)]
            l = [0, 0] + [int(next(iterator)) for _ in range(n - 1)]
        else:
            p = []
            l = []
            
        children_of = [[] for _ in range(n + 1)]
        for i in range(2, n + 1):
            children_of[p[i]].append(i)
            
        blocks = []
        block_by_end = {}
        
        for u in range(1, n + 1):
            # Zbieramy wszystkie momenty (poziomy), gdzie coś się odblokowuje dla węzła `u`
            req_set = {0, h[u]}
            for v in children_of[u]:
                req_set.add(l[v])
            reqs = sorted(list(req_set))
            
            # Tworzymy oddzielne bloki dla każdego przedziału
            for j in range(1, len(reqs)):
                cap = reqs[j] - reqs[j-1]
                val = s[u]
                end_lvl = reqs[j]
                
                b_idx = len(blocks)
                block = {
                    'id': b_idx,
                    'u': u,
                    'cap': cap,
                    'val': val,
                    'end_lvl': end_lvl,
                    'children': []
                }
                blocks.append(block)
                block_by_end[(u, end_lvl)] = b_idx
                
                # Zależności w grafie (drzewie bloków)
                if j == 1:
                    if u > 1:
                        p_u = p[u]
                        req_lvl = l[u]
                        parent_idx = block_by_end[(p_u, req_lvl)]
                        blocks[parent_idx]['children'].append(b_idx)
                else:
                    parent_idx = b_idx - 1
                    blocks[parent_idx]['children'].append(b_idx)
                    
        # Spłaszczanie drzewa - DFS po blokach
        preorder = []
        size = [0] * len(blocks)
        
        def dfs(idx):
            preorder.append(idx)
            s_nodes = 1
            for child in blocks[idx]['children']:
                s_nodes += dfs(child)
            size[idx] = s_nodes
            return s_nodes
            
        if len(blocks) > 0:
            dfs(0)
            
        M = len(preorder)
        preorder_blocks = [blocks[idx] for idx in preorder]
        preorder_size = [0] * M
        for new_idx, old_idx in enumerate(preorder):
            preorder_size[new_idx] = size[old_idx]
            
        # Sufiksowe sumy pojemności bloków - znacznie przyspieszają działanie
        suf_cap = [0] * (M + 1)
        for i in range(M - 1, -1, -1):
            suf_cap[i] = suf_cap[i+1] + preorder_blocks[i]['cap']
            
        for b in range(k + 1):
            dp[M][b] = 0
            
        # Programowanie dynamiczne na drzewie rozszerzone o kolejkę monotoniczną
        for i in range(M - 1, -1, -1):
            blk = preorder_blocks[i]
            cap = blk['cap']
            val = blk['val']
            next_n = i + preorder_size[i]
            
            A = dp[next_n]
            B = dp[i + 1]
            dp_i = dp[i]
            cap_val = cap * val
            
            # Wystarczy przeliczyć DP tylko do maksymalnej przydatnej pojemności
            limit = min(k, suf_cap[i])
            
            D = [A[j] - j * val for j in range(limit + 1)]
            
            head = 0
            tail = 0
            
            for b in range(limit + 1):
                Db = D[b]
                while tail > head and D[q[tail - 1]] <= Db:
                    tail -= 1
                q[tail] = b
                tail += 1
                
                if q[head] < b - cap:
                    head += 1
                    
                v1 = b * val + D[q[head]]
                v2 = cap_val + B[b - cap] if b >= cap else -1
                
                # Wybieramy lepszy scenariusz: pominąć dzieci (v1) lub wziąć węzeł całkowicie (v2)
                if v1 > v2:
                    dp_i[b] = v1
                else:
                    dp_i[b] = v2
                    
            # Padding reszty wyników maksymalną wartością
            max_val = dp_i[limit]
            for b in range(limit + 1, k + 1):
                dp_i[b] = max_val
                
        print(dp[0][k])

if __name__ == "__main__":
    sys.setrecursionlimit(2000)
    main()


