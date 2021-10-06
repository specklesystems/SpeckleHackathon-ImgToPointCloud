import os
import glob
import argparse
import matplotlib

# Keras / TensorFlow
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '5'
from keras.models import load_model
from layers import BilinearUpSampling2D
from utils import predict, load_images2, display_images
from matplotlib import pyplot as plt
from PIL import Image
import json

from sp import new_pointcloud, store_pointcloud

# Argument Parser
parser = argparse.ArgumentParser(description='High Quality Monocular Depth Estimation via Transfer Learning')
parser.add_argument('--model', default='nyu.h5', type=str, help='Trained Keras model file.')
parser.add_argument('--input', default='examples/*.png', type=str, help='Input filename or folder.')
args = parser.parse_args()

# Custom object needed for inference and training
custom_objects = {'BilinearUpSampling2D': BilinearUpSampling2D, 'depth_loss_function': None}

model = None

def load_model_the_real_one():
    global model
    if model != None:
        return
    print('Loading model...')

    # Load model into GPU / CPU
    model = load_model('nyu.h5', custom_objects=custom_objects, compile=False)

    print('\nModel loaded ({0}).'.format(args.model))


def createPC(img_fnames):
    global model
    load_model_the_real_one()
    images0 = []
    images1 = []
    images2 = []

    for fname in img_fnames:
        img = Image.open(fname)
        if img.size[0] > 800 or img.size[1] > 800:
            img.thumbnail((800, 800), Image.ANTIALIAS)
        images0.append(img)
        resized = img.resize((640, 480), Image.LANCZOS)
        images1.append(resized)
        img.show()
        resized.show()
        images2.append(img.resize((320, 240), Image.LANCZOS))

    # Input images
    inputs = load_images2( images1 )
    print('\nLoaded ({0}) images of size {1}.'.format(inputs.shape[0], inputs.shape[1:]))

    # Compute results
    outputs = predict(model, inputs)

    #matplotlib problem on ubuntu terminal fix
    #matplotlib.use('TkAgg')

    out = outputs[0].tolist()
    print(outputs[0].shape)

    return createSingleImagePC(images0[0], out)

    pc = new_pointcloud()

    for x in range(320):
        for y in range(240):
            z = out[y][x][0] * 1000
            r, g, b = images2[0].getpixel((x, y))
            pc.add_point(x, z, -y, r, g, b)

            #for (dx, dy) in [(-1, 0), (0, -1)]:
            #    px = x + dx
            #    py = y + dy
            #    if px < 0 or py < 0:
            #        continue
            #    pz = out[py][px][0] * 1000
            #    if abs(z - pz) < 1:
            #        continue


    return store_pointcloud(pc)

def createSingleImagePC(img, depths):
    # depths is 240x320x1

    pc = new_pointcloud()

    fullwidth, fullheight = img.size
    previous_depth = []
    for y in range(fullheight):
        previous_depth.append([])
        for x in range(fullwidth):
            depthy = y * 240 / fullheight
            depthx = x * 320 / fullwidth
            dx0 = int(depthx)
            dy0 = int(depthy)
            if dx0 + 1 >= 320:
                dx1 = dx0
            else:
                dx1 = dx0 + 1

            if dy0 + 1 >= 240:
                dy1 = dy0
            else:
                dy1 = dy0 + 1
            d00 = depths[dy0][dx0][0] * 1000
            d10 = depths[dy1][dx0][0] * 1000
            d01 = depths[dy0][dx1][0] * 1000
            d11 = depths[dy1][dx1][0] * 1000

            y1factor = depthy - int(depthy)
            y0factor = 1 - y1factor
            x1factor = depthx - int(depthx)
            x0factor = 1 - x1factor

            d00factor = y0factor * x0factor
            d01factor = y0factor * x1factor
            d10factor = y1factor * x0factor
            d11factor = y1factor * x1factor
            factor_sum = d00factor + d01factor + d10factor + d11factor

            factor_factor = 1 / factor_sum

            d = d00 * d00factor * factor_factor + \
                d10 * d10factor * factor_factor + \
                d01 * d01factor * factor_factor + \
                d11 * d11factor * factor_factor

            d *= fullwidth / 320

            r, g, b = img.getpixel((x, y))
            pc.add_point(x, d, -y, r, g, b)

            previous_depth[y].append(d)

            depth_x = d 
            depth_y = d
            if x >= 1:
                depth_x = previous_depth[y][x-1]
            if y >= 1:
                depth_y = previous_depth[y-1][x]
            if abs(depth_x - d) > abs(depth_y - d):
                largest_depth = depth_x
            else:
                largest_depth = depth_y

            num_points = int( abs( d - largest_depth) )
            if num_points < 1:
                continue
            for i in range(num_points):
                if ( d > largest_depth):
                    pc.add_point(x, d - i + 1, -y, r, g, b)
                else:
                    pc.add_point(x, d + i - 1, -y, r, g, b)

 

    return store_pointcloud(pc)

#with open('output.json', 'w') as f:
#    f.write(json.dumps(out, indent=2))

# Display results
#viz = display_images(outputs.copy(), inputs.copy())
#plt.figure(figsize=(10,5))
#plt.imshow(viz)
#plt.savefig('test.png')
#plt.show()
