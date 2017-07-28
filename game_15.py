# permutation: [a[1],...,a[k]] where {a[1],..,a[k]}={0,1,2,...,k-1}

# is a permutation
def is_perm (perm):
  k=len(perm)
  return (frozenset(perm)==frozenset(range(k)))

# identity permutation
def id(k):
  return list(range(k))

# product of two permutations
def prod(first,second):
  assert is_perm (first)
  assert is_perm (second)
  assert (len(first)==len(second))
  return [second[first[i]] for i in range(len(first))]

# trans(i,j,n): permutation of length n exchanging i and j
def trans(i,j,n):
  assert (0<=i)
  assert (i<n)
  assert (0<=j)
  assert (j<n)
  assert (i!=j)
  ans=id(n)
  ans[i], ans[j] = ans[j], ans[i]
  return ans

# even(perm): perm is an even permutation
def even(perm):
  assert (is_perm(perm))
  n=len(perm)
  ans= True
  p=perm[:] # hack to make a copy
  # counting transpositions needed to sort perm
  i= 0
  # i minimal elements of perm are in the right places
  while (i!=n):
    j=i+1
    minpos=i
    # p[minpos]==minimal among p[i..j)
    while (j!=n):
      if p[j] < p[minpos]:
        minpos= j
      j=j+1
    # p[minpos]==minimal among p[i..n)
    if i!=minpos:
      ans=not ans
      p[i],p[minpos]=p[minpos],p[i]
    i=i+1
  return(ans)

# reverse permutation
def rev(perm):
  assert is_perm(perm)
  n=len(perm)
  ans=id(n)
  for i in range(n):
    ans[perm[i]]=i
  return ans

# position: sequence of different objects

# apply permutation to the position (move place i to perm[i])
def apply (perm,pos):
  assert is_perm(perm)
  n = len(perm)
  assert n==len(pos)
  return [pos[rev(perm)[i]] for i in range(n)]

# board size (Python allows accessing global variable N if it is
# not changed inside the functions)
N=4

# game position: position of size N*N filled by pieces 1.2.,,(N*N)-1;
# zero stands for the empty cell (technically a permutation of size N*N)
# piece located at (row in [0..n), column in [0..n)) is stored in
# position [row*N+column]
# only game positions are used in the sequel

# conversion between 2D coordinate (location) and 1D coordinate (index)
def loc(index):
  assert 0<=index
  assert index < N*N
  return (index//N, index%N)
def index(loc):
  (row,col)=loc
  return N*row+col
def good_cell(loc):
  (row,col)= loc;
  return (0<=row) and (row<N) and (0<=col) and (col<N)


# technical: printing without newline
import sys
def pr(x):
   sys.stdout.write(x)
   sys.stdout.flush

# drawing the game position on the screen
def print_game_pos(position):
   print ('-'*20) # separator line
   for row in range(N):
     for column in range(N):
       cell=position[index((row,column))]
       if cell==0:
         pr ("    ")
       else:
         pr (repr(cell).rjust(4),)
     print ("")

def init_game_pos():
  return [(i+1)%(N*N) for i in range(N*N)]

# making moves in the position

# move empty cell in a given direction dir  = "U", "D", "L", "R"
# up, down, left, right
# returns the new position
def move_empty(dir,position):
  empty_index=rev(position)[0]
  (row,col)=loc(empty_index)
  if dir=="U":
    assert (row > 0)
    return apply (trans(empty_index,index((row-1,col)),N*N),position)
  elif dir=="R":
    assert (col < N-1)
    return apply (trans(empty_index,index((row,col+1)),N*N),position)
  elif dir=="D":
    assert (row < N-1)
    return apply (trans(empty_index,index((row+1,col)),N*N),position)
  elif dir=="L":
    assert (col > 0)
    return apply (trans(empty_index,index((row,col-1)),N*N),position)
  else:
    assert False

# move a given piece into the neighbor empty cell
# returns new position
def move_piece(piece,position):
  empty_index=rev(position)[0]
  (row_empty,col_empty)=loc(empty_index)
  piece_index=rev(position)[piece]
  (row_piece,col_piece)=loc(piece_index)
  if (row_piece==row_empty) and (col_piece==col_empty+1):
     return move_empty("R",position)
  if (row_piece==row_empty+1) and (col_piece==col_empty):
    return move_empty("D",position)
  if (row_piece==row_empty) and (col_piece==col_empty-1):
    return move_empty("L",position)
  if (row_piece==row_empty-1) and (col_piece==col_empty):
    return move_empty("U",position)
  assert False # given piece is not near the empty cell

# applying a sequence of moves (given by piece labels) to a position
# returns the new position
def seq_move_piece (sequence,position):
  tmp= position[:] # make a copy (hack)
  for i in sequence:
   tmp=move_piece(i,tmp)
  return tmp

# apply a sequence of moves (given by the directions for the empty cell)
# returns a new position
def seq_move_empty (sequence,position):
  tmp=position[:] # make a copy (hack)
  for i in sequence:
   tmp=move_empty(i,tmp)
  return tmp

# apply a sequence of moves (given by the directions for the empty cell)
# (assuming the initially the empty cell is at the standard place)
# to a given cell
def trace(sequence,cell):
  (empty_row,empty_col)=(N-1,N-1)
  (row,col)=cell
  empty=(cell==(N-1,N-1)) # special case when cell is the empty cell
  # in this case behavior of (row,col) is strange but it is not used later
  for move in sequence:
    if move=="U":
      empty_row= empty_row-1
      if (row,col)==(empty_row,empty_col): # new position of empty cell
        row=row+1
    if move=="D":
      empty_row=empty_row+1
      if (row,col)==(empty_row,empty_col): # new position of empty cell
        row=row-1
    if move=="L":
      empty_col=empty_col-1
      if (row,col)==(empty_row,empty_col): # new position of empty cell
        col=col+1
    if move=="R":
      empty_col=empty_col+1
      if (row,col)==(empty_row,empty_col): # new position of empty cell
        col=col-1
  if empty:
    return (empty_row,empty_col)
  else:
    return (row,col)

# sequence of empty cell moves that bring it to position c, starting
# from the standard position, first up, then left
def seq_move_empty_to(c):
  (row,col)=c
  assert 0<=row
  assert 0<=col
  assert row<N
  assert col<N
  return ["U"]*(N-1-row)+["L"]*(N-1-col)

# reverting a sequence of empty cell moves (ordering and direction reversed)
def seq_move_empty_rev(seq):
  k=len(seq)
  ans = list(range(k)) # creating list of required length
  for i in range(k):
    if seq[k-1-i]=="U":
      ans[i]= "D"
    elif seq[k-1-i]=="L":
      ans[i]= "R"
    elif seq[k-1-i]=="R":
      ans[i]= "L"
    elif seq[k-1-i]=="D":
      ans[i]= "U"
    else:
      assert False
  return(ans)

# sequence of empty cell moves that creates a positive direction 3-cycle of *
#   *     *
#   *    cell

def seq_3_cycle(cell):
  t = seq_move_empty_to(cell)
  f = seq_move_empty_rev (t)
  return t+["L","U","R","D"]+f
# "LURD" determines the cycle

# move left a piece at c using the cycle
def move_left(c):
  (row,col)=c
  assert col>0
  assert col<N
  assert row>=0
  assert row<N-1 # in the bottom row this does not work
  return seq_3_cycle((row+1,col))

# move up a piece at c using the cycle
def move_up(c):
  (row,col)=c
  assert row>0
  assert row<N
  assert col>=0
  assert col<N-1 # does not wor for the last column
  return seq_3_cycle((row,col+1))*2
# note: square = inversion for 3-cycle

# bring a piece at cell to the left upper corner
def left_upper_move(cell):
  assert cell!=(N-1,N-1)
  (r,c)=cell
  seq=[]
  if (c!=N-1):
    while r!=0:
      seq=seq+move_up((r,c))
      r=r-1
    while c!=0:
      seq=seq+move_left((r,c))
      c=c-1
    return(seq)
  elif (r!=N-1):
    while c!=0:
      seq=seq+move_left((r,c))
      c=c-1
    while r!=0:
      seq=seq+move_up((r,c))
      r=r-1
    return(seq)
  else:
    assert False

# bring a piece at cell to the cell on the right of the left upper corner
def left_upper_right_move(cell):
  assert cell!=(0,0)
  assert cell!=(N-1,N-1)
  (r,c)=cell
  seq=[]
  if (r,c)==(N-1,0):
    seq=seq+seq_3_cycle((N-1,1)) # move right and up
    (r,c)=(N-2,1)
  # not in the bottom left corner
  if (c==0) and (r<N-1):
    seq=seq+seq_3_cycle((r+1,c+1))*2 # move right
    c= 1
  # not in the left column
  if (c==N-1):
    seq=seq+move_left((r,c))
    c=c-1
  # not in the right column
  while r!=0:
    seq=seq+move_up((r,c))
    r=r-1
  while c!=1:
    seq=seq+move_left((r,c))
    c=c-1
  return(seq)

# bring a piece at cell to the cell below left upper corner
# not touching the cell on the right of the left upper corner
def left_upper_below_move(cell):
  assert cell!=(0,0)
  assert cell!=(0.1)
  assert cell!=(N-1,N-1)
  (r,c)=cell
  seq=[]
  if (r,c)==(0,N-1):
    seq=seq+move_left((r,c))
    (r,c)=(0,N-2)
  # not in the right upper corner
  if (r==0) and (c<N-1):
    seq=seq+seq_3_cycle((r+1,c+1)) # move one cell down
    r=1
  # not in the upper row
  if (r==N-1):
    seq=seq+move_up((r,c))
    r=r-1
  # not in the bottom row
  while c!=0:
    seq=seq+move_left((r,c))
    c=c-1
  while r!=1:
    seq=seq+move_up((r,c))
    r=r-1
  return(seq)

# debug
def apply_and_print(seq):
  print_game_pos(seq_move_empty(seq,init_game_pos()))

# collect cellA, cellB, cellC (three different cells) into the left corner
# like
#   cellA cellB
#   cellC
def collect(cellA,cellB,cellC):
  assert good_cell(cellA)
  assert good_cell(cellB)
  assert good_cell(cellC)
  assert (cellA!=cellB)
  assert (cellA!=cellC)
  assert (cellB!=cellC)
  seq=left_upper_move (cellA)
  assert trace(seq,cellA)==(0,0)
  curB=trace(seq,cellB)
  seq=seq+left_upper_right_move(curB)
  assert trace(seq,cellA)==(0,0)
  assert trace(seq,cellB)==(0,1)
  curC=trace(seq,cellC)
  seq=seq+left_upper_below_move(curC)
  assert trace(seq,cellA)==(0,0)
  assert trace(seq,cellC)==(1,0)
  assert trace(seq,cellB)==(0,1)
  return seq

# cycle: cellA<-cellB<-cellC<-cycle
def seq_3_gen_cycle (cellA,cellB,cellC):
  assert good_cell(cellA)
  assert good_cell(cellB)
  assert good_cell(cellC)
  assert (cellA!=cellB)
  assert (cellA!=cellC)
  assert (cellB!=cellC)
  seq=collect(cellA,cellB,cellC)
  return (seq+seq_3_cycle((1,1))+seq_move_empty_rev(seq))

def seq_sort(pos):
  assert (pos[N*N-1]==0) # the empty cell should be in the standard place
  seq=[]
  for i in range(1,N*N-2):
    # pieces with labels <i are on the right places
    curpos=seq_move_empty(seq,pos)
    loc_i=loc(rev(curpos)[i]) # where i is
    dest_i=loc(i-1)        # where i should be
    if dest_i != loc_i:
      tmploca=loc(rev(curpos)[i+1])
      tmplocb=loc(rev(curpos)[i+2])
      # one of them can coincide with dest_i
      if tmploca!=dest_i:
        seq=seq+seq_3_gen_cycle(dest_i,loc_i,tmploca)
      elif tmplocb!=dest_i:
        seq=seq+seq_3_gen_cycle(dest_i,loc_i,tmplocb)
      else:
        assert False
  return(seq)

def seq_labels_sort(pos):
  curpos=pos[:] # hack: a copy
  seq= seq_sort(curpos) # sequence of moves of the empty cell
  ans=[]
  row_empty,col_empty=(N-1,N-1)
  for move in seq:
    if move=="U":
      newrow,newcol= row_empty-1,col_empty
    if move=="L":
      newrow,newcol= row_empty,col_empty-1
    if move=="R":
      newrow,newcol= row_empty,col_empty+1
    if move=="D":
      newrow,newcol= row_empty+1,col_empty
    assert good_cell((newrow,newcol)) # new position of the empty cell
    ans=ans+[curpos[index((newrow,newcol))]]
    curpos[index((newrow,newcol))],curpos[index((row_empty,col_empty))]=  \
           curpos[index((row_empty,col_empty))],\
           curpos[index((newrow,newcol))]
    row_empty,col_empty=newrow,newcol
  return(ans)

def solvable(pos):
  assert is_perm(pos)
  assert pos[N*N-1]==0
  if N%2==0:
    return not even(pos)
  else:
    return even(pos)

# compress the answer sequence (optional)
def compress(seq):
  ans=[]
  for i in seq:
    if len(ans)>0 and i==ans[len(ans)-1]:
      ans.pop()
    else:
      ans=ans+[i]
  return(ans)

position=[2,4,6,12,1,5,8,3,9,10,15,11,13,14,7,0]
print_game_pos(position)
print (solvable(position))
seq=seq_labels_sort(position)
#seq=compress(seq)
print (seq)
print ("length: ", len(seq))
print_game_pos(seq_move_piece(seq,position))
