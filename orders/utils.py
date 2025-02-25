import datetime

def generate_order_number(pk):
    curr_datetime=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    order_number=curr_datetime+str(pk)
    return order_number