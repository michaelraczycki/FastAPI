import json
from faker import Faker

fake = Faker()

data = []

for _ in range(100):
    user_data = {
        "id": fake.unique.random_number(digits=5),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "email": fake.email(),
    }
    data.append(user_data)

with open('users.json', 'w') as f:
    json.dump(data, f)
