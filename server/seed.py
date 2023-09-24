from app import app
from sqlalchemy.exc import IntegrityError
from models import db, Restaurant, Pizza, RestaurantPizza
from faker import Faker

fake = Faker()

# List of unique pizza names and associated ingredients
pizza_data = [
    ("Margherita", "Tomato Sauce, Mozzarella Cheese, Basil"),
    ("Pepperoni", "Tomato Sauce, Pepperoni, Mozzarella Cheese"),
    ("Hawaiian", "Tomato Sauce, Ham, Pineapple, Mozzarella Cheese"),
    ("Supreme", "Tomato Sauce, Pepperoni, Sausage, Bell Peppers, Olives, Onions, Mozzarella Cheese"),
    ("Veggie Delight", "Tomato Sauce, Mushrooms, Bell Peppers, Onions, Black Olives, Mozzarella Cheese"),
    ("Four Cheese", "Tomato Sauce, Mozzarella, Cheddar, Parmesan, Feta Cheese"),
    ("BBQ Chicken", "BBQ Sauce, Chicken, Red Onions, Cilantro, Mozzarella Cheese"),
    ("Mushroom Lovers", "Tomato Sauce, Mushrooms, Mozzarella Cheese"),
    ("Meat Lovers", "Tomato Sauce, Pepperoni, Sausage, Bacon, Ground Beef, Mozzarella Cheese"),
    ("Pesto Chicken", "Pesto Sauce, Chicken, Cherry Tomatoes, Mozzarella Cheese"),
]

# Function to generate fake data for restaurants
def generate_restaurant():
    return Restaurant(
        name=fake.company(),  # Generate random company names as restaurant names
        address=fake.address(),
    )

# Function to generate fake data for restaurant-pizza relationships
def generate_restaurant_pizza(restaurant, pizza):
    return RestaurantPizza(
        restaurant=restaurant,
        pizza=pizza,
        price=fake.random_int(min=1, max=30),  # Random price between 5 and 20
    )

if __name__ == '__main__':
    with app.app_context():
        # Delete existing data from tables
        db.session.query(RestaurantPizza).delete()
        db.session.query(Restaurant).delete()
        db.session.query(Pizza).delete()
        db.session.commit()

        try:
            # Generate and add fake data for pizzas
            pizzas = [Pizza(name=name, ingredients=ingredients) for name, ingredients in pizza_data]
            db.session.add_all(pizzas)
            db.session.commit()

            # Generate and add fake data for restaurants
            restaurants = [generate_restaurant() for _ in range(5)]  # Create 5 restaurants
            db.session.add_all(restaurants)
            db.session.commit()

            # Generate and add fake data for restaurant-pizza relationships
            for restaurant in restaurants:
                for _ in range(3):  # Each restaurant offers 3 pizzas
                    pizza = fake.random_element(pizzas)
                    restaurant_pizza = generate_restaurant_pizza(restaurant, pizza)
                    db.session.add(restaurant_pizza)
            db.session.commit()

            print("Fake data seeded successfully!")

        except IntegrityError as e:
            db.session.rollback()
            print(f"Error seeding fake data: {e}")
