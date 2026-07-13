import random

import streamlit as st

import math

from gametools import GT

import time



performance_mode = False

st.title("Luke's Simulated Stock Market")

chart_placeholder = st.empty()

ticker_placeholder = st.empty()

deal_placeholder = st.empty()

market_details = st.empty()

richest_placeholder = st.empty()


max_order_book_length = 500


market_low = 500

market_high = 0


if "price_history" not in st.session_state:
    st.session_state.price_history = []

confidence_capacity = 1

starting_buyers = 100
starting_sellers = 100


starting_stocks = 1

confidence_override = 1


if performance_mode == True:
    starting_buyers = 20
    starting_sellers = 20
    max_order_book_length = 75


order_id_counter = 0

last_price = 0

buyers = {} #id: [name, [stocks], confidence, money, greed, realism]
stocks = {} #id: [name, value, monentum, stability]
sellers = {} #id: [name, [stocks], confidence, money, greed, realism]


order_book = {} #user_id: [buy_or_sell, price, stock_id]


wealth_leaderboard = [] # [type, id, money]

total_stocks = 0

for b in range(0, starting_buyers):

    b_id = b
    name = GT.name_gen()
    name = (name[0]+' '+name[1])
    buyers[b_id] = [name, [], random.random(), random.randint(100, 10000), random.random(), random.random()]
    wealth_leaderboard.append(['buyer', b_id, buyers[b_id][3]])

print('Buyers created')



for sto in range(0, starting_stocks):
    starting_value = 10 # random.randint(50, 400)
    stocks[sto] = [GT.stock_name_generator(), starting_value, 0, 0]


print('Stocks created')



for se in range(0, starting_sellers):
    s_id = se
    name = GT.name_gen()
    name = (name[0]+' '+name[1])
    number_of_stocks = random.randint(1, 100)
    total_stocks+=number_of_stocks
    seller_stocks = []


    for x in range(0, number_of_stocks):
        seller_stocks.append(random.choice(list(stocks.keys())))


    sellers[s_id] = [name, seller_stocks, random.random(), random.randint(100,100000), random.random(), random.random()]
    wealth_leaderboard.append(['seller', s_id, sellers[s_id][3]])

print('Sellers created')


wealth_leaderboard.sort(key=lambda x: x[2], reverse=True) 


def search_seller_stocks(stock_id, number, exclude='-1'):

    available_sellers = []

    valid_sellers_list = [k for k in sellers.keys() if k != exclude]

    for x in valid_sellers_list:

        available_sellers.append(x)

    if available_sellers:

        for x in available_sellers:

            enough_stocks = []

            if sellers[x][1].count(stock_id) >= number:

                enough_stocks.append(x)

        if enough_stocks:

            return enough_stocks

        else:

            return []

    else:

        return []

def stock_loop():
    global confidence_override, confidence_capacity, order_book
    crashing = False
    false_rise = False
    print('Main Loop Began')
    richest_player = wealth_leaderboard[0]
    player_type = richest_player[0]
    player_id = richest_player[1]
    player_money = richest_player[2]
    # Look up their generated name based on their type
    if player_type == 'buyer':
        richest_name = buyers[player_id][0]
    else:
        richest_name = sellers[player_id][0]
    
    # Display it on your website!
    networth = len(buyers[player_id][1])*stocks[0][1]
    richest_placeholder.info(f"**Richest Person:** {richest_name} with £{round(player_money+networth,2)}.")

    while True:
        # Dynamically scan active players to avoid stale data crashes

        if stocks[0][1] <= 15:
            confidence_capacity = random.uniform(1, 1.7)

        richest = wealth_leaderboard[0]
        if richest[0] == 'seller' and richest[1] in sellers:
            richest_stocks = sellers[richest[1]][1]
            player_money = richest[2]
            richest_name = sellers[richest[1]][0] 
            networth = len(richest_stocks)*stocks[0][1]
            richest_placeholder.info(f"**Richest Person:** {richest_name} with £{round(player_money+networth,2)}.")
        elif richest[0] == 'buyer' and richest[1] in buyers:
            richest_stocks = buyers[richest[1]][1]
            player_money = richest[2]
            richest_name = buyers[richest[1]][0] 
            networth = len(richest_stocks)*stocks[0][1]
            richest_placeholder.info(f"**Richest Person:** {richest_name} with £{round(player_money+networth,2)}.")

        if confidence_override >= 3:
            confidence_capacity = 1

        # 2. Separately, let the actual override drift toward that target on every tick
        if confidence_override < confidence_capacity:
            confidence_override += random.uniform(0.01, 0.03)
        elif confidence_override > confidence_capacity:
            confidence_override -= random.uniform(0.01, 0.03)
            if confidence_override < 0:
                confidence_override = 0
        if confidence_capacity-0.1<=confidence_override<=confidence_capacity+0.1 and crashing == True:
            confidence_capacity = 2
            crashing = False
            false_rise = True
        if confidence_capacity-0.1<=confidence_override<=confidence_capacity+0.1 and false_rise == True:
            confidence_capacity = random.uniform(0.2, 0.5)
        richest = wealth_leaderboard[0]

        if random.random() < 0.1:
            buyer_tick()
        if random.random() < 0.1:
            seller_tick()
        order_book_tick()
        if random.random() < 0.00001: 
            confidence_capacity = random.uniform(0.5, 0.6) # Total panic selling
            crashing = True
            st.toast("🚨 MAJOR NEWS EVENT: Market Panic!")
            order_book.clear()
            continue
        if random.random() < 0.00001:
            confidence_capacity = 3
            st.toast("🚨 MAJOR NEWS EVENT: Market excitement!")
            continue
        #print(str(order_book))
        time.sleep(0.01)

def buyer_tick():
        buyer = random.choice(list(buyers.keys()))
        buyer_list = buyers[buyer]
        number_of_stocks = len(buyer_list[1])
        confidence = buyer_list[2]#*confidence_override
        money = buyer_list[3]
        greed = buyer_list[4]
        realism = buyer_list[5]
        budget = money*(confidence/2)*(1.5-greed)*1.5
        available_stocks = [k for k in stocks.keys() if stocks[k][1] <= budget]
        amount = 1
        if number_of_stocks > 10 and random.random() > 0.7:
            new_id = len(list(sellers.keys()))
            sellers[new_id] = buyer_list
            del buyers[buyer]
            return
        if available_stocks:
            if realism <= 0.3:
                chosen_stock = random.choice(list(stocks.keys()))
            else:
                chosen_stock = random.choice(available_stocks)
            stock_price = stocks[chosen_stock][1]
            price = 0
            if stock_price*1.2 < budget:
                price = math.trunc(stock_price*random.uniform(0.9, 1.2))
            elif stock_price <= budget:
                price = math.trunc(stock_price*random.uniform(0.9, 1.1))
            elif stock_price > budget:
                price = budget
            else:
                price = stock_price

            if price < 6:
                price = 6


            price *= ((1-greed)/5)+0.8

            if budget // stock_price > 1:
                amount = math.trunc(budget // stock_price)
            if amount == 0:
                amount = 1
            add_to_order_book(chosen_stock, True, price, buyer, amount)

def seller_tick():
    seller = random.choice(list(sellers.keys()))
    seller_list = sellers[seller]
    owned_stocks = seller_list[1]
    confidence = seller_list[2] *confidence_override
    greed = seller_list[4]
    realism = seller_list[5]    
    demand_modifier = len(buyers)/len(sellers)
    if not owned_stocks:
        new_id = len(list(buyers.keys()))
        buyers[new_id] = seller_list
        del sellers[seller]
        return
    stock_to_sell = random.choice(owned_stocks)
    seller_modifier = ((((greed+confidence+(1-realism))/15)+1)*confidence_override)*demand_modifier
    if stocks[stock_to_sell][1] < 30:
        seller_modifier = ((((confidence)+(1-realism))/15)+1)*1.3
    price = int(stocks[stock_to_sell][1]*seller_modifier)*random.uniform(0.9, 1.1)
    floor = 2
    if price < floor:
        price = floor
    add_to_order_book(stock_to_sell, False, price, seller, 0)

def add_to_order_book(stock_id, buying, price, user_id, amount):
    global order_id_counter
    if buying == True:
        buy_or_sell = 'buy'
    else:
        buy_or_sell = 'sell'
    order_book[order_id_counter] = [buy_or_sell, price, stock_id, user_id, amount]
    order_id_counter += 1
    if len(order_book) > max_order_book_length:
        oldest_order_id = next(iter(order_book))
        del order_book[oldest_order_id]

def order_book_tick():
    all_buyers = [k for k in order_book.keys() if order_book[k][0] == 'buy']
    all_sellers = [k for k in order_book.keys() if order_book[k][0] == 'sell']
    deal_done = False
    for a in all_buyers:
        if a not in order_book:
            continue
            
        buyer_budget = order_book[a][1]
        buyer_stock_id = order_book[a][2]
        buyer_user_id = order_book[a][3]
        num_of_stocks = order_book[a][4]

        valid_sellers = [
            k for k in all_sellers
            if k in order_book 
            and order_book[k][2] == buyer_stock_id
            and order_book[k][1] <= buyer_budget
            and order_book[k][3] != buyer_user_id
        ]

        if valid_sellers:
            best_price = -1
            best_seller_order_id = None

            # 3. Find the cheapest seller
            for v in valid_sellers:
                if best_price == -1 or order_book[v][1] < best_price:
                    best_price = order_book[v][1]
                    best_seller_order_id = v

            if best_seller_order_id is not None:
                seller_user_id = order_book[best_seller_order_id][3]
            
                if seller_user_id in sellers and buyer_user_id in buyers:
                    # 4. Process the transaction once
                    if sellers[seller_user_id][1].count(buyer_stock_id) >= num_of_stocks:
                        purchase_from_single(seller_user_id, buyer_user_id, buyer_stock_id, best_price*num_of_stocks, num_of_stocks)
                    else:
                        count = sellers[seller_user_id][1].count(buyer_stock_id)
                        purchase_from_single(seller_user_id, buyer_user_id, buyer_stock_id, best_price*count, count)
                
                # 5. Cleanly wipe both complete orders out of the book
                if a in order_book:
                    del order_book[a]
                if best_seller_order_id in order_book:
                    del order_book[best_seller_order_id]
                deal_done = True
        if deal_done == False:
            for x in stocks:
                stocks[x][1] = find_highest_bid(x)[0]

def find_highest_bid(stock_id):
    highest_bid = -1
    highest_bidder = None
    for x in order_book:
        if order_book[x][0] == 'buy' and order_book[x][2] == stock_id:
            if order_book[x][1] > highest_bid:
                highest_bid = order_book[x][1]
                highest_bidder = order_book[x][3]
    return [highest_bid, highest_bidder]

def purchase_from_single(seller_id, buyer_id, stock_id, total_price, number_of_stocks):
    global last_price, market_low, market_high
    buyers[buyer_id][3] -= total_price
    sellers[seller_id][3] += total_price
    new_stocks = []
    for x in range(0, number_of_stocks):
        seller_stocks_ = sellers[seller_id][1]
        seller_stocks_.remove(stock_id)
        sellers[seller_id][1] = seller_stocks_

    for x in range(0, number_of_stocks):
        new_stocks.append(stock_id)

    buyers[buyer_id][1] = new_stocks
    stocks[stock_id][1] = total_price/number_of_stocks
    print(f"{buyers[buyer_id][0]} has bought {number_of_stocks} of {stocks[stock_id][0]} stock from {sellers[seller_id][0]} for £{total_price:.2f} (or £{total_price/number_of_stocks:.2f} per stock)")

    # 1. Get the stock name and formatted price
    stock_name = stocks[stock_id][0]
    current_unit_price = total_price / number_of_stocks
    
    # 2. Update the subtitle placeholder live!
    # This stays exactly how it was—it will naturally render below the chart now!
    if total_price/number_of_stocks > last_price:
        arrow = "▲"
    elif total_price/number_of_stocks < last_price:
        arrow = '▼'
    else:
        arrow = '~'
    last_price = total_price/number_of_stocks
    ticker_placeholder.metric(label=stock_name, value=f"£{current_unit_price:.2f} {arrow}")
    chart_placeholder.line_chart(
        st.session_state.price_history,
        x_label="Time (Weeks)",
        y_label="Price (£)"
    )
    buyer_name = buyers[buyer_id][0]
    deal_placeholder.info(
        f"**Latest Deal:** {buyer_name} bought {number_of_stocks} share(s) for a total of £{total_price:.2f}."
    )
    current_unit_price = total_price / number_of_stocks
    st.session_state.price_history.append(current_unit_price)

    if len(st.session_state.price_history) > 500:
        st.session_state.price_history.pop(0)

    if sellers[seller_id][1] == []:
        new_id = len(list(buyers.keys()))
        buyers[new_id] = sellers[seller_id]
        del sellers[seller_id]
    
    # 1. Safely pull the top leaderboard spot
    richest_player = wealth_leaderboard[0]
    player_type = richest_player[0]
    player_id = richest_player[1]
    player_money = richest_player[2]    
    
    richest_name = "Unknown"
    # STRICT CHECK: Verify the ID exists in the CORRECT dictionary matching its type
    if player_type == 'buyer' and player_id in buyers:
        richest_name = buyers[player_id][0]
    elif player_type == 'seller' and player_id in sellers:
        richest_name = sellers[player_id][0]
    
    # 2. Only update the leaderboard if the transacting players broke the record
    if buyer_id in buyers and buyers[buyer_id][3] > wealth_leaderboard[0][2]:
        networth = len(buyers[player_id][1])*stocks[0][1]
        wealth_leaderboard.append(['buyer', buyer_id, buyers[buyer_id][3]])
        wealth_leaderboard.sort(key=lambda x: x[2], reverse=True)
        richest_placeholder.info(f"**Richest Person:** {richest_name} with £{round(player_money+networth,2)}.")
        
    elif seller_id in sellers and sellers[seller_id][3] > wealth_leaderboard[0][2]:
        networth = len(sellers[player_id][1])*stocks[0][1]
        wealth_leaderboard.append(['seller', seller_id, sellers[seller_id][3]])
        wealth_leaderboard.sort(key=lambda x: x[2], reverse=True)
        richest_placeholder.info(f"**Richest Person:** {richest_name} with £{round(player_money+networth,2)}.")
    
    if len(wealth_leaderboard) > 20:
        players_to_remove = len(wealth_leaderboard) - 20
        for x in range(0, players_to_remove):
            wealth_leaderboard.pop(20)

    if current_unit_price > market_high:
        market_high = current_unit_price
        market_details.info(f"**Market High:** £{round(market_high,2)}      **Market Low:** £{round(market_low,2)}")
    elif current_unit_price < market_low:
        market_low = current_unit_price
        market_details.info(f"**Market High:** £{round(market_high,2)}      **Market Low:** £{round(market_low,2)}")

def connect_best_seller(sellers_ids, stock_id):
    best_price = -1
    best_vendor = None
    stock_price = stocks[stock_id][1]
    stock_momentum = stocks[stock_id][2]

    for x in sellers_ids:
        seller_greed = sellers[x][4]
        price = stock_price*(1-(stock_momentum/2))*(1+(seller_greed/2))
        if best_price == -1 or best_price > price:
            best_price = price
            best_vendor = x

    return [best_vendor, best_price]


if "running" not in st.session_state:
    st.session_state.running = False

# 2. If the simulation HAS NOT started, show the button
if not st.session_state.running:
    if st.button("Start Simulation"):
        st.session_state.running = True  # Flip the switch to True
        st.rerun()  # Instantly refresh the page to hide the button

# 3. If the simulation HAS started, run the loop forever
else:
    # Optional: Add a little text indicator where the button used to be
    st.caption("🟢 Market is live and trading...")
    stock_loop()
