#!/usr/bin/env python
# coding: utf-8
import copy
import crash_on_ipy
# 棋盘信息设置
# 棋盘大小
MAP_WIDTH = 6
MAP_HEIGHT = 6
# 目标棋子的目标坐标
TARGET_POS_X = 4
TARGET_POS_Y = 2

# 宏定义区
DIR_UP = 1
DIR_DOWM = 2
DIR_LEFT = 4
DIR_RIGHT = 8

DIR_LR = DIR_LEFT | DIR_RIGHT
DIR_UD = DIR_UP | DIR_DOWM

def LOG_DEBUG(string):
    print "DEBUG:"+str(string)

# 判断是否可以向上下左右走
def getUpDistance(Map,Block):
    Min = Block.y - 0
    if Min == 0:
        return Min
    for current_block in Map.blockList:
        current_block_left = current_block.x
        current_block_right = current_block.x + current_block.width
        current_block_up = current_block.y
        current_block_bottem = current_block.y + current_block.height
        Block_left =  Block.x
        Block_right = Block.x + Block.width
        Block_up = Block.y
        Block_bottem = Block.y + Block.height
        if  current_block_left < Block_right and current_block_right > Block_left and current_block_bottem <= Block_up :
            up_distance =  Block_up - current_block_bottem
            # LOG_DEBUG('current_block_pos='+str(current_block_left)+str(current_block_up)+' Block_Pos='+str(Block_left)+str(Block_up)\
            #                             +' distance='+ str(up_distance) )
            if up_distance < Min:
                Min = up_distance
    return Min
def getDownDistance(Map,Block):
    Min = MAP_HEIGHT - ( Block.y + Block.height )
    if Min == 0:
        return Min
    for current_block in Map.blockList:
        current_block_left = current_block.x
        current_block_right = current_block.x + current_block.width
        current_block_up = current_block.y
        current_block_bottem = current_block.y + current_block.height
        Block_left =  Block.x
        Block_right = Block.x + Block.width
        Block_up = Block.y
        Block_bottem = Block.y + Block.height 
        if  current_block_left < Block_right and current_block_right > Block_left and current_block_up >= Block_bottem :
            down_distance =  current_block_up - Block_bottem
            # LOG_DEBUG('current_block_pos='+str(current_block_left)+str(current_block_up)+' Block_Pos='+str(Block_left)+str(Block_up)\
            #                             +' distance='+ str(down_distance) )
            if down_distance < Min:
                Min = down_distance
    return Min
def getLeftDistance(Map,Block):
    Min = Block.x - 0
    if Min == 0:
        return Min
    for current_block in Map.blockList:
        current_block_left = current_block.x
        current_block_right = current_block.x + current_block.width
        current_block_up = current_block.y
        current_block_bottem = current_block.y + current_block.height
        Block_left =  Block.x
        Block_right = Block.x + Block.width
        Block_up = Block.y
        Block_bottem = Block.y + Block.height 
        if  current_block_up < Block_bottem and current_block_bottem > Block_up and current_block_right <= Block_left :
            left_distance =  Block_left - current_block_right
            # LOG_DEBUG('current_block_pos='+str(current_block_left)+str(current_block_up)+' Block_Pos='+str(Block_left)+str(Block_up)\
            #                             +' left_distance='+ str(left_distance) )
            if left_distance < Min:
                Min = left_distance
    return Min

def getRightDistance(Map,Block):
    Min = MAP_WIDTH - ( Block.x + Block.width )
    if Min == 0:
        return Min
    for current_block in Map.blockList:
        current_block_left = current_block.x
        current_block_right = current_block.x + current_block.width
        current_block_up = current_block.y
        current_block_bottem = current_block.y + current_block.height
        Block_left =  Block.x
        Block_right = Block.x + Block.width
        Block_up = Block.y
        Block_bottem = Block.y + Block.height 
        if  current_block_up < Block_bottem and current_block_bottem > Block_up and current_block_left >= Block_right :
            right_distance =  current_block_left - Block_right
            if right_distance < Min:
                Min = right_distance
    return Min

def isTargetMap(Map):
    for current_block in Map.blockList:
        if current_block.isTargetblock == True:
            if current_block.x == TARGET_POS_X and current_block.y == TARGET_POS_Y:
                return True
            else:
                return False

class Map(object):
    """docstring for Map"""
    def __init__(self):
        self.blockList = list()
        self.lastMapHash = None
        self.howToMove = ''
class Block(object):
    def __init__(self, x, y, width, height, direction, isTargetblock = False):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.isTargetblock = isTargetblock
        self.direction = direction

def mirrorMap(Map):
    newMap = copy.deepcopy(Map)
    AXIS_X = ( MAP_WIDTH - 0 )/2
    AXIS_Y = ( MAP_HEIGHT - 0 )/2
    for current_block in newMap.blockList:
        current_block.x =  AXIS_X + ( AXIS_X - ( current_block.x + current_block.width ))
        current_block.y =  AXIS_Y + ( AXIS_Y - ( current_block.y + current_block.height ))
    return  newMap

def encodeMap(Map):
    encodeList = list()
    result_str = ''
    for current_block in Map.blockList:
        encodeString =  str(current_block.x)  + str(current_block.y) + str(current_block.width) + str(current_block.height) + ' '
        encodeList.append(encodeString)
    encodeList.sort()
    for current_str in encodeList:
        result_str += current_str
    return result_str
def getMoveString(from_block,to_block):
    return 'Move '+ str(from_block.x) + ',' + str(from_block.y) + ' To ' + str(to_block.x) + ',' + str(to_block.y)

def printSolution( Map_hash , Map):
    current_map = Map
    while current_map.lastMapHash != None:
        print current_map.howToMove
        current_map = Map_hash[current_map.lastMapHash]
    print current_map.howToMove
    return
#广度优先搜索 BFS
def broadFirstSearch(startMap):
    #while 不是队列末尾
    mapList = list()
    map_hash = dict()
    mapList.append(startMap)
    map_hash[encodeMap(startMap)] = startMap
    for current_map in mapList:
        LOG_DEBUG(encodeMap(current_map)+' current_map')
        #for 每一个块
        for current_block_index in xrange(len(current_map.blockList)):
            for current_direction in [DIR_UP,DIR_DOWM,DIR_LEFT,DIR_RIGHT]:
                if current_direction == DIR_UP:
                    if current_map.blockList[current_block_index].direction & DIR_UP == 0:
                        continue
                    up_distance = getUpDistance(current_map, current_map.blockList[current_block_index])
                    if up_distance > 0:
                        newMap = copy.deepcopy(current_map)
                        newMap.blockList[current_block_index].y -= up_distance
                        newMap.howToMove = getMoveString(current_map.blockList[current_block_index] ,newMap.blockList[current_block_index])
                    else:
                        continue
                if current_direction == DIR_DOWM:
                    if current_map.blockList[current_block_index].direction & DIR_DOWM == 0:
                        continue
                    down_distance = getDownDistance(current_map,current_map.blockList[current_block_index])
                    if down_distance > 0:
                        newMap = copy.deepcopy(current_map)
                        newMap.blockList[current_block_index].y += down_distance
                        newMap.howToMove = getMoveString(current_map.blockList[current_block_index] ,newMap.blockList[current_block_index])
                    else:
                        continue
                if current_direction == DIR_LEFT: 
                    if current_map.blockList[current_block_index].direction & DIR_LEFT == 0:
                        continue
                    left_distance = getLeftDistance(current_map,current_map.blockList[current_block_index])
                    if left_distance > 0:
                        newMap = copy.deepcopy(current_map)
                        newMap.blockList[current_block_index].x -= left_distance
                        newMap.howToMove = getMoveString(current_map.blockList[current_block_index] ,newMap.blockList[current_block_index])
                    else:
                        continue
                if current_direction == DIR_RIGHT:
                    if current_map.blockList[current_block_index].direction & DIR_RIGHT == 0:
                        continue
                    right_distance = getRightDistance(current_map,current_map.blockList[current_block_index])
                    if right_distance > 0:
                        newMap = copy.deepcopy(current_map)
                        newMap.blockList[current_block_index].x += right_distance
                        newMap.howToMove = getMoveString(current_map.blockList[current_block_index] ,newMap.blockList[current_block_index])
                    else:
                        continue
                newMap.lastMapHash = encodeMap(current_map)
                #if 当前棋盘样式符合最终答案
                    #输出解法
                #if 当前棋盘样式未出现过 && 对称的棋盘样式未出现过 && 不与父节点相同
                    #添加该棋盘样式至队列末尾
                    #添加该棋盘样式至样式哈希表中
                #else:
                    #不添加
                if map_hash.has_key(encodeMap(newMap)) == False and map_hash.has_key(encodeMap(mirrorMap(newMap))) == False \
                                                            and encodeMap(newMap) != encodeMap(current_map):
                    mapList.append(newMap)
                    LOG_DEBUG(newMap.howToMove)
                    LOG_DEBUG(encodeMap(newMap)+' desc=add_to_mapList')
                    map_hash[encodeMap(newMap)] = newMap

                if isTargetMap(newMap):
                    LOG_DEBUG('Sucess!!')
                    printSolution(map_hash,newMap)
                    return
    LOG_DEBUG('loop_over')

if __name__ == '__main__':
    startMap=Map()
    startMap.blockList.append(Block(0,0,1,2,DIR_UD))
    startMap.blockList.append(Block(1,0,2,1,DIR_LR))
    startMap.blockList.append(Block(1,1,2,1,DIR_LR))
    startMap.blockList.append(Block(0,2,2,1,DIR_LR,True))
    startMap.blockList.append(Block(2,2,1,2,DIR_UD))
    startMap.blockList.append(Block(2,4,1,2,DIR_UD))
    startMap.blockList.append(Block(3,0,1,3,DIR_UD))
    startMap.blockList.append(Block(4,0,1,2,DIR_UD))
    startMap.blockList.append(Block(4,2,1,2,DIR_UD))
    # startMap.blockList.append(Block(4,4,2,1,DIR_LR))
    broadFirstSearch(startMap)
    # print getUpDistance(startMap,Block(1,2,1,3))
