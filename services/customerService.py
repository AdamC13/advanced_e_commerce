from sqlalchemy.orm import Session
from database import db
from models.customer import Customer
from sqlalchemy import select, delete
from flask import jsonify, request
from schemas.customerSchema import customer_schema
from marshmallow import ValidationError

# Create a function that takes in customer data and creates a new customer in db
def save(customer_data):
    # Open a session
    with Session(db.engine) as session:
        with session.begin():
            # Create a new instance of Customer
            new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'])
            # Add and commit to the database
            session.add(new_customer)
            session.commit()
        # After committing the session, the new_customer object may have become detatched
        # Refresh the object to ensure it is still attached to the session
        session.refresh(new_customer)
        return new_customer
    
def fetch_all(page=1, per_page=10):
    query = select(Customer).offset((page-1) * per_page).limit(per_page)
    customers = db.session.execute(query).scalars().all()
    return customers

def delete_customer(id):
    # create a delete statement to delete the customer with the provided id
    delete_statement = delete(Customer).where(Customer.customer_id == id)
    #                    DELETE FROM Customers customer_id = id
    with db.session.begin(): #start our session transaction
        result = db.session.execute(delete_statement) #executing delete query
        print(result)
        # check that the customer exists
        if result.rowcount == 0:
            return jsonify({"error": "Customer not found"}), 404
        
        return jsonify({"message": "Customer removed succesfully"}), 200
    
def update_customer(id):
    with Session(db.engine) as session:
        with session.begin(): #begin a transaction
            # query our customer table for the id passed through our url
            query = select(Customer).filter(Customer.customer_id == id) #SELECT * FROM Customers WHERE customer_id = id
            result = session.execute(query).scalars().first()
            if result is None:
                return jsonify({"error": "Customer Not Found"}), 404
            customer = result

            try:
                # validate incoming data and deserialize
                customer_data = customer_schema.load(request.json)
            except ValidationError as err:
                return jsonify(err.messages), 400

            
            # updating the customer
            for field, value in customer_data.items():
                setattr(customer, field, value)

            session.commit() #commits the transaction to save the changes
            return jsonify({"message": "Customer details updated succesfully"}), 200