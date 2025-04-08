from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from homeservice_app.forms import SchdeuleForm
from homeservice_app.models import Schedule, Bill, Customers, Appointment,Worker


@login_required(login_url='login_view')
def worker_home(request):
    return render(request, 'workertemp/worker_home.html')


@login_required(login_url='login_view')
def schedule_add(request):
    form = SchdeuleForm()
    if request.method == 'POST':
        form = SchdeuleForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.employee = Worker.objects.get(user=request.user)
            form.save()
            messages.info(request, 'schedule added successful')
            return redirect('schedule_views')
    return render(request, 'workertemp/schedule_add.html', {'form': form})


@login_required(login_url='login_view')
def schedule_view(request):
    worker = Worker.objects.get(user=request.user)
    print(worker)
    s = Schedule.objects.filter(employee=worker)
    print(s)
    context = {
        'schedule': s
    }
    return render(request, 'workertemp/schedule_view.html', context)


@login_required(login_url='login_view')
def schedule_update(request, id):
    s = Schedule.objects.get(id=id)
    if request.method == 'POST':
        form = SchdeuleForm(request.POST or None, instance=s)
        if form.is_valid():
            form.save()
            messages.info(request, 'schdeule updated')
            return redirect('schedule_views')
    else:
        form = SchdeuleForm(instance=s)
    return render(request, 'workertemp/schedule_update.html', {'form': form})


@login_required(login_url='login_view')
def schedule_delete(request, id):
    s = Schedule.objects.filter(id=id)
    if request.method == 'POST':
        s.delete()
        return redirect('schedule_views')

def view_bill_worker(request):
    bill = Bill.objects.all()
    print(bill)
    return render(request, 'workertemp/view_payment_details.html', {'bills': bill})

# @login_required(login_url='login_view')
# def appointment_view_worker(request):
#     user = request.user
#     print(user)
#     worker = Worker.objects.get(user=user)
#     print(worker,"worker")
#     data=Schedule.objects.filter(employee=worker)
#     print(data)
#     return render(request, 'workertemp/appointment_view.html', {'data': data})

@login_required(login_url='login_view')
def appointment_view_worker(request):
    user = request.user
    worker = Worker.objects.get(user=user)
    
    # Fetching schedules with related appointments
    data = Schedule.objects.filter(employee=worker).prefetch_related('appointment_set')
    print(data,"data")
    
    appointments = []
    for schedule in data:
        appointment = Appointment.objects.filter(schedule=schedule).first()  # Assuming one appointment per schedule
        print(appointment,"appoint")
        appointments.append({
            "schedule": schedule,
            "status": appointment.status if appointment else None
        })
    
    return render(request, 'workertemp/appointment_view.html', {'appointments': appointments})



