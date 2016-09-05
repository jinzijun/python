#!/usr/bin/env python
# coding: utf-8

from PIL import Image
import sys
from pylab import *
import math
import numpy
import copy

#PIC setting
PIC_X = 0 
PIC_Y = 463
PIC_WIDTH = 720
PIC_HEIGHT = 720

#thubnial pic setting
THUMBNAIL_WIDTH = 15
THUMBNAIL_HEIGHT = 15

MAP_ROW_NUM =10
MAP_COLUMN_NUM = 10
BLOCK_WIDTH = 72

class Map(object):
    """docstring for Map"""
    def __init__(self, score=0):
        self.inner_map = dict()
        self.score = score
        self.howToClick = ''
        self.check_dict = dict()
        self.left_num = MAP_ROW_NUM*MAP_COLUMN_NUM
        self.click_times = 0

def getColorByRGB(r,g,b):
    allowed_bias = 5
    if abs(r - 193) < allowed_bias and abs(g - 67) < allowed_bias and abs(b - 95) < allowed_bias:
        return 'r'
    if abs(r - 162) < allowed_bias and abs(g - 62) < allowed_bias and abs(b - 212) < allowed_bias:
        return 'p'
    if abs(r - 70) < allowed_bias and abs(g - 165) < allowed_bias and abs(b - 215) < allowed_bias:
        return 'b'
    if abs(r - 92) < allowed_bias and abs(g - 174) < allowed_bias and abs(b - 41) < allowed_bias:
        return 'g'
    if abs(r - 213) < allowed_bias and abs(g - 158) < allowed_bias and abs(b - 35) < allowed_bias:
        return 'y'
def showMap(inner_map):
    for current_row in xrange(MAP_ROW_NUM):
        for current_column in xrange(MAP_COLUMN_NUM):
            print inner_map[(MAP_ROW_NUM-1-current_row,current_column)]+' ',
        print ''

def adjustMap(inner_map):
    #move down debug:sucess
    for current_column in xrange(MAP_COLUMN_NUM):
        for current_row in xrange(MAP_ROW_NUM):
            if inner_map[(current_row,current_column)] != '0':
                continue
            i = current_row + 1
            j = current_row
            while i<MAP_ROW_NUM and inner_map[(i,current_column)] == '0':
                    i += 1
            if i == MAP_ROW_NUM:
                continue
            while j<MAP_ROW_NUM:
                if i<MAP_ROW_NUM:
                    inner_map[(j,current_column)] = inner_map[(i,current_column)]
                else:
                    inner_map[(j,current_column)] = '0'
                i += 1
                j += 1
    #move left
    for current_column in xrange(MAP_COLUMN_NUM):
        if inner_map[(0,current_column)] != '0':
                continue
        i = current_column+1
        j = current_column
        while i<MAP_COLUMN_NUM and inner_map[(0,i)] == '0':
            i += 1
        if i == MAP_COLUMN_NUM:
            continue

        while j<MAP_COLUMN_NUM:
            for x in xrange(MAP_ROW_NUM):
                if i<MAP_COLUMN_NUM:
                    inner_map[(x,j)] = inner_map[(x,i)]
                else:
                    inner_map[(x,j)] = '0'
            i += 1
            j += 1



def getMapFromImage(image_path):

    output_inner_map = dict()
    img = Image.open(image_path).convert('RGB')
    region = (PIC_X,PIC_Y,PIC_X + PIC_WIDTH,PIC_Y + PIC_HEIGHT)
    cropImg = img.crop(region)

    for current_row in xrange(MAP_ROW_NUM):
        for current_column in xrange(MAP_COLUMN_NUM):
            current_region = (current_column * BLOCK_WIDTH ,current_row * BLOCK_WIDTH ,(current_column+1) * BLOCK_WIDTH ,(current_row+1) * BLOCK_WIDTH)
            current_block_img = cropImg.crop(current_region)
            current_block_img.thumbnail((THUMBNAIL_WIDTH,THUMBNAIL_HEIGHT))
            pix = current_block_img.load()
            r_list = list()
            g_list = list()
            b_list = list()
            for x in xrange(THUMBNAIL_HEIGHT):
                for y in xrange(THUMBNAIL_WIDTH):
                    r,g,b = pix[x,y]
                    r_list.append(r)
                    g_list.append(g)
                    b_list.append(b)
            current_block_r = int(numpy.mean(r_list))
            current_block_g = int(numpy.mean(g_list))
            current_block_b = int(numpy.mean(b_list))
            current_block_img.close()
            output_inner_map[(MAP_ROW_NUM-current_row-1,current_column)] = getColorByRGB(current_block_r,current_block_g,current_block_b)
        #     print   output_inner_map[(MAP_ROW_NUM-current_row-1,current_column)],
        # print ''
    cropImg.close()
    img.close()
    return output_inner_map
def getMapByClick(Map,Row,Column):

    disappear_block_list = list()
    new_map = copy.deepcopy(Map)
    disappear_block_list.append((Row,Column))
    color = Map.inner_map[(Row,Column)] 
    disappear_block_dict = dict()
    disappear_block_dict[(Row,Column)] = 1 
    for current_row,current_column in disappear_block_list:
        #up
        if current_row+1<MAP_ROW_NUM \
            and disappear_block_dict.has_key((current_row+1,current_column)) == False \
            and Map.inner_map[(current_row+1,current_column)] == color:
            disappear_block_list.append( (current_row+1,current_column) )
            disappear_block_dict[(current_row+1,current_column)] = 1
        #down
        if current_row-1 >= 0 \
            and disappear_block_dict.has_key((current_row-1,current_column)) == False \
            and Map.inner_map[(current_row-1,current_column)] == color:
            disappear_block_list.append( (current_row-1,current_column) )
            disappear_block_dict[(current_row-1,current_column)] = 1
        #left
        if current_column-1 >= 0 \
            and disappear_block_dict.has_key((current_row,current_column-1)) == False \
            and Map.inner_map[(current_row,current_column-1)] == color:
            disappear_block_list.append( (current_row,current_column-1) )
            disappear_block_dict[(current_row,current_column-1)] = 1
        #right
        if current_column+1<MAP_COLUMN_NUM \
            and disappear_block_dict.has_key((current_row,current_column+1)) == False \
            and Map.inner_map[(current_row,current_column+1)] == color:
            disappear_block_list.append( (current_row,current_column+1) )
            disappear_block_dict[(current_row,current_column+1)] = 1
        # #left up
        # if (current_row+1 < MAP_ROW_NUM and current_column-1 >= 0) \
        # and disappear_block_dict.has_key((current_row+1,current_column-1)) == False \
        # and Map.inner_map[(current_row+1,current_column-1)] == color:
        #     disappear_block_list.append( (current_row+1,current_column-1) )
        #     disappear_block_dict[(current_row+1,current_column-1)] = 1
        # #right up
        # if (current_row-1 >= 0 and current_column+1 < MAP_COLUMN_NUM )\
        #     and disappear_block_dict.has_key((current_row-1,current_column+1)) == False \
        #     and Map.inner_map[(current_row-1,current_column+1)] == color:
        #     disappear_block_list.append( (current_row-1,current_column+1) )
        #     disappear_block_dict[(current_row-1,current_column+1)] = 1
        # #left down
        # if ( current_row-1 >=0 and  current_column-1 >= 0 )\
        #     and disappear_block_dict.has_key((current_row-1,current_column-1)) == False \
        #     and Map.inner_map[(current_row-1,current_column-1)] == color:
        #     disappear_block_list.append( (current_row-1,current_column-1) )
        #     disappear_block_dict[(current_row-1,current_column-1)] = 1
        # #right down
        # if ( current_row-1 >=0 and current_column+1 < MAP_COLUMN_NUM )\
        #     and disappear_block_dict.has_key((current_row-1,current_column+1)) == False \
        #     and Map.inner_map[(current_row-1,current_column+1)] == color:
        #     disappear_block_list.append( (current_row-1,current_column+1) )
        #     disappear_block_dict[(current_row-1,current_column+1)] = 1

    if len(disappear_block_list) < 2:
        return None
    # #debug
    # print disappear_block_list
    for pos in disappear_block_list:
        Map.check_dict[pos] = 1

    new_map.check_dict.clear()
    new_map.score += 5*len(disappear_block_list)*len(disappear_block_list)
    new_map.left_num -= len(disappear_block_list)
    new_map.howToClick += "("+str(Row)+","+str(Column)+","+str(color)+"*"+str(len(disappear_block_list))+")"
    new_map.click_times += 1
    for pos in disappear_block_list:
        new_map.inner_map[pos] = '0'
    #TODO:调整棋盘
    adjustMap(new_map.inner_map)
    return new_map


def broadFirstSearch(start_map,depth=10):
    map_list = list()
    map_list.append(start_map)
    max_score = 0
    best_solution = ''
    for current_map in map_list:
        start_map_num=len(map_list)
        for current_row in xrange(MAP_ROW_NUM):
            for current_column in xrange(MAP_COLUMN_NUM):
                if current_map.inner_map[(current_row,current_column)] == '0':
                    continue
                if current_map.check_dict.has_key((current_row,current_column)) == True:
                    continue
                if current_map.click_times >= depth:
                    if current_map.score>max_score:
                        max_score = current_map.score
                        best_solution = current_map.howToClick
                    continue
                new_map = getMapByClick(current_map,current_row,current_column)
                if new_map != None:
                    map_list.append(new_map)
        # diff_num = len(map_list) - start_map_num
        # if diff_num == 0 or current_map.click_times >= depth:
            # current_map.score += 2000 - 20*current_map.left_num*current_map.left_num
            
    print "score="+str(max_score)
    print "best_solution="+str(best_solution)
    


def main():

    image_path = sys.argv[1]
    start_map = Map(0)
    start_map.inner_map = getMapFromImage(image_path)
    # showMap(start_map.inner_map)
    # new_map = getMapByClick(start_map,7,4)
    # print '----------------after--------------'
    # if new_map == None:
    #     print 'None'
    # else:
    #     showMap(new_map.inner_map)
    # print "score"+str(new_map.score)
    # print "solution"+str(new_map.howToClick)
    
    #debug:getMapFromImage success
    #debug:showMap success
    
    broadFirstSearch(start_map,3)
    return

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print 'missing file path.'
        sys.exit()
    main()