from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db_setup import Category, Base, CategoryItem, User

# engine = create_engine('sqlite:///catelogitemswithusers.db')

engine = create_engine('postgres://uiqzqtqlesjzzn:fxAK1ml3_UGwN9YOz70-Y_L66-@ec2-107-20-242-191.compute-1.amazonaws.com:5432/dv91n1mvr0bap')

# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Create dummy user
User1 = User(name="Nehal Ahmed", email="an425@live.com",
             picture='http://icons.iconarchive.com/icons/treetog/junior/128/earth-icon.png')
session.add(User1)
session.commit()

User2 = User(name="Ahmed Nehal", email="an25490@gmail.com",
             picture ='https://lh3.googleusercontent.com/-rs3jvXJp8_A/UYZspNGV60I/AAAAAAAAACQ/liJmb97XHcQ/w139-h140-p/DSC08783.JPG')
session.add(User2)
session.commit()

################################################Soccer Category#######################################################################################
category1 = Category(user_id=2, name="Soccer")

session.add(category1)
session.commit()

categoryItem0 = CategoryItem(user_id=2, 
                             name="Shinguards", 
                             description="a pad worn to protect the shins when playing soccer, hockey, and other sports.",
                             category=category1)

session.add(categoryItem0)
session.commit()


categoryItem1 = CategoryItem(user_id=2, 
                             name="Jersey", 
                             description="The shirt worn by players.",
                             category=category1)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=2, 
                             name="Soccer Cleats", 
                             description="Turf shoes often feature small rubber studs or patterns on the outsole to improve traction on hard, natural fields and artificial turf. Turf boots are also great for soccer training and can be used as a back up pair of shoes for play on hard surfaces.",
                             category=category1)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=2, 
                             name="Soccer Ball", 
                             description="A form of football played between two teams of 11 players, in which the ball may be advanced by kicking or by bouncing it off any part of the body but the arms and hands, except in the case of the goalkeepers, who may use their hands to catch, carry, throw, or stop the ball. Origin of soccer Expand.",
                             category=category1)

session.add(categoryItem3)
session.commit()

categoryItem4 = CategoryItem(user_id=2, 
                             name="Net", 
                             description="The goal is covered by a net, which is firmly attached to the goalposts, crossbar and ground behind the goals. Because the ball is restrained by the net, it is a means of telling whether the ball has actually passed under the crossbar and between the posts, so that the referee or assistant can be sure a goal has been scored.",
                             category=category1)

session.add(categoryItem4)
session.commit()

categoryItem5 = CategoryItem(user_id=2, 
                             name="Socks", 
                             description="The thick fabric that cover a player\'s legs",
                             category=category1)

session.add(categoryItem5)
session.commit()


################################################Basketball Category#######################################################################################

category2 = Category(user_id=2, name="Basketball")

session.add(category2)
session.commit()


categoryItem0 = CategoryItem(user_id=2, 
                             name="Sneakers", 
                             description="A high or low shoe, usually of fabric such as canvas, with a rubber or synthetic sole",
                             category=category2)

session.add(categoryItem0)
session.commit()

categoryItem1 = CategoryItem(user_id=2, 
                             name="Sleeveless Shirt", 
                             description="A sleeveless shirt is a shirt manufactured without sleeves, or one whose sleeves have been cut off.",
                             category=category2)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=2, 
                             name="Hoop", 
                             description="A circular band of metal, wood, or similar material, especially one used for binding the staves of barrels or forming part of a framework.",
                             category=category2)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=2, 
                             name="Backboard", 
                             description="A board placed at or forming the back of something, such as a collage or piece of electronic equipment.",
                             category=category2)

session.add(categoryItem3)
session.commit()


###############################################Baseball Category#######################################################################################

category3 = Category(user_id=1, name="Baseball")

session.add(category3)
session.commit()


categoryItem0 = CategoryItem(user_id=1, 
                             name="Cleats", 
                             description="Turf shoes often feature small rubber studs or patterns on the outsole to improve traction on hard, natural fields and artificial turf. Turf boots are also great for soccer training and can be used as a back up pair of shoes for play on hard surfaces.",
                             category=category3)

session.add(categoryItem0)
session.commit()

categoryItem1 = CategoryItem(user_id=1, 
                             name="Socks", 
                             description="The thick fabric that cover a player\'s legs",
                             category=category3)
session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, 
                             name="Jersey", 
                             description="The shirt worn by players.",
                             category=category3)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=2, 
                             name="Bat", 
                             description="A long wooden piece used by batters to hit the ball.",
                             category=category3)

session.add(categoryItem3)
session.commit()

################################################Frisbee Category#######################################################################################

category4 = Category(user_id=1, name="Frisbee")

session.add(category4)
session.commit()

categoryItem0 = CategoryItem(user_id=1, 
                             name="Jersey", 
                             description="The shirt worn by players.",
                             category=category4)

session.add(categoryItem0)
session.commit()

categoryItem1 = CategoryItem(user_id=1, 
                             name="Frisbee", 
                             description="A disc that floats through air.",
                             category=category4)

session.add(categoryItem1)
session.commit()

################################################Snowboarding Category#######################################################################################

category5 = Category(user_id=1, name="Snowboarding")

session.add(category5)
session.commit()


categoryItem0 = CategoryItem(user_id=1, 
                             name="Jacket", 
                             description="A heavy cover that keeps the body warm in cold weather.",
                             category=category5)

session.add(categoryItem0)
session.commit()

categoryItem1 = CategoryItem(user_id=1, 
                             name="Snowboard", 
                             description="A board that glides through snow.",
                             category=category5)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, 
                             name="Bindings", 
                             description="The hooks that hold the snowboarder to the board.",
                             category=category5)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=1, 
                             name="Helmet", 
                             description="A head gear that protects the head of a snowboarder in case that person falls unnaturally.",
                             category=category5)

session.add(categoryItem3)
session.commit()


################################################Rock Climbing Category#######################################################################################

category6 = Category(user_id=1, name="Rock Climbing")

session.add(category6)
session.commit()



categoryItem0 = CategoryItem(user_id=1, 
                             name="Cleats", 
                             description="Turf shoes often feature small rubber studs or patterns on the outsole to improve traction on hard, natural fields and artificial turf. Turf boots are also great for soccer training and can be used as a back up pair of shoes for play on hard surfaces.",
                             category=category6)

session.add(categoryItem0)
session.commit()

categoryItem1 = CategoryItem(user_id=1, 
                             name="Helmet", 
                             description="A head gear that protects the climber in case that person falls unnaturally.",
                             category=category6)

session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=1, 
                             name="Sling Ropes", 
                             description="Elastic ropes that stops the climber from falling to the ground in case that person falls unnaturally.",
                             category=category6)

session.add(categoryItem2)
session.commit()


################################################Foosball Category#######################################################################################
category7 = Category(user_id=2, name="Foosball")

session.add(category7)
session.commit()


categoryItem0 = CategoryItem(user_id=2, 
                             name="Foosball Table", 
                             description="A table top that has bunch of handles allowing to move a ball forward by rotating the handle.",
                             category=category7)

session.add(categoryItem0)
session.commit()

################################################Skating Category#######################################################################################

category8 = Category(user_id=1, name="Skating")

session.add(category8)
session.commit()

categoryItem1 = CategoryItem(user_id=1, 
                             name="Skates", 
                             description="Special shoes that have blades underneath the shoes to skate on ice.",
                             category=category8)
session.add(categoryItem1)
session.commit()

categoryItem3 = CategoryItem(user_id=1, 
                             name="Helmet", 
                             description="A head gear that protects the skater in case that person falls unnaturally.",
                             category=category8)

session.add(categoryItem3)
session.commit()

################################################Hockey Category#######################################################################################

category9 = Category(user_id=2, name="Hockey")

session.add(category9)
session.commit()


categoryItem1 = CategoryItem(user_id=2, 
                             name="Hockey Socks", 
                             description="The thick fabric that cover a player\'s legs",
                             category=category9)
session.add(categoryItem1)
session.commit()

categoryItem2 = CategoryItem(user_id=2, 
                             name="Jersey", 
                             description="The shirt worn by players.",
                             category=category9)

session.add(categoryItem2)
session.commit()

categoryItem3 = CategoryItem(user_id=2, 
                             name="Hockey Stick", 
                             description="A long wooden piece used by players to control the disc.",
                             category=category9)

session.add(categoryItem3)
session.commit()

print "added Categories and their items!"