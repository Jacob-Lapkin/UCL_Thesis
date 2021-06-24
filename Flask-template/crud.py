from app import db, Puppy

# create 
my_puppy = Puppy('Leonoardo', 'Dicap')
db.session.add(my_puppy)
db.session.commit()

# read
all_puppies = Puppy.query.all()
print(all_puppies)

# select by ID
puppy_one = Puppy.query.get(1)
print(puppy_one.first)

# filters
# this will produce SQL code
puppy_leonardo = Puppy.query.filter_by(first='Leonardo')
print(puppy_leonardo.all())

#update
first_puppy = Puppy.query.get(1)
first_puppy.first = 'George'
db.session.add(first_puppy)
db.session.commit()

# delete
second_pup = Puppy.query.get(2)
db.session.delete(second_pup)
db.session.commit()

#
all_puppies = Puppy.query.all()
print(all_puppies)

