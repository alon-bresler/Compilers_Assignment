
# C:/Users/Alon/PycharmProjects/CompilersAssignment1\parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.5'

_lr_method = 'LALR'

_lr_signature = '29DFC646F21F2759B269000B4CCBDC24'
    
_lr_action_items = {'RPAREN':([5,7,8,13,14,15,16,17,],[-7,-8,13,-6,-5,-4,-2,-3,]),'DIVIDE':([5,6,7,8,13,14,15,16,17,],[-7,9,-8,9,-6,-5,-4,9,9,]),'EQUALS':([2,],[3,]),'FLOAT_LITERAL':([3,4,9,10,11,12,],[5,5,5,5,5,5,]),'PLUS':([5,6,7,8,13,14,15,16,17,],[-7,11,-8,11,-6,-5,-4,-2,-3,]),'LPAREN':([3,4,9,10,11,12,],[4,4,4,4,4,4,]),'TIMES':([5,6,7,8,13,14,15,16,17,],[-7,10,-8,10,-6,-5,-4,10,10,]),'MINUS':([5,6,7,8,13,14,15,16,17,],[-7,12,-8,12,-6,-5,-4,-2,-3,]),'ID':([0,3,4,9,10,11,12,],[2,7,7,7,7,7,7,]),'$end':([1,5,6,7,13,14,15,16,17,],[0,-7,-1,-8,-6,-5,-4,-2,-3,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'assignment':([0,],[1,]),'expression':([3,4,9,10,11,12,],[6,8,14,15,16,17,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> assignment","S'",1,None,None,None),
  ('assignment -> ID EQUALS expression','assignment',3,'p_assignment','parse_ula.py',25),
  ('expression -> expression PLUS expression','expression',3,'p_expression','parse_ula.py',29),
  ('expression -> expression MINUS expression','expression',3,'p_expression','parse_ula.py',30),
  ('expression -> expression TIMES expression','expression',3,'p_expression','parse_ula.py',31),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression','parse_ula.py',32),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','parse_ula.py',45),
  ('expression -> FLOAT_LITERAL','expression',1,'p_expression_number','parse_ula.py',49),
  ('expression -> ID','expression',1,'p_id_expression','parse_ula.py',53),
]
