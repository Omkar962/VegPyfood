import datetime
import simplejson as json


def generate_order_number(pk):
    curr_datetime=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    order_number=curr_datetime+str(pk)
    return order_number

def order_total_by_vendor(order,vendor_id):
    total_Data=json.loads(order.total_data)
    data=total_Data.get(str(vendor_id))
    subtotal=0
    tax=0
    tax_dict={}

    for key,val in data.items():
        subtotal+=float(key)
        val=val.replace("'",'"')
        val=json.loads(val)
        tax_dict.update(val)

        for i in val:
            for j in val[i]:
                tax+=float(val[i][j])
    total=float(subtotal)+float(tax)

    context={
        'subtotal':subtotal,
        'tax_dict':tax_dict,
        'total':total
    }

    return context
