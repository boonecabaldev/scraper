from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from myspider.models import HatLeaf, HatComponent  # replace with your actual models

# create a new engine
engine = create_engine('sqlite:///mydatabase.db')  # replace with your actual database URL

# create a new session
Session = sessionmaker(bind=engine)
session = Session()

# specify the HatComponent id
hatcomponent_id = 2  # replace with your actual id

# query the HatComponent with the specified id
hatcomponent = session.query(HatComponent).filter(HatComponent.id == hatcomponent_id).first()

print(f"Querying HatComponent with id {hatcomponent_id}...")
if hatcomponent is not None:
    # query all HatLeaf instances related to the HatComponent
    leaves = session.query(HatLeaf).filter(HatLeaf.node_id == hatcomponent.id).all()
    for leaf in leaves:
        print(leaf.h3_title)
    print(f"Found {len(leaves)} HatLeaf instances related to HatComponent with id {hatcomponent_id}")
else:
    print(f"No HatComponent found with id {hatcomponent_id}")

# close the session
session.close()