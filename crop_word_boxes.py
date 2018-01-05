# Author: Ankush Gupta
# Date: 2015

"""
Visualize the generated localization synthetic
data stored in h5 data-bases
"""
from __future__ import division
import os
import os.path as osp
import numpy as np
import matplotlib.pyplot as plt 
import h5py 
from common import *
from PIL import Image
import math
import diagonal_crop

def crop_boxes(base_path, filename, text_im, wordBB):
    """
    text_im : image containing text
    charBB_list : list of 2x4xn_i bounding-box matrices
    wordBB : 2x4xm matrix of word coordinates
    """
    H,W = text_im.shape[:2]
    im = Image.fromarray(text_im)

    # plot the word-BB:
    for i in xrange(wordBB.shape[-1]):
        pt = {}
	bb = wordBB[:,:,i]
        bb = np.c_[bb,bb[:,0]]
	pt["x1"] = bb[0,0]
        pt["y1"] = bb[1,0]
        pt["x2"] = bb[0,1]
        pt["y2"] = bb[1,1]
        pt["x3"] = bb[0,2]
        pt["y3"] = bb[1,2]
        pt["x4"] = bb[0,3]
        pt["y4"] = bb[1,3]
        crop_single(im,pt).save(base_path+filename+"_"+str(i)+".jpg")



def crop_single(img, pt):

    x1 = pt["x1"]
    y1 = pt["y1"]
    x2 = pt["x2"]
    y2 = pt["y2"]
    x3 = pt["x3"]
    y3 = pt["y3"]
    x4 = pt["x4"]
    y4 = pt["y4"]

    #x1,y1 is base
    ptA_x = x2
    ptA_y = y1

    perpendicular_len = math.hypot(ptA_x - x2, ptA_y - y2)
    base_len = math.hypot(ptA_x - x1, ptA_y - y1)
    angle = math.atan(perpendicular_len/base_len)
    #NOT A PERFECT RECTANGLE!
    height = math.hypot(x2-x3,y2-y3)
    width = math.hypot(x3-x4,y3-y4)
    if(y1 < y2): #IF angle is negative
        angle = angle * -1
    #print math.degrees(angle)
    cropped_im = diagonal_crop.crop(img, (x1,y1), angle, height, width)
    return cropped_im



def main(base_path, db_fname):
    db = h5py.File(db_fname, 'r')
    dsets = sorted(db['data'].keys())
    print "total number of images : ", colorize(Color.RED, len(dsets), highlight=True)
    for k in dsets:
        rgb = db['data'][k][...]
        charBB = db['data'][k].attrs['charBB']
        wordBB = db['data'][k].attrs['wordBB']
	print wordBB
        txt = db['data'][k].attrs['txt']

        crop_boxes(base_path, k, rgb, wordBB)
        print "image name        : ", colorize(Color.RED, k, bold=True)
        print "  ** no. of chars : ", colorize(Color.YELLOW, charBB.shape[-1])
        print "  ** no. of words : ", colorize(Color.YELLOW, wordBB.shape[-1])
        print "  ** text         : ", colorize(Color.GREEN, txt)

        if 'q' in raw_input("next? ('q' to exit) : "):
            break
    db.close()

if __name__=='__main__':
    main('results/cropped/','results/SynthText.h5')

