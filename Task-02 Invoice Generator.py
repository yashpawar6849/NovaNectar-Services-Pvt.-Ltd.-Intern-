from flask import Flask, render_template, request
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

app = Flask(__name__)

index_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Invoice Generator</title>
</head>
<body>
    <h1>Invoice Generator</h1>
    <form action="/generate_invoice" method="POST">
        <label for="client_name">Client Name:</label>
        <input type="text" id="client_name" name="client_name" required><br><br>
        
        <label for="item_name">Item Name:</label>
        <input type="text" id="item_name" name="item_name" required><br><br>
        
        <label for="quantity">Quantity:</label>
        <input type="number" id="quantity" name="quantity" min="1" required><br><br>
        
        <label for="price">Price per Unit:</label>
        <input type="number" id="price" name="price" step="0.01" min="0.01" required><br><br>
        
        <button type="submit">Generate Invoice</button>
    </form>
</body>
</html>
"""

@app.route('/')
def index():
    return index_html

@app.route('/generate_invoice', methods=['POST'])
def generate_invoice():
    client_name = request.form['client_name']
    item_name = request.form['item_name']
    quantity = int(request.form['quantity'])
    price = float(request.form['price'])

    subtotal = quantity * price
    tax_rate = 0.1  # Example tax rate of 10%
    tax_amount = subtotal * tax_rate
    total_amount = subtotal + tax_amount

    # Create a PDF document
    response = canvas.Canvas("invoice.pdf", pagesize=letter)
    response.drawString(100, 750, "Invoice")
    response.drawString(100, 730, f"Client Name: {client_name}")
    response.drawString(100, 710, f"Item Name: {item_name}")
    response.drawString(100, 690, f"Quantity: {quantity}")
    response.drawString(100, 670, f"Price per Unit: ${price}")
    response.drawString(100, 650, f"Subtotal: ${subtotal}")
    response.drawString(100, 630, f"Tax (10%): ${tax_amount}")
    response.drawString(100, 610, f"Total: ${total_amount}")
    response.save()

    return 'Invoice generated successfully!'

if __name__ == '__main__':
    app.run(debug=True)
