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
    sales_last_week = Sale.objects.filter(sale_date__gte=seven_days_ago)

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

'''def generate_line_plot(sales):
    plt.figure(figsize=(10, 6))
    
    # Create a dictionary to store data for each item
    item_data = {}
    
    # Process data for each item type
    for sale in sales:
        if sale.i_type not in item_data:
            item_data[sale.i_type] = {'dates': [], 'total_quantity': []}
        if sale.sale_date not in item_data[sale.i_type]['dates']:
            item_data[sale.i_type]['dates'].append(sale.sale_date)
            item_data[sale.i_type]['total_quantity'].append(sale.cost)
        else:
            index = item_data[sale.i_type]['dates'].index(sale.sale_date)
            #total_cost = sale.cost * sale.quantity
            item_data[sale.i_type]['total_quantity'][index] += (sale.totalcost)
    
    # Plot each item's data
    for item, data in item_data.items():
        plt.plot(data['dates'], data['total_quantity'], marker='o', linestyle='-', label=item)
    
    plt.title('Sales over Time by Item')
    plt.xlabel('Date')
    plt.ylabel('Sale')
    plt.grid(True)
    plt.legend()

    # Save the plot as an image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    return image_base64'''

from datetime import datetime, timedelta

def generate_line_plot(sales):
    plt.figure(figsize=(10, 6))
    
    # Create a dictionary to store data for each item
    item_data = {}
    
    # Filter sales data for the past month
    today = datetime.today().date()
    past_month = today - timedelta(days=30)
    filtered_sales = [sale for sale in sales if sale.sale_date >= past_month]
    
    # Process data for each item type
    for sale in filtered_sales:
        if sale.i_type not in item_data:
            item_data[sale.i_type] = {'dates': [], 'total_quantity': []}
        if sale.sale_date not in item_data[sale.i_type]['dates']:
            item_data[sale.i_type]['dates'].append(sale.sale_date)
            item_data[sale.i_type]['total_quantity'].append(sale.totalcost)
        else:
            index = item_data[sale.i_type]['dates'].index(sale.sale_date)
            item_data[sale.i_type]['total_quantity'][index] += sale.totalcost
    
    # Plot each item's data
    for item, data in item_data.items():
        plt.plot(data['dates'], data['total_quantity'], marker='o', linestyle='-', label=item)
    
    plt.title('Sales over Time by Item (Past Month)')
    plt.xlabel('Date')
    plt.ylabel('Sale')
    plt.grid(True)
    plt.legend()

    # Save the plot as an image
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    return image_base64


'''def generate_bar_plot(sales):
    # Group sales data by manufacturer and sum quantities sold for each manufacturer
    manufacturer_sales = {}
    for sale in sales:
        if sale.manufacturer in manufacturer_sales:
            manufacturer_sales[sale.manufacturer] += sale.items_sold
        else:
            manufacturer_sales[sale.manufacturer] = sale.items_sold

    # Extract x and y values for the plot
    x_values = list(manufacturer_sales.keys())
    y_values = list(manufacturer_sales.values())
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

    return image_base64'''

from datetime import datetime, timedelta

'''def generate_bar_plot(sales):
    # Filter sales data for the past 7 days
    today = datetime.today().date()
    past_week = today - timedelta(days=7)
    filtered_sales = [sale for sale in sales if sale.sale_date >= past_week]

    # Group sales data by manufacturer and sum quantities sold for each manufacturer
    manufacturer_sales = {}
    for sale in filtered_sales:
        if sale.manufacturer in manufacturer_sales:
            manufacturer_sales[sale.manufacturer] += sale.items_sold
        else:
            manufacturer_sales[sale.manufacturer] = sale.items_sold

    # Extract x and y values for the plot
    x_values = list(manufacturer_sales.keys())
    y_values = list(manufacturer_sales.values())
    plt.figure(figsize=(10, 6))
    plt.bar(x_values, y_values)
    plt.title('Sales by Manufacturer (Past 7 Days)')
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

    return image_base64'''


from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def generate_bar_plot(sales):
    # Filter sales data for the past 7 days
    today = datetime.today().date()
    past_week = today - timedelta(days=7)
    filtered_sales = [sale for sale in sales if sale.sale_date >= past_week]

    # Group sales data by manufacturer and sum quantities sold for each manufacturer
    manufacturer_sales = {}
    for sale in filtered_sales:
        if sale.v_type in manufacturer_sales:
            manufacturer_sales[sale.v_type] += sale.items_sold
        else:
            manufacturer_sales[sale.v_type] = sale.items_sold

    # Extract x and y values for the plot
    x_values = list(manufacturer_sales.keys())
    y_values = list(manufacturer_sales.values())
    
    plt.figure(figsize=(10, 6))
    # Add numbers at the end of each bar
    plt.barh(x_values, y_values, height=0.3, color='hotpink' )  # Adjust the height to keep the bars thin

    # Add numbers at the end of each bar
    for i, value in enumerate(y_values):
        plt.text(value, i, str(value), ha='left', va='center')  # Add annotation at the end of the bar

    plt.title('Sales by Manufacturer (Past 7 Days)')
    plt.ylabel('Vehicle')
    plt.xlabel('Quantity')
    plt.grid(axis='x')

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


from datetime import datetime, timedelta

def calculate_totals(sales):
    # Calculate totals for the past month
    today = datetime.today().date()
    past_month = today - timedelta(days=30)
    sales_past_month = [sale for sale in sales if sale.sale_date >= past_month]
    revenue_past_month = sum(sale.totalcost for sale in sales_past_month)
    items_sold_past_month = sum(sale.items_sold for sale in sales_past_month)

    # Calculate totals for the past week
    past_week = today - timedelta(days=7)
    sales_past_week = [sale for sale in sales if sale.sale_date >= past_week]
    revenue_past_week = sum(sale.totalcost for sale in sales_past_week)
    items_sold_past_week = sum(sale.items_sold for sale in sales_past_week)

    return {
        "revenue_past_month": revenue_past_month,
        "items_sold_past_month": items_sold_past_month,
        "revenue_past_week": revenue_past_week,
        "items_sold_past_week": items_sold_past_week
    }

