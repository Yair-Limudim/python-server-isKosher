from flask import Flask, jsonify, request
import random
from datetime import datetime, timedelta
from faker import Faker

from config import Config

app = Flask(__name__)
fake = Faker('he_IL')


def generate_mock_kosher_business():
    business_data = {
        "name": random.choice(Config.BUSINESS_NAMES),
        "address": fake.address(),
        "phone_number": fake.phone_number(),
        "supervisor": fake.name(),
        "certification_date": fake.date_between(start_date="-2y", end_date="today"),
        "expiration_date": (datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"),
        "certification_number": fake.bothify(text="???-######"),
        "food_type": random.choice(Config.FOOD_TYPES),
        "kosher_type": random.choice(Config.KOSHER_CERTIFICATIONS)
    }
    return business_data


mock_data_list = [generate_mock_kosher_business() for _ in range(Config.NUM_OF_EXAMPLES)]


@app.route('/businesses', methods=['GET'])
def get_businesses():
    name = request.args.get('name', default='', type=str)
    city = request.args.get('city', default='', type=str)
    kosher_type = request.args.get('kosher_type', default='', type=str)
    food_type = request.args.get('food_type', default='', type=str)

    filtered_businesses = mock_data_list

    if name:
        filtered_businesses = [business for business in filtered_businesses if name in business['name']]
    if city:
        filtered_businesses = [business for business in filtered_businesses if city in business['address']]
    if kosher_type:
        filtered_businesses = [business for business in filtered_businesses if kosher_type in business['kosher_type']]
    if food_type:
        filtered_businesses = [business for business in filtered_businesses if food_type in business['food_type']]

    return jsonify(filtered_businesses[:Config.MAX_RESULTS])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
