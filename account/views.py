from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from slick_reporting.views import SlickReportView
from slick_reporting.fields import SlickReportField
from account.models import Paymenttype, Programme, Departments, Intakes, Cons, Students, student_status, Reciept
from re import template
from django.db.models import Q
from django.views.generic import ListView
import os
from uuid import uuid4
from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.template.loader import get_template
# from xhtml2pdf import pisa
# import io
# from reportlab.pdfgen import canvas
# from reportlab.lib.units import inch
# from reportlab.lib.pagesizes import letter
from django.contrib.staticfiles import finders


def index(request):
    return render(request, 'index.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login_view')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'register.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('adminpage')
            # elif user is not None and user.is_customer:
            #     login(request, user)
            #     return redirect('customer')
            # elif user is not None and user.is_employee:
            #     login(request, user)
            #     return redirect('employee')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'login.html', {'form': form, 'msg': msg})


def admin(request):
    return render(request,'home_content.html')




# ==================================================================== #

# #students

def add_student(request):
    #student = Students.objects.get(admin=student_id)
    departments = Departments.objects.all()
    intakes = Intakes.objects.all()
    status = student_status.objects.all()
    programme = Programme.objects.all()
    context = {
        "departments":departments,
        "intakes":intakes,
        "status":status,
        "programme":programme,
        #"student": student,
        #"student_id": student_id
    }
    return render(request, 'hod_template/add_student_template.html', context)

def add_student_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_student')
    else:
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        intake = request.POST.get('intake')
        department = request.POST.get('department')
        status = request.POST.get('status')
        total_fee = request.POST.get('total_fee')
        nin = request.POST.get('nin')
        ip_id = request.POST.get('ip_id')
        student_id = request.POST.get('student_id')
        programme = request.POST.get('programme')




        user = Students.objects.create(username=username, email=email, 
        last_name=last_name, first_name=first_name, student_id=student_id,
        nin=nin, ip_id=ip_id, totalFee=total_fee)#, programme=programme
        user.department=Departments.objects.get(id=department) 
        user.intake=Intakes.objects.get(id=intake)
        user.programme=Programme.objects.get(id=programme)
        user.status=student_status.objects.get(status_name=status)
        user.address = address
        user.save()
        messages.success(request, "student Added Successfully!")
        return redirect('add_student')

def manage_student(request):
    students = Students.objects.all()
    context = {
        "students": students
    }
    return render(request, "hod_template/manage_student_template.html", context)

def edit_student(request, stu_id):
    student = Students.objects.get(id=stu_id)
    departments = Departments.objects.all()
    intakes = Intakes.objects.all()
    status = student_status.objects.all()
    programme = Programme.objects.all()

    context = {
        "departments":departments,
        "intakes":intakes,
        "status":status,
        "student": student,
        "programme": programme,
        "stu_id": stu_id
    }
    return render(request, "hod_template/edit_student_template.html", context)

def edit_student_save(request):
    if request.method != "POST":
        return HttpResponse("<h2>Method Not Allowed</h2>")
    else:
        stu_id = request.POST.get('stu_id')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        address = request.POST.get('address')
        department = request.POST.get('department')
        intake = request.POST.get('intake')
        status = request.POST.get('status')
        gender = request.POST.get('gender')
        total_fee = request.POST.get('total_fee')
        nin = request.POST.get('nin')
        ip_id = request.POST.get('ip_id')
        student_id = request.POST.get('student_id')
        programme = request.POST.get('programme')


        user = Students.objects.get(id=stu_id)
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.username = username
        user.save()
        
        # INSERTING into student Model
        print(department)
        student_model = Students.objects.get(id=stu_id)
        student_model.department=Departments.objects.get(id=department) 
        student_model.programme=Programme.objects.get(id=programme) 
        student_model.intake=Intakes.objects.get(id=intake)
        student_model.status=student_status.objects.get(id=status)
        # student_model.gender=gender
        student_model.address = address
        student_model.nin = nin
        student_model.ip_id = ip_id
        student_model.totalFee = total_fee
        student_model.student_id = student_id
        student_model.save()

        messages.success(request, "student Updated Successfully.")
        return redirect('/edit_student/'+stu_id)

def delete_student(request, stu_id):
    student = Students.objects.get(id=stu_id)
    try:
        student.delete()
        messages.success(request, "student Deleted Successfully.")
        return redirect('manage_student')
    except:
        messages.error(request, "Failed to Delete student.")
        return redirect('manage_student')


def add_department(request):
    return render(request, "hod_template/add_department_template.html")

def add_department_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_department')
    else:
        department = request.POST.get('department')
        try:
            department_model = Departments(department_name=department)
            department_model.save()
            messages.success(request, "Department Added Successfully!")
            return redirect('add_department')
        except:
            messages.error(request, "Failed to Add Department!")
            return redirect('add_department')

def manage_department(request):
    departments = Departments.objects.all()
    context = {
        "departments": departments
    }
    return render(request, 'hod_template/manage_department_template.html', context)

def edit_department(request, department_id):
    department = Departments.objects.get(id=department_id)
    context = {
        "department": department,
        "id": department_id
    }
    return render(request, 'hod_template/edit_department_template.html', context)

def edit_department_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        department_id = request.POST.get('department_id')
        department_name = request.POST.get('department')

        try:
            department = Departments.objects.get(id=department_id)
            department.department_name = department_name
            department.save()

            messages.success(request, "department Updated Successfully.")
            return redirect('/edit_department/'+department_id)

        except:
            messages.error(request, "Failed to Update department.")
            return redirect('/edit_department/'+department_id)

def delete_department(request, department_id):
    department = Departments.objects.get(id=department_id)
    try:
        department.delete()
        messages.success(request, "department Deleted Successfully.")
        return redirect('manage_department')
    except:
        messages.error(request, "Failed to Delete department.")
        return redirect('manage_department')

# Status

def add_status(request):
    return render(request, "hod_template/add_status_template.html")

def add_status_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_status')
    else:
        status = request.POST.get('status')
        try:
            status_model = student_status(status_name=status)
            status_model.save()
            messages.success(request, "status Added Successfully!")
            return redirect('add_status')
        except:
            messages.error(request, "Failed to Add status!")
            return redirect('add_status')

def manage_status(request):
    status = student_status.objects.all()
    context = {
        "status": status
    }
    return render(request, 'hod_template/manage_status_template.html', context)

def edit_status(request, status_id):
    status = student_status.objects.get(id=status_id)
    context = {
        "status": status,
        "id": status_id
    }
    return render(request, 'hod_template/edit_status_template.html', context)

def edit_status_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        status_id = request.POST.get('status_id')
        status_name = request.POST.get('status')

        try:
            status = student_status.objects.get(id=status_id)
            status.status_name = status_name
            status.save()

            messages.success(request, "status Updated Successfully.")
            return redirect('/edit_status/'+status_id)

        except:
            messages.error(request, "Failed to Update status.")
            return redirect('/edit_status/'+status_id)

def delete_status(request, status_id):
    status = student_status.objects.get(id=status_id)
    try:
        status.delete()
        messages.success(request, "status Deleted Successfully.")
        return redirect('manage_status')
    except:
        messages.error(request, "Failed to Delete status.")
        return redirect('manage_status')

# Intakes

def add_intake(request):
    return render(request, "hod_template/add_intake_template.html")

def add_intake_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_intake')
    else:
        intake = request.POST.get('intake')
        try:
            intake_model = Intakes(intake_name=intake)
            intake_model.save()
            messages.success(request, "intake Added Successfully!")
            return redirect('add_intake')
        except:
            messages.error(request, "Failed to Add intake!")
            return redirect('add_intake')

def manage_intake(request):
    intakes = Intakes.objects.all()
    context = {
        "intakes": intakes
    }
    return render(request, 'hod_template/manage_intake_template.html', context)

def edit_intake(request, intake_id):
    intake = Intakes.objects.get(id=intake_id)
    context = {
        "intake": intake,
        "id": intake_id
    }
    return render(request, 'hod_template/edit_intake_template.html', context)

def edit_intake_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        intake_id = request.POST.get('intake_id')
        intake_name = request.POST.get('intake')

        try:
            intake = Intakes.objects.get(id=intake_id)
            intake.intake_name = intake_name
            intake.save()

            messages.success(request, "intake Updated Successfully.")
            return redirect('/edit_intake/'+intake_id)

        except:
            messages.error(request, "Failed to Update intake.")
            return redirect('/edit_intake/'+intake_id)

def delete_intake(request, intake_id):
    intake = Intakes.objects.get(id=intake_id)
    try:
        intake.delete()
        messages.success(request, "intake Deleted Successfully.")
        return redirect('manage_intake')
    except:
        messages.error(request, "Failed to Delete intake.")
        return redirect('manage_intake')


def manage_sop_admin(request):
    sops = Cons.objects.all()
    context = {
        "sops": sops
    }
    return render(request, 'hod_template/manage_sop_template.html', context)

def edit_sop_admin(request, sop_id):
    sop = Cons.objects.get(id=sop_id)
    context = {
        "sop": sop,
        "id": sop_id,
    }
    return render(request, 'hod_template/edit_sop_template.html', context)

def edit_sop_admin_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        sop_id = request.POST.get('sop_id')
        item_1 = request.POST.get('item_1')
        i_price_1 = request.POST.get('i_price_1')
        item_2 = request.POST.get('item_2')
        i_price_2 = request.POST.get('i_price_2')
        item_3 = request.POST.get('item_3')
        i_price_3 = request.POST.get('i_price_3')
        item_4 = request.POST.get('item_4')
        i_price_4 = request.POST.get('i_price_4')
        item_5 = request.POST.get('item_5')
        i_price_5 = request.POST.get('i_price_5')
        is_approved= request.POST.get('is_approved')
        if is_approved == 'on':
            is_approved = True
        else:
            is_approved = False
        # try:
        sop = Cons.objects.get(id=sop_id)
        sop.one = item_1
        sop.amountOne = i_price_1
        sop.two = item_2
        sop.amountTwo = i_price_2
        sop.three = item_3
        sop.amountThree = i_price_3
        sop.four = item_4
        sop.amountFour = i_price_4
        sop.five = item_5
        sop.amountFive = i_price_5
        sop.is_approved = is_approved
        sop.save()

        messages.success(request, "SOP Updated Successfully.")
        return redirect('/edit_sop_admin/'+sop_id)

        # except:
        #     messages.error(request, "Failed to Update SOP.")
        #     return redirect('/edit_sop_admin/'+sop_id)

def delete_sop_admin(request, sop_id):
    sop = Cons.objects.get(id=sop_id)
    try:
        sop.delete()
        messages.success(request, "SOP Deleted Successfully.")
        return redirect('manage_sop_admin')
    except:
        messages.error(request, "Failed to Delete SOP.")
        return redirect('manage_sop_admin')


class SimpleListReport(SlickReportView):
    
    report_model = Reciept
    # the model containing the data we want to analyze

    date_field = 'date'
    # a date/datetime field on the report model

    # fields on the report model ... surprise !
    columns = ['date', 'student_name', 'student_id', 'tution', 'acceptance', 'application', 'others','amount', 'total']

# Programme


def add_programme(request):
    return render(request, "hod_template/add_programme_template.html")

def add_programme_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_programme')
    else:
        programme = request.POST.get('programme')
        try:
            programme_model = Programme(programme_name=programme)
            programme_model.save()
            messages.success(request, "Programme Added Successfully!")
            return redirect('add_programme')
        except:
            messages.error(request, "Failed to Add Programme!")
            return redirect('add_programme')

def manage_programme(request):
    programme = Programme.objects.all()
    context = {
        "programme": programme,
    }
    return render(request, 'hod_template/manage_programme_template.html', context)

def edit_programme(request, programme_id):
    programme = Programme.objects.get(id=programme_id)
    context = {
        "programme": programme,
        "id": programme_id
    }
    return render(request, 'hod_template/edit_programme_template.html', context)

def edit_programme_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        programme_id = request.POST.get('programme_id')
        programme_name = request.POST.get('programme')

        try:
            programme = Programme.objects.get(id=programme_id)
            programme.programme_name = programme_name
            programme.save()

            messages.success(request, "department Updated Successfully.")
            return redirect('/edit_programmme/'+programme_id)

        except:
            messages.error(request, "Failed to Update department.")
            return redirect('/edit_programmme/'+programme_id)

def delete_programme(request, programme_id):
    programme = Programme.objects.get(id=programme_id)
    try:
        programme.delete()
        messages.success(request, "Programme Deleted Successfully.")
        return redirect('manage_programme')
    except:
        messages.error(request, "Failed to Delete Programme.")
        return redirect('manage_programme')



def add_ptype(request):
    return render(request, "hod_template/add_ptype_template.html")

def add_ptype_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_ptype')
    else:
        ptype = request.POST.get('ptype')
        try:
            ptype_model = Paymenttype(ptype_name=ptype)
            ptype_model.save()
            messages.success(request, "Payment Type Added Successfully!")
            return redirect('add_ptype')
        except:
            messages.error(request, "Failed to Add Payment Type!")
            return redirect('add_ptype')

def manage_ptype(request):
    ptype = Paymenttype.objects.all()
    context = {
        "ptype": ptype
    }
    return render(request, 'hod_template/manage_ptype_template.html', context)

def edit_ptype(request, ptype_id):
    ptype = Paymenttype.objects.get(id=ptype_id)
    context = {
        "ptype": ptype,
        "id": ptype_id
    }
    return render(request, 'hod_template/edit_ptype_template.html', context)

def edit_ptype_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        ptype_id = request.POST.get('ptype_id')
        ptype_name = request.POST.get('ptype')

        try:
            ptype = Paymenttype.objects.get(id=ptype_id)
            ptype.ptype_name = ptype_name
            ptype.save()

            messages.success(request, "Payment Type Updated Successfully.")
            return redirect('manage_ptype')

        except:
            messages.error(request, "Failed to Update Payment Type.")
            return redirect('/edit_ptype/'+ptype_id)

def delete_ptype(request, ptype_id):
    ptype = Paymenttype.objects.get(id=ptype_id)
    try:
        ptype.delete()
        messages.success(request, "Payment Type Deleted Successfully.")
        return redirect('manage_ptype')
    except:
        messages.error(request, "Failed to Delete Payment Type.")
        return redirect('manage_ptype')


# =============================================================== #


def finance_home(request):
    return render(request, "finance_template/finance_home_template.html")#, context

def finance_profile(request):
    pass


def venue_pdf(request):
    buf = io.BytesIO()

    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)
    textob = c.beginText()
    textob.setTextOrigin(inch, inch)
    textob.setFont("Helvetica", 14)
    # lines = [
    #     "Hi Evevery One",
    #     "Hi Evevery One",
    #     "Hi Evevery One",
    # ]

    receipt = InvoiceDetail.objects.all().get(id=id)

    lines = []

    for rc in receipt:
        lines.append(rc.invoice)
        lines.append(rc.amount)
        lines.append(" ")






    # for line in lines:
    #     textob.textLine(line)

    c.drawText(textob)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='reciept.pdf')

def payslip(request, pk):
    student = Students.objects.get(id=pk)
    template_path = 'finance_template/student_payslip.html'
    context = {
        'student': student,
    }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response



# def createInvoice(request):
#     #create a blank invoice ....
#     # number = 'INV-'+str(uuid4()).split('-')[-1]
#     newInvoice = Invoice.objects.create()#number=number
#     newInvoice.save()

#     inv = Invoice.objects.get()#number=number
#     return redirect('create-build-invoice', slug=inv.slug)



def create_invoice(request):
    total_students = Students.objects.count()
    total_invoice = Invoice.objects.count()

    form = InvoiceForm()
    # formset = InvoiceDetailFormSet()
    if request.method == "POST":
        form = InvoiceForm(request.POST)
        # formset = InvoiceDetailFormSet(request.POST)
        if form.is_valid():
            invoice = Invoice.objects.create(
                student=form.cleaned_data.get("student"),
                date=form.cleaned_data.get("date"),
                status=form.cleaned_data.get("status"),
                type=form.cleaned_data.get("type"),
                paymentTerms=form.cleaned_data.get("paymentTerms"),
                amount=form.cleaned_data.get("amount"),

            )
        # if formset.is_valid():
            # total = 0
            # for form in formset:
                # product = form.cleaned_data.get("product")
                # amount = form.cleaned_data.get("amount")
                # if product and amount:
                #     # Sum each row
                #     sum = float(product.product_price) * float(amount)
                #     # Sum of total invoice
                #     total += sum
                #amountamount
            InvoiceDetail(
                invoice=invoice,
            ).save()
            # Pointing the customer
            # points = 0
            # if total > 1000:
            #     points += total / 1000
            # invoice.customer.customer_points = round(points)
            # Save the points to Customer table
            invoice.student.save()

            # Save the invoice
            # invoice.total = total
            invoice.save()
            return redirect("view_invoice")

    context = {
        "total_students": total_students,
        "total_invoice": total_invoice,
        "form": form,
        # "formset": formset,
    }

    return render(request, "finance_template/create_invoice.html", context)


def view_invoice(request):
    total_students = Students.objects.count()
    total_invoice = Invoice.objects.count()

    invoice = Invoice.objects.all()

    context = {
        "total_students": total_students,
        "total_invoice": total_invoice,
        "invoice": invoice,
    }

    return render(request, "finance_template/view_invoice.html", context)


# Detail view of invoices
def view_invoice_detail(request, pk):
    total_students = Students.objects.count()
    total_invoice = Invoice.objects.count()

    invoice = Invoice.objects.get(id=pk)
    invoice_detail = InvoiceDetail.objects.filter(invoice=invoice)

    context = {
        "total_students": total_students,
        "total_invoice": total_invoice,
        # 'invoice': invoice,
        "invoice_detail": invoice_detail,
    }

    return render(request, "finance_template/view_invoice_detail.html", context)


# Delete invoice
def delete_invoice(request, pk):
    total_students = Students.objects.count()
    total_invoice = Invoice.objects.count()

    invoice = Invoice.objects.get(id=pk)
    invoice_detail = InvoiceDetail.objects.filter(invoice=invoice)
    if request.method == "POST":
        invoice_detail.delete()
        invoice.delete()
        return redirect("view_invoice")

    context = {
        "total_students": total_students,
        "total_invoice": total_invoice,
        "invoice": invoice,
        "invoice_detail": invoice_detail,
    }

    return render(request, "finance_template/delete_invoice.html", context)





# Recipet O.G

def add_reciept(request, student_id):
    student = Students.objects.get(id=student_id)
    ptype = Paymenttype.objects.all()
    context = {
        "student": student,
        "ptype": ptype,
        "id": student_id,
    }
    return render(request, "finance_template/add_reciept_template.html", context)

def add_reciept_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('manage_reciept')
    else:
        stu_name = request.POST.get('stu_name')
        stu_id = request.POST.get('stu_id')
        student_id = request.POST.get('student_id')
        ptype = request.POST.get('ptype')
        # tution = request.POST.get('tution')
        # if tution == 'on':
        #     tution = True
        # else:
        #     tution = False
        # acceptance = request.POST.get('acceptance')
        # if acceptance == 'on':
        #     acceptance = True
        # else:
        #     acceptance = False
        # application = request.POST.get('application')
        # if application == 'on':
        #     application = True
        # else:
        #     application = False
        # others = request.POST.get('others')
        # if others == 'on':
        #     others = True
        # else:
        #     others = False
        amount = request.POST.get('amount')
        total = request.POST.get('total')
        notes = request.POST.get('notes')
        stu_nin = request.POST.get('stu_nin')
        balance = request.POST.get('balance')
        # stu_programme = request.POST.get('stu_programme')

        try:
            reciept_model = Reciept(student_name=stu_name, student_id=stu_id,
            amount=amount, total=total, notes=notes)#stu_nin=stu_nin,
            reciept_model.ptype=Paymenttype.objects.get(id=ptype)
            reciept_model.save()
            messages.success(request, "Reciept Added Successfully!")
            return redirect('/add_reciept/'+student_id)
        except:
            messages.error(request, "Failed to Add Recipt!")
            return redirect('/add_reciept/'+student_id)


def manage_reciept(request):
    rec = Reciept.objects.all()
    context = {
        "rec": rec
    }
    return render(request, 'finance_template/manage_reciept_template.html', context)

def edit_reciept(request, reciept_id):
    reciept = Reciept.objects.get(id=reciept_id)
    context = {
        "reciept": reciept,
        "id": reciept_id,
    }
    return render(request, 'finance_template/edit_reciept_template.html', context)

class SearchResultsView(ListView):
    model = Students
    template_name = 'finance_template/search_results.html'

    def get_queryset(self):
        query= self.request.GET.get('q')
        object_list = Students.objects.filter(
            Q(student_id__icontains=query) | Q(nin__icontains=query) | Q(ip_id__icontains=query)
        )
        return object_list

def search(request):

    results = []

    if request.method == "GET":

        query = request.GET.get('search')

        if query == '':

            query = 'None'

        results = Students.objects.filter(Q(student_id__icontains=query) | Q(nin__icontains=query) | Q(ip_id__icontains=query) | Q(first_name__icontains=query) | Q(email__icontains=query))

    return render(request, 'finance_template/search.html', {'query': query, 'results': results})

def pdf_report_create(request, reciept_id):
    reciept = Reciept.objects.get(id=reciept_id)
    context = {
        "reciept": reciept,
        "id": reciept_id,
    }
    template_path = 'finance_template/PdfReciept.html'
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename="stu_report.pdf"'

    template = get_template(template_path)

    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funy view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
# Try All
def pdf__create(request, reciept_id):
    reciept = Reciept.objects.get(id=reciept_id)
    context = {
        "reciept": reciept,
        "id": reciept_id,
    }
    return render(request, 'finance_template/reprint.html', context)


def edit_reciept_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:        
        stu_name = request.POST.get('stu_name')
        stu_id = request.POST.get('stu_id')
        reciept_id = request.POST.get('reciept_id')
        tution = request.POST.get('tution')
        if tution == 'on':
            tution = True
        else:
            tution = False
        acceptance = request.POST.get('acceptance')
        if acceptance == 'on':
            acceptance = True
        else:
            acceptance = False
        application = request.POST.get('application')
        if application == 'on':
            application = True
        else:
            application = False
        others = request.POST.get('others')
        if others == 'on':
            others = True
        else:
            others = False
        amount = request.POST.get('amount')
        total = request.POST.get('total')
        notes = request.POST.get('notes')
        try:
            rec = Reciept.objects.get(id=reciept_id)
            rec.student_name = stu_name
            rec.student_id = stu_id
            rec.tution = tution
            rec.acceptance = acceptance
            rec.application = application
            rec.others = others
            rec.amount = amount
            rec.total = total
            rec.notes = notes
            rec.save()

            messages.success(request, "Reciept Updated Successfully.")
            return redirect('/edit_reciept/'+reciept_id)

        except:
            messages.error(request, "Failed to Update Reciept.")
            return redirect('/edit_reciept/'+reciept_id)

def delete_reciept(request, reciept_id):
    reciept = Reciept.objects.get(id=reciept_id)
    try:
        reciept.delete()
        messages.success(request, "Reciept Deleted Successfully.")
        return redirect('manage_reciept')
    except:
        messages.error(request, "Failed to Delete Reciept.")
        return redirect('manage_reciept')


# ======================================================== #


def staff_home(request):
    return render(request, "staff_template/staff_home_template.html")#, context


# #SOP
def add_sop(request):
    return render(request, "staff_template/add_sop_template.html")

def add_sop_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_sop')
    else:
        item_1 = request.POST.get('item_1')
        i_price_1 = request.POST.get('i_price_1')
        item_2 = request.POST.get('item_2')
        i_price_2 = request.POST.get('i_price_2')
        item_3 = request.POST.get('item_3')
        i_price_3 = request.POST.get('i_price_3')
        item_4 = request.POST.get('item_4')
        i_price_4 = request.POST.get('i_price_4')
        item_5 = request.POST.get('item_5')
        i_price_5 = request.POST.get('i_price_5')

        try:
            sop_model = Cons(one=item_1, amountOne=i_price_1, two=item_2, amountTwo=i_price_2,
            three=item_3, amountThree=i_price_3, four=item_4, amountFour=i_price_4, five=item_5, amountFive=i_price_5)
            sop_model.save()
            messages.success(request, "SOP Added Successfully!")
            return redirect('add_sop')
        except:
            messages.error(request, "Failed to Add SOP!")
            return redirect('add_sop')

def manage_sop(request):
    sops = Cons.objects.all()
    context = {
        "sops": sops
    }
    return render(request, 'staff_template/manage_sop_template.html', context)

def edit_sop(request, sop_id):
    sop = Cons.objects.get(id=sop_id)
    context = {
        "sop": sop,
        "id": sop_id,
    }
    return render(request, 'staff_template/edit_sop_template.html', context)

def edit_sop_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        sop_id = request.POST.get('sop_id')
        item_1 = request.POST.get('item_1')
        i_price_1 = request.POST.get('i_price_1')
        item_2 = request.POST.get('item_2')
        i_price_2 = request.POST.get('i_price_2')
        item_3 = request.POST.get('item_3')
        i_price_3 = request.POST.get('i_price_3')
        item_4 = request.POST.get('item_4')
        i_price_4 = request.POST.get('i_price_4')
        item_5 = request.POST.get('item_5')
        i_price_5 = request.POST.get('i_price_5')
        try:
            sop = Cons.objects.get(id=sop_id)
            sop.one = item_1
            sop.amountOne = i_price_1
            sop.two = item_2
            sop.amountTwo = i_price_2
            sop.three = item_3
            sop.amountThree = i_price_3
            sop.four = item_4
            sop.amountFour = i_price_4
            sop.five = item_5
            sop.amountFive = i_price_5
            sop.save()

            messages.success(request, "SOP Updated Successfully.")
            return redirect('/edit_sop/'+sop_id)

        except:
            messages.error(request, "Failed to Update SOP.")
            return redirect('/edit_sop/'+sop_id)

def delete_sop(request, sop_id):
    sop = Cons.objects.get(id=sop_id)
    try:
        sop.delete()
        messages.success(request, "SOP Deleted Successfully.")
        return redirect('manage_sop')
    except:
        messages.error(request, "Failed to Delete SOP.")
        return redirect('manage_sop')



# #intake
def add_intake(request):
    return render(request, "staff_template/add_intake_template.html")

def add_intake_save(request):
    if request.method != "POST":
        messages.error(request, "Invalid Method!")
        return redirect('add_intake')
    else:
        intake = request.POST.get('intake')
        try:
            intake_model = Intakes(intake_name=intake)
            intake_model.save()
            messages.success(request, "intake Added Successfully!")
            return redirect('add_intake')
        except:
            messages.error(request, "Failed to Add intake!")
            return redirect('add_intake')

def manage_intake(request):
    intakes = Intakes.objects.all()
    context = {
        "intakes": intakes
    }
    return render(request, 'staff_template/manage_intake_template.html', context)

def edit_intake(request, intake_id):
    intake = Intakes.objects.get(id=intake_id)
    context = {
        "intake": intake,
        "id": intake_id
    }
    return render(request, 'staff_template/edit_intake_template.html', context)

def edit_intake_save(request):
    if request.method != "POST":
        HttpResponse("Invalid Method")
    else:
        intake_id = request.POST.get('intake_id')
        intake_name = request.POST.get('intake')

        try:
            intake = Intakes.objects.get(id=intake_id)
            intake.intake_name = intake_name
            intake.save()

            messages.success(request, "intake Updated Successfully.")
            return redirect('/edit_intake/'+intake_id)

        except:
            messages.error(request, "Failed to Update intake.")
            return redirect('/edit_intake/'+intake_id)

def delete_intake(request, intake_id):
    intake = Intakes.objects.get(id=intake_id)
    try:
        intake.delete()
        messages.success(request, "intake Deleted Successfully.")
        return redirect('manage_intake')
    except:
        messages.error(request, "Failed to Delete intake.")
        return redirect('manage_intake')