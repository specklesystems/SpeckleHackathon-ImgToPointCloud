from array import array
from hashlib import new
from types import AsyncGeneratorType
from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.api.resources import stream
from specklepy.transports.server import ServerTransport
from specklepy.objects.geometry import Point
from specklepy.objects import Base
from random import randint

client = SpeckleClient(host = "https://latest.speckle.dev/")

account = get_default_account()
client.authenticate(token=account.token)

stream_id = "Point Cloud"
new_stream_id = client.stream.create(name = stream_id)
new_stream = client.stream.get(id = new_stream_id)

PointsArr = []


num_points = 1000
size_coord = 100


for i in range(num_points):
    x = randint(0,size_coord)
    y = randint(0,size_coord)
    z = randint(0,size_coord)
    new_point = Point()
    Point.x = x
    Point.y = y
    Point.z = z
    PointsArr.append(new_point)

base = Base()
base["@Points"] = PointsArr


transport = ServerTransport(client = client,stream_id = new_stream_id )

hash = operations.send(base= base,transports= [transport])

commit_id = client.commit.create(
    stream_id= new_stream_id,
    obj_id=hash,
    message = "this is a point cloud array"
)