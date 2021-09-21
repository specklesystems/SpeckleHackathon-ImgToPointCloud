from array import array
from hashlib import new
from logging import NullHandler
from types import AsyncGeneratorType
from typing import List
from specklepy.api import operations
from specklepy.api.client import SpeckleClient
from specklepy.api.credentials import get_default_account
from specklepy.api.resources import stream
from specklepy.transports.server import ServerTransport
from specklepy.objects.geometry import GEOMETRY, Box, Point
from specklepy.objects import Base
from numpy import ndarray

from random import randint

client = SpeckleClient(host = "https://latest.speckle.dev/")

account = get_default_account()
client.authenticate(token=account.token)

stream_id = "Point Cloud"
new_stream_id = client.stream.create(name = stream_id)
new_stream = client.stream.get(id = new_stream_id)

class PointCloud(Base,speckle_type = GEOMETRY + "Pointcloud",chunkable = {"points":31250,"colors":62500,"sizes":62500}):

    colors: List[int] = None
    sizes: List[float] = None
    points: List[float] = None
    bbox: Box = None


points = []
num_points = 100000
size_coord = 1000
colors = [] 

for i in range(num_points):
    x = randint(0,size_coord)
    y = randint(0,size_coord)
    z = randint(0,size_coord)
    R = randint(0,255)
    B= randint (0,0)
    G = randint (0,0)
    RGBint = (R<<16) + (G<<8) + B
    colors.append(RGBint)
    points.append(x)
    points.append(y)
    points.append(z)

pointscloud = PointCloud()
pointscloud.colors = colors
pointscloud.points = points




base = Base()
base["@PointCloud"] = pointscloud

transport = ServerTransport(client = client,stream_id = new_stream_id )

hash = operations.send(base= base,transports= [transport])

commit_id = client.commit.create(
    stream_id= new_stream_id,
    object_id=hash,
    message = "this is a point cloud array"
)