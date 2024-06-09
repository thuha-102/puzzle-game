from re import T
import minmax
import xlrd
import random
from xlutils.copy import copy


def encode(table):
    # 1 --> 2
    # 0 --> 1
    # -1 --> 0
    result=0
    for i in range(5):
        for j in range(5):
            result+=(table[i][j]+1)* (3**(i*5+j))
    return result

def main(player):
    minmax.board()
    boardlist=[(minmax.dupTable(minmax.board.current_board))]
    minmax.board.turn=player
    for i in range(100):
        valid_moves=minmax.board.get_valid_moves(minmax.board.current_board,minmax.board.previous_board,minmax.board.turn)
        if len(valid_moves)==0: break
        random.seed()
        move=valid_moves[random.randint(0,len(valid_moves)-1)]
        previous_board=minmax.board.copy_board(minmax.board.current_board)
        minmax.board.act_move(minmax.board.current_board,move,minmax.board.turn)
        boardlist.append(minmax.dupTable(minmax.board.current_board))
        minmax.board.turn=-minmax.board.turn
        minmax.board.previous_board=minmax.board.copy_board(previous_board)
    score=0
    for i in range(5):
        for j in range(5):
            if(minmax.board.current_board[i][j]==1): score-=1
            elif(minmax.board.current_board[i][j]==-1): score+=1
    if(score>0): win=-1
    elif(score<0): win=1
    else: win=0
    boardict ={}
    for x in range(len(boardlist)):
        if str(encode(boardlist[x])) in boardict.keys():
            if win==1:
                if x%2==0: boardict[str(encode(boardlist[x]))][0]+=1
                else: boardict[str(encode(boardlist[x]))][1]+=1
            else:
                if x%2==0: boardict[str(encode(boardlist[x]))][1]+=1
                else: boardict[str(encode(boardlist[x]))][0]+=1
        else:
            if win==1:
                if x%2==0: boardict[str(encode(boardlist[x]))]=[1,0]
                else: boardict[str(encode(boardlist[x]))]=[0,1]
            else:
                if x%2==0: boardict[str(encode(boardlist[x]))]=[0,1]
                else: boardict[str(encode(boardlist[x]))]=[1,0]
    if len(boardict)==1: raise Exception("Bad")
    for x in boardict.keys():
        wb = xlrd.open_workbook("trainingset.xls")
        nwb = copy(wb)
        s=wb.sheet_by_index(0)
        ns = nwb.get_sheet(0)
        check=False
        i=0
        while i<s.nrows:
            if s.cell_value(i,0)==x:
                check=True
                break
            else: i+=1
        if check:
            ns.write(i,1,int(s.cell_value(i,1))+boardict[x][0])
            ns.write(i,2,int(s.cell_value(i,2))+boardict[x][1])
        else:
            ns.write(s.nrows,0,x)
            ns.write(s.nrows,1,boardict[x][0])
            ns.write(s.nrows,2,boardict[x][1])
        nwb.save("trainingset.xls")
for a in range(100000):
    main(1)
    print(a)
for a in range(100000):
    main(-1)
    print(a)