import random
import streamlit as st
import math
from gametools import GT

st.title("Luke's Simulated Stock Market")
chart_placeholder = st.empty()
ticker_placeholder = st.empty()
deal_placeholder = st.empty()
market_details = st.empty()
richest_placeholder = st.empty()

market_low = 500
market_high = 0

if "price_history" not in st.session_state:
    st.session_state.price_history = []

starting_buyers = 100

starting_sellers = 20

starting_stocks = 1


order_id_counter = 0

last_price = 0

buyers = {} #id: [name, [stocks], confidence, money, greed, realism]
stocks = {} #id: [name, value, monentum, stability]
sellers = {} #id: [name, [stocks], confidence, money, greed, realism]

order_book = {} #user_id: [buy_or_sell, price, stock_id]

wealth_leaderboard = [] # [type, id, money]

for b in range(0, starting_buyers):
    
    b_id = b
    name = GT.name_gen()
    name = (name[0]+' '+name[1])
    buyers[b_id] = [name, [], random.random(), random.randint(100, 10000), random.random(), random.random()]
    wealth_leaderboard.append(['buyer', b_id, buyers[b_id][3]])
print('Buyers created')


for sto in range(0, starting_stocks):
    starting_value = random.randint(50, 400)
    stocks[sto] = [GT.stock_name_generator(), starting_value, 0, 0]

print('Stocks created')


for se in range(0, starting_sellers):
    s_id = se
    name = GT.name_gen()
    name = (name[0]+' '+name[1])
    number_of_stocks = random.randint(1, 100)

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
    richest_placeholder.info(f"🔔 **Richest Person:** {richest_name} with £{player_money}.")

    while True:
        if random.random() < 0.0005:
            buyer_tick()
        if random.random() < 0.0005:
            seller_tick()
        order_book_tick()

def buyer_tick():
        buyer = random.choice(list(buyers.keys()))
        buyer_list = buyers[buyer]
        confidence = buyer_list[2]
        money = buyer_list[3]
        greed = buyer_list[4]
        realism = buyer_list[5]
        budget = money*(confidence/2)*(1.5-greed)  
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
    confidence = seller_list[2]
    greed = seller_list[4]
    realism = seller_list[5]    
    if not owned_stocks:
        new_id = len(list(buyers.keys()))
        buyers[new_id] = seller_list
        del sellers[seller]
        return
    stock_to_sell = random.choice(owned_stocks)
    price = int(stocks[stock_to_sell][1]*(0.75+greed)*(1.8-confidence)*1+(realism/2))
    add_to_order_book(stock_to_sell, False, price, seller, 0)

def add_to_order_book(stock_id, buying, price, user_id, amount):
    global order_id_counter
    if buying == True:
        buy_or_sell = 'buy'
    else:
        buy_or_sell = 'sell'
    order_book[order_id_counter] = [buy_or_sell, price, stock_id, user_id, amount]
    order_id_counter += 1

#remade by AI (code originate from me)

def order_book_tick():
    all_buyers = [k for k in order_book.keys() if order_book[k][0] == 'buy']
    all_sellers = [k for k in order_book.keys() if order_book[k][0] == 'sell']
    for a in all_buyers:
        # 1. Skip if this buyer order was deleted by a previous match
        if a not in order_book:
            continue
            
        buyer_budget = order_book[a][1]
        buyer_stock_id = order_book[a][2]
        buyer_user_id = order_book[a][3]
        num_of_stocks = order_book[a][4]

        # 2. Find sellers that still exist in the book
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
    #print(f"{buyers[buyer_id][0]} has bought {number_of_stocks} of {stocks[stock_id][0]} stock from {sellers[seller_id][0]} for £{total_price:.2f} (or £{total_price/number_of_stocks:.2f} per stock)")

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
    
    richest_player = wealth_leaderboard[0]
    player_type = richest_player[0]
    player_id = richest_player[1]
    player_money = richest_player[2]    

    if player_type == 'buyer':
        richest_name = buyers[player_id][0]
    else:
        richest_name = sellers[player_id][0]


    if buyer_id in buyers:
        if buyers[buyer_id][3] > wealth_leaderboard[0][2]:
            wealth_leaderboard.append(['buyer', buyer_id, buyers[buyer_id][3]])
            wealth_leaderboard.sort(key=lambda x: x[2], reverse=True)
            richest_placeholder.info(f"**Richest Person:** {richest_name} with £{player_money}.")
    if seller_id in sellers:
        if sellers[seller_id][3] > wealth_leaderboard[0][2]:
            wealth_leaderboard.append(['seller', seller_id, sellers[seller_id][3]])
            wealth_leaderboard.sort(key=lambda x: x[2], reverse=True)
            richest_placeholder.info(f"**Richest Person:** {richest_name} with £{player_money}.")

    if current_unit_price > market_high:
        market_high = current_unit_price
        market_details.info(f"**Market High:** £{market_high}      **Market Low:** £{market_low}")
    elif current_unit_price < market_low:
        market_low = current_unit_price
        market_details.info(f"**Market High:** £{market_high}      **Market Low:** £{market_low}")

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
