from django.shortcuts import render
import pdfkit

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse
from django.template.loader import get_template
from .models import Seller, Buyer, Item, Invoice
import pdfkit



def generate_invoice(request):
    if request.method == 'POST':
        # Retrieve form data
        seller_name = request.POST.get('seller_name')
        seller_phone = request.POST.get('seller_phone')
        seller_address = request.POST.get('seller_address')
        buyer_name = request.POST.get('buyer_name')
        buyer_phone = request.POST.get('buyer_phone')
        buyer_address = request.POST.get('buyer_address')
        item_names = request.POST.getlist('item_name')
        item_prices = request.POST.getlist('item_price')
        item_taxes = request.POST.getlist('item_tax')
        item_quantities = request.POST.getlist('item_quantity')

        # Create seller instance
        seller = Seller(name=seller_name, phone=seller_phone, address=seller_address)
        seller.save()

        # Create buyer instance
        buyer = Buyer(name=buyer_name, phone=buyer_phone, address=buyer_address)
        buyer.save()

        # Create invoice instance
        invoice = Invoice(seller=seller, buyer=buyer)
        invoice.save()

        # Create item instances
        for name, price, tax, quantity in zip(item_names, item_prices, item_taxes, item_quantities):
            item = Item(name=name, price=price, tax=tax, quantity=quantity, invoice=invoice)
            item.save()

        # Generate PDF invoice using a template
        template = get_template('invoice.html')
        context = {'invoice': invoice}
        rendered_template = template.render(context)

        # Generate PDF file
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
        pdf = generate_pdf(rendered_template)
        response.write(pdf)

        return response

    return render(request, 'generate_invoice.html')

def generate_pdf(rendered_template):
    options = {
        'page-size': 'A4',
        'encoding': 'UTF-8',
    }
    pdf = pdfkit.from_string(rendered_template, False, options=options)
    return pdf

