import random

import sys

import time

from pathlib import Path

import streamlit as st

import math

current_dir = Path(__file__).resolve().parent

parent_dir = current_dir.parent

if str(parent_dir) not in sys.path:

    sys.path.append(str(parent_dir))


from gametools import GT

st.title("Luke's Stock Market")
chart_placeholder = st.empty()

if "price_history" not in st.session_state:
    st.session_state.price_history = []

starting_buyers = 1000

starting_sellers = 200

starting_stocks = 1


order_id_counter = 0


buyers = {} #id: [name, [stocks], confidence, money, greed, realism]

stocks = {} #id: [name, value, monentum, stability]

sellers = {} #id: [name, [stocks], confidence, money, greed, realism]


order_book = {} #user_id: [buy_or_sell, price, stock_id]


for b in range(0, starting_buyers):
    b_id = b
    name = GT.name_gen()
    name = (name[0], name[1])
    buyers[b_id] = [name, [], random.random(), random.randint(100, 10000), random.random(), random.random()]

print('Buyers created')


for sto in range(0, starting_stocks):
    starting_value = random.randint(1, 100)
    stocks[sto] = [GT.stock_name_generator(), starting_value, 0, 0]

print('Stocks created')


for se in range(0, starting_sellers):
    s_id = se
    name = GT.name_gen()
    name = (name[0], name[1])
    number_of_stocks = random.randint(1, 100)

    seller_stocks = []

    for x in range(0, number_of_stocks):

        seller_stocks.append(random.choice(list(stocks.keys())))

    sellers[s_id] = [name, seller_stocks, random.random(), random.randint(100,100000), random.random(), random.random()]

print('Sellers created')


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
    while True:
        if random.random() < 0.0001:
            buyer_tick()
        if random.random() < 0.0001:
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
        if available_stocks:
            if realism <= 0.3:
                chosen_stock = random.choice(list(stocks.keys()))
            else:
                chosen_stock = random.choice(available_stocks)
            stock_price = stocks[chosen_stock][1]
            price = 0
            if stock_price*1.2 < budget:
                price = math.trunc(stock_price*random.uniform(1, 1.3))
            elif stock_price <= budget:
                price = math.trunc(stock_price*random.uniform(0.9, 1.1))
            elif stock_price > budget:
                price = budget
            else:
                price = stock_price
            add_to_order_book(chosen_stock, True, price, buyer)

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
    add_to_order_book(stock_to_sell, False, price, seller)

def add_to_order_book(stock_id, buying, price, user_id):
    global order_id_counter
    if buying == True:
        buy_or_sell = 'buy'
    else:
        buy_or_sell = 'sell'
    order_book[order_id_counter] = [buy_or_sell, price, stock_id, user_id]
    order_id_counter += 1

#remade by AI (code originate from me)

def order_book_tick():

    all_buyers = [k for k in order_book.keys() if order_book[k][0] == 'buy']

    all_sellers = [k for k in order_book.keys() if order_book[k][0] == 'sell']

   

    for a in all_buyers:

        buyer_budget = order_book[a][1]

        buyer_stock_id = order_book[a][2]

        buyer_user_id = order_book[a][3]


        valid_sellers = [

            k for k in all_sellers

            if order_book[k][2] == buyer_stock_id

            and order_book[k][1] <= buyer_budget

            and order_book[k][3] != buyer_user_id

        ]

       

        if valid_sellers:

            best_price = -1

            best_seller_order_id = None

           

            for v in valid_sellers:

                if best_price == -1 or order_book[v][1] < best_price:

                    best_price = order_book[v][1]

                    best_seller_order_id = v


            seller_user_id = order_book[best_seller_order_id][3]

           

            if seller_user_id in sellers:
                purchase_from_single(seller_user_id, buyer_user_id, buyer_stock_id, best_price, 1)


            del order_book[a]

            del order_book[best_seller_order_id]


            break

def purchase_from_single(seller_id, buyer_id, stock_id, total_price, number_of_stocks):

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

    current_unit_price = total_price / number_of_stocks
    st.session_state.price_history.append(current_unit_price)

    if len(st.session_state.price_history) > 500:
        st.session_state.price_history.pop(0)

    chart_placeholder.line_chart(st.session_state.price_history)

    if sellers[seller_id][1] == []:

        new_id = len(list(buyers.keys()))

        buyers[new_id] = sellers[seller_id]

        del sellers[seller_id]


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


# Replace your lone stock_loop() call with this:
if st.button("Start Simulation"):
    stock_loop()
