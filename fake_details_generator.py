import pandas as pd
from faker import Faker

# Create object
fake = Faker()

# Generate data Sample
fake.name()
fake.text()
fake.address()
fake.email()
fake.date()
fake.country()
fake.phone_number()
fake.random_number(digits=5)

# Dataframe creation
fakeDataframe = pd.DataFrame({'date':[fake.date() for i in range(5)],
 'name':[fake.name() for i in range(5)],
 'email':[fake.email() for i in range(5)],
 'text':[fake.text() for i in range(5)]})
print(fakeDataframe)