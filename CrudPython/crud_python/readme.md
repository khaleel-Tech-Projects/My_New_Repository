🛒 Product Management System
A simple web-based Product Management System built with Python, Flask, SQLite, and Bootstrap. This application allows users to create, read, update, and delete products with a user-friendly interface.

📌 Features
Add new products
View detailed product information
Edit existing products
Delete products
Bootstrap-based responsive UI

📁 Project Structure
project/
│
├── app.py                  # Main Flask app
├── products.db             # SQLite database (auto-created)
├── templates/              # HTML templates
│   ├── index.html          # Product list page
│   ├── add_product.html    # Add product form
│   ├── edit_product.html   # Edit product form
│   └── view_product.html   # View product details
└── README.md               # Project documentation
🛠️ Requirements
Python 3.x

Flask

🔧 Installation & Setup
Clone the repository
git clone https://github.com/lopalopa/product-management-system.git
cd product-management-system
Install Flask
pip install flask
Run the app

python app.py
Access the application

Open your browser and go to: http://127.0.0.1:5000

🖼️ Screenshots

🔐 Note
This app uses Flask's development server, which is not recommended for production. For deployment, consider using a production WSGI server like Gunicorn or uWSGI.

📄 License
This project is licensed under the MIT License - feel free to use, modify, and share.
