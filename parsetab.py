
# C:/Users/Alon/PycharmProjects/CompilersAssignment1\parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.5'

_lr_method = 'LALR'

_lr_signature = 'B51D5AA08465A9AF1E2C06741942D082'
    
_lr_action_items = {'RPAREN':([1,4,9,10,11,12,13,],[-6,9,-5,-1,-4,-2,-3,]),'DIVIDE':([1,3,4,9,10,11,12,13,],[-6,6,6,-5,6,-4,6,-3,]),'NUMBER':([0,2,5,6,7,8,],[1,1,1,1,1,1,]),'TIMES':([1,3,4,9,10,11,12,13,],[-6,8,8,-5,8,-4,8,-3,]),'PLUS':([1,3,4,9,10,11,12,13,],[-6,5,5,-5,-1,-4,-2,-3,]),'LPAREN':([0,2,5,6,7,8,],[2,2,2,2,2,2,]),'MINUS':([1,3,4,9,10,11,12,13,],[-6,7,7,-5,-1,-4,-2,-3,]),'$end':([1,3,9,10,11,12,13,],[-6,0,-5,-1,-4,-2,-3,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expression':([0,2,5,6,7,8,],[3,4,10,11,12,13,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expression","S'",1,None,None,None),
  ('expression -> expression PLUS expression','expression',3,'p_expression_binop','parse_ula.py',47),
  ('expression -> expression MINUS expression','expression',3,'p_expression_binop','parse_ula.py',48),
  ('expression -> expression TIMES expression','expression',3,'p_expression_binop','parse_ula.py',49),
  ('expression -> expression DIVIDE expression','expression',3,'p_expression_binop','parse_ula.py',50),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_group','parse_ula.py',55),
  ('expression -> NUMBER','expression',1,'p_expression_number','parse_ula.py',59),
]