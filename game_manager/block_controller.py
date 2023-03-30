#!/usr/bin/python3
# -*- coding: utf-8 -*-

from datetime import datetime
import pprint
import copy

class Block_Controller(object):

    # init parameter
    board_backboard = 0
    board_data_width = 0
    board_data_height = 0
    ShapeNone_index = 0
    CurrentShape_class = 0
    NextShape_class = 0

    # GetNextMove is main function.
    # input
    #    nextMove : nextMove structure which is empty.
    #    GameStatus : block/field/judge/debug information. 
    #                 in detail see the internal GameStatus data.
    # output
    #    nextMove : nextMove structure which includes next shape position and the other.
    def GetNextMove(self, nextMove, GameStatus):

        t1 = datetime.now()

        #
        # Challenge Flag Setting
        #   FourLineStrategy
        #       True  : Try deleting four lines
        #       False : Normal Mode
        #
        FourLineStrategy = False
        UseHoldFunction = True

        # print GameStatus
        print("=================================================>")
        pprint.pprint(GameStatus, width = 61, compact = True)

        # get data from GameStatus
        # current shape info
        CurrentShapeDirectionRange = GameStatus["block_info"]["currentShape"]["direction_range"]
        CurrentShapeIndex = GameStatus["block_info"]["currentShape"]["index"]
        self.CurrentShape_class = GameStatus["block_info"]["currentShape"]["class"]
        # next shape info
        NextShapeDirectionRange = GameStatus["block_info"]["nextShape"]["direction_range"]
        self.NextShape_class = GameStatus["block_info"]["nextShape"]["class"]
        # current board info
        self.board_backboard = GameStatus["field_info"]["backboard"]
        # default board definition
        self.board_data_width = GameStatus["field_info"]["width"]
        self.board_data_height = GameStatus["field_info"]["height"]
        self.ShapeNone_index = GameStatus["debug_info"]["shape_info"]["shapeNone"]["index"]
        # hold shape info
        HoldShapeDirectionRange = GameStatus["block_info"]["holdShape"]["direction_range"]
        HoldShapeIndex = GameStatus["block_info"]["holdShape"]["index"]
        HoldShape_class = GameStatus["block_info"]["holdShape"]["class"]
        # temporary shape info
        tempShapeDirectionRange = CurrentShapeDirectionRange
        tempShapeIndex = CurrentShapeIndex
        tempShape_class = self.CurrentShape_class

        # 最初に Hold をした(Holdが空だったか)を示すフラグ
        FirstHoldExecution = False

        # がっつりモードで Hold 機能有効の時だけ、
        # Iミノがきれいに収まりそうな時(Iミノを積極的に使う):
        #   Hold のミノが I の時:
        #     CurrentShape が I ミノじゃないとき:
        #       I ミノを Hold から出してくる
        #     CurrentShape が I ミノの時：
        #       Hold ミノはそのまま Hold しておいて CurrentShape の Iミノを使う
        #   Hold ミノが I以外 (I以外のミノか、Hold が無い場合)：
        #     どうしようもないのでそのまま
        # がっつり埋まりそうじゃないとき(IミノをできるだけHoldしておく)
        #   CurrentShape が I の時：
        #     Hold が I 以外の時：
        #       IをHoldする
        #     Hold が I の時：
        #       もう I が Hold されてるのでそのまま
        #   CurrentShape が Ｉ じゃないとき：
        #     当然ながらそのまま

        # I ミノが縦に収まりそうな空きがあるかチェックする
        # 時間がかかるかどうかチェックしたいのでモードに関わらずチェックするようにする
        # ほぼ calcEvaluationValueSample からのコピペで恥ずかしいけど我慢
        width = self.board_data_width
        height = self.board_data_height
        ## まずは各列の高さを求める
        BlockMaxY = [0] * width
        ### check back board (ミノを置く前のボード)
        # each y line
        for y in range(height - 1, 0, -1):
            hasHole = False
            hasBlock = False
            # each x line
            for x in range(width):
                ## check if hole or block..
                if self.board_backboard[y * self.board_data_width + x] != self.ShapeNone_index:
                    BlockMaxY[x] = height - y                # update blockMaxY

        ### 各列の高さから、へこみがあるかチェック
        highGap = 3 # Gap があると認識する高さの差
        onlyOneColumnSpace = False  # 1列だけの空きがあるかどうかを示すフラグ
        lefthight = height # 注目列の左列の高さ。列0は左端なので最大の高さを入れておく
        switchHold = 'n' # Hold をswichするかどうかのフラグ
        for i in range(width - 1):
            if lefthight - BlockMaxY[i] >= highGap:
                # へこんでる
                if i == width - 1: # 右端だったら I ミノが縦に収まる
                    onlyOneColumnSpace = True
                else:
                    if BlockMaxY[i+1] -  BlockMaxY[i] >= highGap:
                        # すぐまた立ち上がっている時は I ミノが縦に収まる
                        onlyOneColumnSpace = True
            else:
                # へこんでないときは次の列チェックにそなえて比較用の左列高さにいまの高さを入れる
                lefthight = BlockMaxY[i]
        #
        if UseHoldFunction == True:
            if onlyOneColumnSpace == True:
                if HoldShapeIndex == 1:
                    if CurrentShapeIndex != 1:
                        # Hold から I ミノを出す
                        switchHold = 'y'
                        tempShapeDirectionRange = CurrentShapeDirectionRange
                        tempShapeIndex = CurrentShapeIndex
                        tempShape_class = self.CurrentShape_class
                        CurrentShapeDirectionRange = HoldShapeDirectionRange
                        CurrentShapeIndex = HoldShapeIndex
                        self.CurrentShape_class = HoldShape_class
                        HoldShapeDirectionRange = tempShapeDirectionRange
                        HoldShapeIndex = tempShapeIndex
                        HoldShape_class = tempShape_class
                    else:
                        pass
                else:
                    if HoldShapeIndex == None:
                        FirstHoldExecution = True
                    else:
                        pass
            else:
                if CurrentShapeIndex == 1:
                    if HoldShapeIndex != 1:
                        if HoldShapeIndex == None:
                            FirstHoldExecution = True
                        #  I ミノ を Holdに入れる
                        switchHold = 'y'
                        tempShapeDirectionRange = CurrentShapeDirectionRange
                        tempShapeIndex = CurrentShapeIndex
                        tempShape_class = self.CurrentShape_class
                        CurrentShapeDirectionRange = HoldShapeDirectionRange
                        CurrentShapeIndex = HoldShapeIndex
                        self.CurrentShape_class = HoldShape_class
                        HoldShapeDirectionRange = tempShapeDirectionRange
                        HoldShapeIndex = tempShapeIndex
                        HoldShape_class = tempShape_class
                    else:
                        pass # IミノHold 済のため、そのまま
                else:
                    pass

        # search best nextMove -->
        strategy = None
        LatestEvalValue = -100000

        if FirstHoldExecution == False:
            # number of holes before putting tetrimino
            RetArray = self.calcEvaluationValueSample(self.board_backboard, 0)
            Holes_wo_NewTetrimino = RetArray[1]

            # search with current block Shape
            for direction0 in CurrentShapeDirectionRange:
                # search with x range
                x0Min, x0Max = self.getSearchXRange(self.CurrentShape_class, direction0)
                for x0 in range(x0Min, x0Max):
                    # get board data, as if dropdown block
                    board = self.getBoard(self.board_backboard, self.CurrentShape_class, direction0, x0)

                    # evaluate board
                    RetArray = self.calcEvaluationValueSample(board, Holes_wo_NewTetrimino)
                    EvalValue = RetArray[0]
                    print(x0, x0Max-1, CurrentShapeIndex, direction0)
                    if FourLineStrategy and x0 == (x0Max-1) and not (CurrentShapeIndex == 1 and direction0 == 0):
                        EvalValue = EvalValue - 100
                        print ("Hello")
                        print(EvalValue)
                    if EvalValue > LatestEvalValue:
                        strategy = (direction0, x0, 1, 1, 'n')
                        # Hold機能使用時に再利用するために保存しておく
                        savdirection0 = direction0
                        savx0 = x0
                        LatestEvalValue = EvalValue
            
                    ###test
                    ###for direction1 in NextShapeDirectionRange:
                    ###  x1Min, x1Max = self.getSearchXRange(self.NextShape_class, direction1)
                    ###  for x1 in range(x1Min, x1Max):
                    ###        board2 = self.getBoard(board, self.NextShape_class, direction1, x1)
                    ###        EvalValue = self.calcEvaluationValueSample(board2)
                    ###        if EvalValue > LatestEvalValue:
                    ###            strategy = (direction0, x0, 1, 1)
                    ###            LatestEvalValue = EvalValue
            # search best nextMove <--

            nextMove["strategy"]["direction"] = strategy[0]
            nextMove["strategy"]["x"] = strategy[1]
            nextMove["strategy"]["y_operation"] = strategy[2]
            nextMove["strategy"]["y_moveblocknum"] = strategy[3]
            nextMove["strategy"]["use_hold_function"] = switchHold
        else:
            nextMove["strategy"]["direction"] = 0
            nextMove["strategy"]["x"] = 0
            nextMove["strategy"]["y_operation"] = 0
            nextMove["strategy"]["y_moveblocknum"] = 0
            nextMove["strategy"]["use_hold_function"] = switchHold

        print("===", datetime.now() - t1)
        print(nextMove)
        print("###### SAMPLE CODE ######")
            
        
        return nextMove

    def getSearchXRange(self, Shape_class, direction):
        #
        # get x range from shape direction.
        #
        minX, maxX, _, _ = Shape_class.getBoundingOffsets(direction) # get shape x offsets[minX,maxX] as relative value.
        xMin = -1 * minX
        xMax = self.board_data_width - maxX
        return xMin, xMax

    def getShapeCoordArray(self, Shape_class, direction, x, y):
        #
        # get coordinate array by given shape.
        #
        coordArray = Shape_class.getCoords(direction, x, y) # get array from shape direction, x, y.
        return coordArray

    def getBoard(self, board_backboard, Shape_class, direction, x):
        # 
        # get new board.
        #
        # copy backboard data to make new board.
        # if not, original backboard data will be updated later.
        board = copy.deepcopy(board_backboard)
        _board = self.dropDown(board, Shape_class, direction, x)
        return _board

    def dropDown(self, board, Shape_class, direction, x):
        # 
        # internal function of getBoard.
        # -- drop down the shape on the board.
        # 
        dy = self.board_data_height - 1
        coordArray = self.getShapeCoordArray(Shape_class, direction, x, 0)
        # update dy
        for _x, _y in coordArray:
            _yy = 0
            while _yy + _y < self.board_data_height and (_yy + _y < 0 or board[(_y + _yy) * self.board_data_width + _x] == self.ShapeNone_index):
                _yy += 1
            _yy -= 1
            if _yy < dy:
                dy = _yy
        # get new board
        _board = self.dropDownWithDy(board, Shape_class, direction, x, dy)
        return _board

    def dropDownWithDy(self, board, Shape_class, direction, x, dy):
        #
        # internal function of dropDown.
        #
        _board = board
        coordArray = self.getShapeCoordArray(Shape_class, direction, x, 0)
        for _x, _y in coordArray:
            _board[(_y + dy) * self.board_data_width + _x] = Shape_class.shape
        return _board

    def calcEvaluationValueSample(self, board, holesWOtetrimino):
        #
        # sample function of evaluate board.
        #
        width = self.board_data_width
        height = self.board_data_height

        # evaluation paramters
        ## lines to be removed
        fullLines = 0
        ## number of holes or blocks in the line.
        nHoles, nIsolatedBlocks = 0, 0
        ## absolute differencial value of MaxY
        absDy = 0
        ## how blocks are accumlated
        BlockMaxY = [0] * width
        holeCandidates = [0] * width
        holeConfirm = [0] * width

        ### check board
        # each y line
        for y in range(height - 1, 0, -1):
            hasHole = False
            hasBlock = False
            # each x line
            for x in range(width):
                ## check if hole or block..
                if board[y * self.board_data_width + x] == self.ShapeNone_index:
                    # hole
                    hasHole = True
                    holeCandidates[x] += 1  # just candidates in each column..
                else:
                    # block
                    hasBlock = True
                    BlockMaxY[x] = height - y                # update blockMaxY
                    if holeCandidates[x] > 0:
                        holeConfirm[x] += holeCandidates[x]  # update number of holes in target column..
                        holeCandidates[x] = 0                # reset
                    if holeConfirm[x] > 0:
                        nIsolatedBlocks += 1                 # update number of isolated blocks

            if hasBlock == True and hasHole == False:
                # filled with block
                fullLines += 1
            elif hasBlock == True and hasHole == True:
                # do nothing
                pass
            elif hasBlock == False:
                # no block line (and ofcourse no hole)
                pass

        # nHoles
        for x in holeConfirm:
            nHoles += abs(x)

        ### absolute differencial value of MaxY
        BlockMaxDy = []
        for i in range(len(BlockMaxY) - 1):
            val = BlockMaxY[i] - BlockMaxY[i+1]
            BlockMaxDy += [val]
        for x in BlockMaxDy:
            absDy += abs(x)

        #### maxDy
        #maxDy = max(BlockMaxY) - min(BlockMaxY)
        #### maxHeight
        #maxHeight = max(BlockMaxY) - fullLines

        ## statistical data
        #### stdY
        #if len(BlockMaxY) <= 0:
        #    stdY = 0
        #else:
        #    stdY = math.sqrt(sum([y ** 2 for y in BlockMaxY]) / len(BlockMaxY) - (sum(BlockMaxY) / len(BlockMaxY)) ** 2)
        #### stdDY
        #if len(BlockMaxDy) <= 0:
        #    stdDY = 0
        #else:
        #    stdDY = math.sqrt(sum([y ** 2 for y in BlockMaxDy]) / len(BlockMaxDy) - (sum(BlockMaxDy) / len(BlockMaxDy)) ** 2)


        # calc Evaluation Value
        holesDiff_w_wo_tetrimino = nHoles - holesWOtetrimino

        score = 0
        score = score + fullLines * 10.0           # try to delete line 
        score = score - nHoles * 3.0               # try not to make hole
        score = score - nIsolatedBlocks * 3.0      # try not to make isolated block
        score = score - absDy * 2.0                # try to put block smoothly
        score = score - holesDiff_w_wo_tetrimino * 20.0 # try to reduce new holes 

        #score = 0
        #score = score + fullLines * 10.0           # try to delete line 
        #score = score - nHoles * 1.0               # try not to make hole
        #score = score - nIsolatedBlocks * 8.0      # try not to make isolated block
        #score = score - absDy * 1.0                # try to put block smoothly
        #score = score - holesDiff_w_wo_tetrimino * 20.0
        #score = score - maxDy * 0.3                # maxDy
        #score = score - maxHeight * 5              # maxHeight
        #score = score - stdY * 1.0                 # statistical data
        #score = score - stdDY * 0.01               # statistical data

        # print(score, fullLines, nHoles, nIsolatedBlocks, maxHeight, stdY, stdDY, absDy, BlockMaxY)
        print(score, fullLines, nHoles, nIsolatedBlocks, absDy, BlockMaxY)
        # print (score)
        return score, nHoles


BLOCK_CONTROLLER = Block_Controller()
