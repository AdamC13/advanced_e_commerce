from sqlalchemy.orm import Session
from database import db
from models.order import Order
from sqlalchemy import select

# Create a function that takes in customer data and creates a new customer in db
def save(customer_data):
    # Open a session
    with Session(db.engine) as session:
        with session.begin():
            # Create a new instance of Customer
            new_customer = Order(customer_id=customer_data['customer_id'], product_id=customer_data['product_id'], quantity=customer_data['quantity'], total_price=customer_data['total_price'])
            # Add and commit to the database
            session.add(new_customer)
            session.commit()
        # After committing the session, the new_customer object may have become detatched
        # Refresh the object to ensure it is still attached to the session
        session.refresh(new_customer)
        return new_customer
    
def fetch_all(page=1, per_page=10):
    query = select(Order).offset((page-1) * per_page).limit(per_page)
    customers = db.session.execute(query).scalars().all()
    return customers

def get_order(order_id):
    return db.session.get(Order, order_id)