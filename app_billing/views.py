from django.shortcuts import render, redirect
from .models import Items, Purchase, Order, OrderLine
from .forms import ItemCreateForm, PurchaceCreateForm, OrderCreateForm, \
    OrderLineCreateForm, RegistrationForm, LoginForm, SearchForm
from django.views.generic import TemplateView
from django.db.models import Sum
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import datetime,date
from django.db.models import Q

class ItemCreate(TemplateView):
    model = Items
    template_name = 'app_billing/item_create.html'
    form_class = ItemCreateForm
    def get(self, request, *args, **kwargs):
        items = Items.objects.all()
        self.context = {
            "form": self.form_class,
            "items":items
        }
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item')
        return render(request, self.template_name, self.context)

"""class ItemView(TemplateView):
    model = Items
    template_name = 'app_billing/item_view.html'
    def get(self, request, *args, **kwargs):
        items = self.model.objects.all()
        self.context = {
            'items': items
        }
        return render(request,self.template_name, self.context)"""

class ItemDelete(TemplateView):
    model = Items
    def get_object(self, id):
        return self.model.objects.get(id=id)

    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        item = self.get_object(id)
        item.delete()
        return redirect('item')

class PurchaseCreate(TemplateView):
    model = Purchase
    template_name = 'app_billing/purchase_create.html'
    form_class = PurchaceCreateForm
    def get(self, request, *args, **kwargs):
        products = self.model.objects.all()
        self.context = {
            "form":self.form_class,
            "products":products,
        }
        return render(request, self.template_name, self.context)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('productcreate')
        return render(request, self.template_name, self.context)

"""class PurchaseView(TemplateView):
    model = Purchase
    template_name = 'app_billing/purchase_view.html'
    def get(self, request, *args, **kwargs):
        products = self.model.objects.all()
        self.context = {
            'products':products,
        }
        return render(request, self.template_name, self.context)"""

class PurchaseEdit(TemplateView):
    model = Purchase
    template_name = 'app_billing/purchase_create.html'
    form_class = PurchaceCreateForm
    def get_object(self, id):
        return self.model.objects.get(id=id)

    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        products = self.get_object(id)
        form = self.form_class(instance=products)
        self.context = {
            'form':form
        }
        return render(request, self.template_name, self.context)
    def post(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        products = self.get_object(id)
        form = self.form_class(request.POST, instance=products)
        if form.is_valid():
            form.save()
            return redirect('productcreate')
        return render(request, self.template_name, self.context)

"""class PurchaseDetailedView(TemplateView):
    model = Purchase
    template_name = 'app_billing/purchase_detailedview.html'
    def get_object(self, id):
        return self.model.objects.get(id=id)
    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        items = self.get_object(id)
        self.context = {
            'items':items,
        }
        return render(request, self.template_name, self.context)"""

class PurchaseDelete(TemplateView):
    model = Purchase
    def get_object(self,id):
        return self.model.objects.get(id=id)
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        product = self.get_object(id)
        product.delete()
        return redirect('productcreate')

class OrderCreate(TemplateView):
    model = Order
    form_class = OrderCreateForm
    template_name = 'app_billing/order_create.html'
    def get(self, request, *args, **kwargs):
        order = self.model.objects.last()
        if order:
            last_billnum = order.billnumber
            lst = int(last_billnum.split('-')[1])+1
            billnum = 'BL-'+str(lst)
        else:
            billnum = 'BL-1000'
        form = self.form_class(initial={'billnumber':billnum})
        self.context = {
            "form":form
        }
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            billnumber = form.cleaned_data.get("billnumber")

            form.save()

            return redirect('orderlinecreate', billnumber=billnumber )

class OrderLineCreate(TemplateView):
    model = OrderLine
    form_class = OrderLineCreateForm
    template_name = 'app_billing/orderline_create.html'
    def get(self, request, *args, **kwargs):
        billnum = kwargs.get("billnumber")
        form = self.form_class(initial={"bill_number":billnum})
        self.context = {
            "form": form,
            "items": self.model.objects.filter(bill_number__billnumber=billnum),
            "billnum":billnum,
        }

        total = OrderLine.objects.filter(bill_number__billnumber=billnum).aggregate(Sum('amount'))
        self.context["total"]=total["amount__sum"]

        return render(request, self.template_name, self.context)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            bill_number = form.cleaned_data.get("bill_number")
            p_qty = form.cleaned_data.get("product_quantity")
            product_name = form.cleaned_data.get("product_name")
            order = Order.objects.get(billnumber=bill_number)
            product = Purchase.objects.get(items__item_name=product_name)
            prdct = Items.objects.get(item_name=product_name)
            amount = p_qty * product.selling_price

            orderline = self.model(bill_number=order, product_name=prdct,product_qty=p_qty, amount=amount)
            orderline.save()
            return redirect('orderlinecreate', billnumber=bill_number)

class BillGenrate(TemplateView):
    model = Order
    context = {}
    template_name = 'app_billing/billdisplay.html'

    def get(self, request, *args, **kwargs):
        billnum = kwargs.get('billnumber')
        orderlines = OrderLine.objects.filter(bill_number__billnumber=billnum)
        total = OrderLine.objects.filter(bill_number__billnumber=billnum).aggregate(Sum('amount'))
        self.context = {
            'billnum':billnum,
            'orderlines':orderlines,
            'total':total['amount__sum'],
        }
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        bill_number = kwargs.get('billnumber')
        ordr = self.model.objects.get(billnumber=bill_number)
        total = OrderLine.objects.filter(bill_number__billnumber=bill_number).aggregate(Sum('amount'))
        total = total['amount__sum']
        ordr.bill_total = total
        ordr.save()
        return redirect('ordercreate')


class Registration(TemplateView):
    form_class = RegistrationForm
    model = User
    template_name = 'app_billing/registration.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class
        self.context={
            "form":form
        }
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'app_billing/login.html')
        else:
            self.context = {
                "form":form
            }
            return render(request, self.template_name, self.context)

class LoginView(TemplateView):
    template_name = 'app_billing/login.html'
    form_class = LoginForm
    def get(self, request, *args, **kwargs):
        form = self.form_class
        self.context = {
            "form": form
        }
        return render(request, self.template_name, self.context)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            uname = form.cleaned_data.get('Username')
            pwd = form.cleaned_data.get('Password')
            user = authenticate(username=uname, password=pwd)
            if user != None:
                login(request,user)
                return redirect('dsales')
            else:
                self.context = {

                    "form":self.form_class(request.POST)

                }
                return render(request,self.template_name, self.context)


class SearchView(TemplateView):
    model = OrderLine
    form_class = SearchForm
    template_name = 'app_billing/search.html'
    def get(self, request, *args, **kwargs):
        form = self.form_class
        self.context = {
            "form":form
        }
        products = OrderLine.objects.filter()
        return render(request, self.template_name, self.context)
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            billnum = form.cleaned_data.get("search")
            items = OrderLine.objects.filter(bill_number__billnumber=billnum)
            self.context = {
                "items":items,
                "form":form,
            }
            return render(request, self.template_name, self.context)

class DailySales(TemplateView):
    model = Order

    template_name = 'app_billing/admin_home.html'
    def get(self, request, *args, **kwargs):
        dates = date.today()
        tbill = Order.objects.filter(bill_date=dates)

        products = OrderLine.objects.filter(bill_number__billnumber__in=[t.billnumber for t in tbill])

        
        self.context = {
            "products":products,

        }
        return render(request, self.template_name, self.context)



class adminpagecontent(TemplateView):
    template_name = 'app_billing/admin.html'

    def get(self, request, *args, **kwargs):
        context={}

        #   pie chart

        list, countlist, countvalues, datelist, datevalues = [], [], [], [], []
        dict = {}
        for object in Order.objects.all():

            if object.bill_date not in list:
                list.append(object.bill_date)
        for date in list:
            result = Order.objects.filter(bill_date=date).count()
            dict[str(date)] = result
            countlist.append(result)
        dict = sorted(dict, key=dict.get, reverse=True)
        countlist = sorted(countlist, reverse=True)
        for i in range(3):
            countvalues.append(str(countlist[i]))
            datevalues.append(dict[i])
        context['countvalues'] = ','.join((countvalues))
        context['datevalues'] = ','.join((datevalues))
        context['date'] = datevalues

        #   display collection by month,week,day

        cunrent_month = datetime.now().month
        monthly_total = Order.objects.filter(bill_date__month=cunrent_month).aggregate(Sum('bill_total'))
        context['month'] = monthly_total['bill_total__sum']
        cunrent_week = date.today().isocalendar()[1]
        weekly_total = Order.objects.filter(bill_date__week=cunrent_week).aggregate(Sum('bill_total'))
        context['week'] = weekly_total['bill_total__sum']
        cunrent_day = date.today()
        daily_total = Order.objects.filter(bill_date=cunrent_day).aggregate(Sum('bill_total'))
        context['daily'] = daily_total['bill_total__sum']

        #   progress bar

        listofproducts, listofcount = [], []
        product_dict = {}
        for item in Items.objects.all():
            listofproducts.append(item.item_name)
        for item in listofproducts:
            solditemcount = 0
            obj = OrderLine.objects.filter(Q(product_name__item_name=item) & Q(bill_number__bill_date=cunrent_day))
            for i in obj:
                solditemcount += i.product_qty
                product_dict[item] = solditemcount
        toplist = sorted(product_dict, key=product_dict.get, reverse=True)
        for item in toplist:
            if item in product_dict:
                listofcount.append(product_dict[item])
        if len(toplist) >= 5:
            context['toplist'] = toplist[:5]
        else:
            context['toplist'] = toplist
        context['count'] = listofcount

        return render(request,self.template_name,context)
