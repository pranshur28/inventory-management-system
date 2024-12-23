# Inventory Management System

A web-based inventory management system built with Flask that helps businesses track and manage their product inventory efficiently.

## Features

- Add new products to inventory
- Edit existing product details
- Delete products from inventory
- View all products in a clean, organized table
- Track product quantities and prices
- Real-time inventory updates

## Technologies Used

- Python 3.x
- Flask (Web Framework)
- SQLite (Database)
- HTML/CSS
- Bootstrap 5 (Frontend Styling)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/pranshur28/inventory-management-system.git
   cd inventory-management-system
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your web browser and navigate to `http://localhost:5000`

## Project Structure

```
inventory-management-system/
├── app.py                  # Main application file
├── requirements.txt        # Project dependencies
├── instance/              
│   └── inventory.db       # SQLite database
└── templates/             # HTML templates
    ├── base.html          # Base template
    ├── index.html         # Home page
    ├── add_product.html   # Add product form
    └── edit_product.html  # Edit product form
```

## Usage

1. **Adding Products**:
   - Click on "Add Product" button
   - Fill in the product details
   - Submit the form

2. **Editing Products**:
   - Click on the "Edit" button next to a product
   - Modify the product details
   - Save changes

3. **Deleting Products**:
   - Click on the "Delete" button next to a product
   - Confirm deletion

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).
