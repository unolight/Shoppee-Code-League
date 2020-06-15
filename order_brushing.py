from collections import defaultdict
from datetime import datetime, timedelta
import os


class Order:
  def __init__(self, orderid, user, time):
    self.id = orderid
    self.user = user
    self.time = time

  def __repr__(self):
    return '({},{})'.format(self.user,self.time)

  def __str__(self):
    return '({},{})'.format(self.user,self.time)


# ================ Read ======================= 
data = []
with open('order_brush_order.csv', 'r') as f:
  for line in f:
    data.append(line.strip().split(','))


# ================== Preprocessing ============================

# orderid,shopid,userid,event_time

data = data[1:]
shop_ids = []
shops = defaultdict(list)

for d in data:
  orderid = int(d[0])
  shopid = int(d[1])
  user = int(d[2])
  time = datetime.strptime(d[3], '%Y-%m-%d %H:%M:%S').timestamp()
  shops[shopid].append(Order(orderid, user,time))
  shop_ids.append(shopid)

shop_ids = sorted(set(shop_ids))


# ========================== Main ===============================
ans = defaultdict(set)
ONE_HOUR=3600
for shop, v in shops.items():
  print(shop)
  orders=sorted(v, key=lambda o: o.time)
  k=0
  user_orders = defaultdict(int)
  total_orders = 0
  window = []
  time_seq = []
  cand = set()
  while k<len(orders):
    current_time=orders[k].time

    while len(time_seq)>0 and time_seq[0]+ONE_HOUR<current_time:
      if total_orders>=3*len(user_orders):
        for w in window:
          cand.update(w)
          
      time_seq.pop(0)
      w = window.pop(0)
      for o in w:
        user_orders[o.user]-=1
        total_orders-=1
        if user_orders[o.user]<=0:
          del user_orders[o.user]

    if total_orders>=3*len(user_orders):
      for w in window:
        cand.update(w)

    current_orders = []
    while k<len(orders) and orders[k].time==current_time:
      current_orders.append(orders[k])
      k+=1


    for o in current_orders:
      user_orders[o.user]+=1
      total_orders+=1

    window.append(current_orders)
    time_seq.append(current_time)

  while len(time_seq):
    if total_orders>=3*len(user_orders):
      for w in window:
        cand.update(w)
    time_seq.pop(0)
    w = window.pop(0)
    for o in w:
      user_orders[o.user]-=1
      total_orders-=1
      if user_orders[o.user]<=0:
        del user_orders[o.user]


  cnt = defaultdict(int)
  for o in cand:
    cnt[o.user]+=1

  mx=0
  for u,c in cnt.items():
    mx=max(mx,c)

  for u,c in cnt.items():
    if mx==c:
      ans[shop].add(u)

  if len(ans[shop]) == 0:
    ans[shop].add(0)


# ============ Write Output ====================
with open('out.csv', 'w') as f:
  f.write('shopid,userid\n')
  for s in shop_ids:
      v=ans[s]
      v=sorted(v)
      x = '&'.join(list(map(str,v)))
      f.write('{},{}\n'.format(s,x))
