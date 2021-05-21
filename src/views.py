from django.shortcuts import render
import razorpay
from .models import donate
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def index(request):
    return render(request,"index.html")
def home(request):
    if request.method == "POST":
        name=request.POST.get("name")
        amount=request.POST.get("amount")
        email=request.POST.get("email")
        print(name)
        print(amount)
        client=razorpay.Client(auth=("rzp_test_eNtGkZQDLi2LXf","YS3EQzKJ9lxvlWklvGdAcLko"))
        payment=client.order.create({'amount':amount,'currency':'INR','payment_capture':'1'})
        print(payment)
        Donate=donate(name=name,amount=amount,email=email,payment_id=payment['id'])
        Donate.save()
        return render(request,"pay.html",{'payment':payment})

    return render(request,"pay.html")

@csrf_exempt
def success(request):
    if request.method == "POST":
        a=request.POST
        print(a)
        order_id=""
        for key,val in a.items():
            if key=='razorpay_order_id':
                order_id=val
                break

        user=donate.objects.filter(payment_id=order_id).first()
        user.paid=True
        user.save()

        msg_plain=render_to_string("email.txt")
        msg_html=render_to_string("email.html")
        send_mail("Your donation is successful ",msg_plain, settings.EMAIL_HOST_USER,
                  ['aieshaf08@gmail.com'],html_message=msg_html
                  )
    return render(request,"success.html")