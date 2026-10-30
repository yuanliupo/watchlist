from faker import Faker
fake = Faker()
print(' '.join(fake.words(nb = 3, ext_word_list = None, unique = False)))