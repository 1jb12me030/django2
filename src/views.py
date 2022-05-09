from locale import currency
from urllib import response
from xmlrpc import client
from django.shortcuts import render
from src.forms import CoffeepaymentForm
import razorpay
from src.models import Coffee

# Create your views here.
def coffee_payment(request):
    if request.method == 'POST':
        name=request.POST.get('name')
        amount=int(request.POST.get('amount'))*100
        
        client=razorpay.Client(auth=('rzp_test_KyE94QtJ4p1DAV','wYof3oVUxFNX8Mkbtti9HUQK'))
        response_payment=client.order.create(dict(amount=amount,currency='INR'))
        order_id = response_payment['id']
        order_status=response_payment['status']
        
        if order_status=='created':
            coffee=Coffee(
                
                name=name,
                amount=amount,
                order_id=order_id
            )
            
            coffee.save()
            response_payment['name'] = name
            form=CoffeepaymentForm(request.POST or None)
            return render(request, 'Coffee_payment.html', {'form':form, 'payment':response_payment })
        
        #print(response_payment)
    form=CoffeepaymentForm()
    return render(request, 'coffee_payment.html',{'form':form})
def payment_status(request):
    response=request.POST
    params_dict = {
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature']
        
    }
    
    client=razorpay.Client(auth=('rzp_test_KyE94QtJ4p1DAV','wYof3oVUxFNX8Mkbtti9HUQK'))
    
    try:
        status=client.utility.verify_payment_signature(params_dict)
        coffee=Coffee.objects.get(order_id=response['razorpay_order_id'])
        coffee.razorpay_payment_id=response['razorpay_payment_id']
        coffee.paid=True
        coffee.save()
        return render(request, 'payment_status.html',{'status':True})
    except:
        return render(request,'payment_status.html',{'status':False})
