from .forms import *
from .models import Item 
from .views import *
from .urls import *
from datetime import datetime , timedelta 
from django.db.models import Sum

item_sales = {}

def calculate_items_sold_last_7_days():
    # Calculate the date 7 days ago
    seven_days_ago = datetime.now() - timedelta(days=7)

    # Query the sales data for the last 7 days
    sales_last_week = Sale.objects.filter(_date__gte=seven_days_ago)

    # Initialize a dictionary to store total items sold for each item type
    

    # Calculate the total items sold for each item type
    for sale in sales_last_week:
        item_type = sale.i_type
        items_sold = sale.items_sold
        if item_type in item_sales:
            item_sales[item_type] += items_sold
        else:
            item_sales[item_type] = items_sold

    # Print the total items sold for each item type in the last week
    
    for key,value in item_sales.items() :
        _items = Item.objects.all()
        for item in _items:
            if(item.i_type == key):
                item.threshold = value 
                item.save()

    for item_type, total_items_sold in item_sales.items():
        print(f"Item Type: {item_type}, Total Items Sold: {total_items_sold}")


    '''for item_type, total_items_sold in item_sales.items():
    # Check if an item with the given item_type exists
        if (Item.objects.filter(i_type=item_type).exists() and total_items_sold !=0) :
        # Update the threshold value for items of this item_type
            Item.objects.filter(i_type=item_type).update(threshold=total_items_sold)'''


# utils.py

from matplotlib import pyplot as plt
from io import BytesIO
import base64

def generate_line_plot(sales):
    plt.figure(figsize=(10, 6))
    
    # Create a dictionary to store data for each item
    item_data = {}
    
    # Process data for each item
    for sale in sales:
        if sale.i_type not in item_data:
            item_data[sale.i_type] = {'dates': [], 'quantities': []}
        item_data[sale.i_type]['dates'].append(sale._date)
        item_data[sale.i_type]['quantities'].append(sale.items_sold)
    
    # Plot each item's data
    for item, data in item_data.items():
        plt.plot(data['dates'], data['quantities'], marker='o', linestyle='-', label=item)
    
    plt.title('Sales over Time by Item')
    plt.xlabel('Date')
    plt.ylabel('Quantity')
    plt.grid(True)
    plt.legend()

    # Save the plot as an image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    return image_base64

def generate_bar_plot(sales):
    # Process the data to get x and y values for the plot
    x_values = [sale.manufacturer for sale in sales]
    y_values = [sale.items_sold for sale in sales]

    # Create the plot using Matplotlib
    plt.figure(figsize=(10, 6))
    plt.bar(x_values, y_values)
    plt.title('Sales by Manufacturer')
    plt.xlabel('Manufacturer')
    plt.ylabel('Quantity')
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y')

    # Save the plot as an image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    return image_base64

def generate_pie_chart(sales):
    # Process the data to get labels and sizes for the plot
    labels = [sale.manufacturer for sale in sales]
    sizes = [sale.quantity for sale in sales]

    # Create the plot using Matplotlib
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title('Sales Distribution by Manufacturer')

    # Save the plot as an image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    return image_base64

