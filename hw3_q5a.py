#!/usr/bin/env python3
import hashlib,sys
K=16; N=1<<K
def h_user_k(x,userid,k=K):
    m=hashlib.sha256(); m.update(userid.encode('utf-8')); m.update(x.to_bytes(2,'big'))
    return int.from_bytes(m.digest(),'big') & ((1<<k)-1)
def build_graph(userid):
    f=[0]*N; indeg=[0]*N
    for u in range(N):
        v=h_user_k(u,userid); f[u]=v; indeg[v]+=1
    return f,indeg
def stats(userid):
    f,indeg=build_graph(userid)
    seen=[0]*N; tails=[]; cyc_lens=[]
    for t in [u for u in range(N) if indeg[u]==0]:
        u=t; path={}
        while seen[u]==0:
            path[u]=len(path); seen[u]=1; u=f[u]
        if u in path:
            cyc=len(path)-path[u]; tail=path[u]
            tails.append(tail); cyc_lens.append(cyc)
        for v in path: seen[v]=2
    for s in range(N):
        if seen[s]!=0: continue
        u=s; path={}
        while seen[u]==0:
            path[u]=len(path); seen[u]=1; u=f[u]
        if u in path:
            cyc=len(path)-path[u]; cyc_lens.append(cyc)
        for v in path: seen[v]=2
    components=len(cyc_lens)
    avg_tail=(sum(tails)/len(tails)) if tails else 0.0
    max_tail=max(tails) if tails else 0
    min_cycle=min(cyc_lens) if cyc_lens else 0
    avg_cycle=(sum(cyc_lens)/len(cyc_lens)) if cyc_lens else 0.0
    max_cycle=max(cyc_lens) if cyc_lens else 0
    return components,avg_tail,max_tail,min_cycle,avg_cycle,max_cycle
if __name__=="__main__":
    if len(sys.argv)<2:
        print("usage: python3 hw3_q5a.py <userid>"); sys.exit(1)
    userid=sys.argv[1]
    c,at,mt,mnc,avc,mxc=stats(userid)
    print(f"{c} {at:.6f} {mt} {mnc} {avc:.6f} {mxc}")