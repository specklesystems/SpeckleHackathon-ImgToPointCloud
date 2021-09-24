
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

import os
from random import randint

client = SpeckleClient(host = os.environ['SPECKLE_SERVER'])
client.authenticate(token=os.environ['SPECKLE_TOKEN'])

new_stream_id = ''

class PointCloud(Base,speckle_type = GEOMETRY + "Pointcloud",chunkable = {"points":31250,"colors":62500,"sizes":62500}):
    colors: List[int] = None
    sizes: List[float] = None
    points: List[float] = None
    bbox: Box = None

    def init(self):
        global new_stream_id
        global new_stream
        stream_id = "Point Cloud"
        new_stream_id = client.stream.create(name=stream_id)
        new_stream = client.stream.get(id=new_stream_id)

        self.colors = []
        self.points = []

    def add_point(self, x, y, z, R, G, B):
        self.points.append(x)
        self.points.append(y)
        self.points.append(z)
        RGBint = (R << 16) + (G << 8) + B
        self.colors.append(RGBint)

def new_pointcloud():
    pc = PointCloud()
    pc.init()
    return pc

def store_pointcloud(pc):
    base = Base()
    base["@PointCloud"] = pc

    transport = ServerTransport(client=client, stream_id=new_stream_id)

    hash = operations.send(base=base, transports=[transport])

    commit_id = client.commit.create(
        stream_id=new_stream_id,
        object_id=hash,
        message="this is a point cloud array"
    )
    # return 'http://anthe.local/streams/' + new_stream_id
    return 'https://latest.speckle.dev/streams/' + new_stream_id


def main():
    num_points = 10000
    size_coord = 1000

    p = new_pointcloud()

    for i in range(num_points):
        x = randint(0,size_coord)
        y = randint(0,size_coord)
        z = randint(0,size_coord)
        R = randint(0,255)
        B= randint (0,0)
        G = randint (0,0)

        p.add_point(x, y, z, R, G, B)


    store_pointcloud(p)

