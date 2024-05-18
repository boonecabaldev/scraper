from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from myspider.models import HatLeaf, HatNode  # replace with your actual models

# create a new engine
engine = create_engine('sqlite:///mydatabase.db')  # replace with your actual database URL

# create a new session
Session = sessionmaker(bind=engine)
session = Session()

# specify the HatNode id
hatnode_id = 2  # replace with your actual id

# query the HatNode with the specified id
hatnode = session.query(HatNode).filter(HatNode.id == hatnode_id).first()

print(f"Querying HatNode with id {hatnode_id}...")
if hatnode is not None:
    # query all HatLeaf instances related to the HatNode
    leaves = session.query(HatLeaf).filter(HatLeaf.node_id == hatnode.id).all()
    for leaf in leaves:
        print(leaf.h3_title)
    print(f"Found {len(leaves)} HatLeaf instances related to HatNode with id {hatnode_id}")
else:
    print(f"No HatNode found with id {hatnode_id}")

# close the session
session.close()