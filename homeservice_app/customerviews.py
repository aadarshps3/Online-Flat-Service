from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from homeservice_app.forms import FeedbackForm, PayBillForm
from homeservice_app.models import Worker, Schedule, Customers, Appointment, Feedback, Bill, CreditCard


@login_required(login_url='login_view')
def customer_home(request):
    return render(request, 'customertemp/customer_home.html')


@login_required(login_url='login_view')
def view_workers_customer(request):
    data = Worker.objects.all()
    return render(request, 'customertemp/workers.html', {'data': data})


@login_required(login_url='login_view')
def view_schedule_customer(request):
    s = Schedule.objects.all()
    context = {
        'schedule': s
    }
    return render(request, 'customertemp/schedule_view.html', context)


@login_required(login_url='login_view')
def take_appointment(request, id):
    s = Schedule.objects.get(id=id)  # Fetch the schedule
    c = Customers.objects.get(user=request.user)  # Fetch the customer
    appointment = Appointment.objects.filter(user=c, schedule=s)
    
    if appointment.exists():
        messages.info(request, 'You Have Already Requested Appointment for this Schedule')
        return redirect('view_schedule')

    if request.method == 'POST':
        obj = Appointment()
        obj.user = c
        obj.schedule = s
        obj.user2 = s.employee  # Assuming Schedule has a ForeignKey to Worker
        obj.save()
        messages.info(request, 'Appointment Booked Successfully')
        return redirect('appointment_view')

    return render(request, 'customertemp/take_appointment.html', {'schedule': s})


@login_required(login_url='login_view')
def appointment_view(request):
    c = Customers.objects.get(user=request.user)
    a = Appointment.objects.filter(user=c)
    return render(request, 'customertemp/appointment_view.html', {'appointment': a})


@login_required(login_url='login_view')
def Feedback_add_user(request):
    form = FeedbackForm()
    u = request.user
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            messages.info(request, 'Complaint Registered Successfully')
            return redirect('Feedback_view_user')
    return render(request, 'customertemp/complaint_add.html', {'form': form})


@login_required(login_url='login_view')
def Feedback_view_user(request):
    f = Feedback.objects.filter(user=request.user)
    return render(request, 'customertemp/complaint_view.html', {'feedback': f})


def view_bill_user(request):
    u = Customers.objects.get(user=request.user)
    print(u)
    bill = Bill.objects.filter(name=u)
    print(bill)
    return render(request, 'customertemp/view_bill_user.html', {'bills': bill})


def pay_bill(request, id):
    bi = Bill.objects.get(id=id)
    # form = PayBillForm()
    if request.method == 'POST':
        card = request.POST.get('card')
        c = request.POST.get('cvv')
        da = request.POST.get('exp')
        CreditCard(card_no=card, card_cvv=c, expiry_date=da).save()
        bi.status = 1
        bi.save()
        messages.info(request, 'Bill Paid  Successfully')
        return redirect('bill_history')

        # form = PayBillForm(request.POST)
        # if form.is_valid():
        #     pay = form.save(commit=False)
        #     pay.bill = bi
        #     pay.save()
        #     bi.status = 1
        #     bi.save()

    return render(request, 'customertemp/pay_bill.html', )


def pay_in_direct(request, id):
    bi = Bill.objects.get(id=id)
    bi.status = 2
    bi.save()
    messages.info(request, 'Choosed to Pay Fee Direct in office')
    return redirect('bill_history')


def bill_history(request):
    u = Customers.objects.get(user=request.user)
    bill = Bill.objects.filter(name=u, status__in=[1, 2])

    return render(request, 'customertemp/view_bill_history.html', {'bills': bill})
