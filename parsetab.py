
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'nonassocIFFORleftLTLEGTGEEQNEleftPLUSMINUSleftMULDIVMODrightPOWrightNEGATEAND BREAK CASE COLON COMMA CONTINUE DEFAULT DIV DIVEQUALS ELLIPSIS ELSE EQ EQUALS FALSE FLOAT FLOATCONST FOR FROM GE GT IDENTIFIER IF INT INTCONST INTEGRATE LBRACE LBRACKET LE LET LPAREN LT MINUS MINUSEQUALS MINUSMINUS MOD MUL MULEQUALS NE NOT OR PERIOD PLUS PLUSEQUALS PLUSPLUS POW PRINT RBRACE RBRACKET RETURN RPAREN SEMICOLON STRING STRINGCONST SWITCH TO TRUE TYPE WHILE\n        line_statement : statement_list SEMICOLON\n        \n        decl_statement : LET IDENTIFIER EQUALS expression\n                       | LET IDENTIFIER\n        \n        decl_statement : IDENTIFIER EQUALS expression\n        \n        statement_list : statement\n                       | decl_statement\n                       | statement_list SEMICOLON statement\n                       | statement_list SEMICOLON decl_statement\n        \n        statement : PRINT LPAREN expr_list RPAREN\n        \n        expression : TRUE\n        \n        expression : FALSE\n        \n        expression : IDENTIFIER\n        \n        expression : FLOATCONST\n        \n        expression : INTCONST\n        \n        expression : STRINGCONST\n        \n        expression : MINUS expression %prec NEGATE\n        \n        expression : expression PLUS expression\n                   | expression MINUS expression\n                   | expression MUL expression\n                   | expression DIV expression\n                   | expression MOD expression\n                   | expression POW expression\n                   | expression GT expression\n                   | expression GE expression\n                   | expression LT expression\n                   | expression LE expression\n                   | expression EQ expression\n                   | expression NE expression\n        \n        expression : IDENTIFIER PLUSPLUS\n        \n        expression : IDENTIFIER MINUSMINUS\n        \n        expr_list : expression\n                  | expr_list COMMA expression\n\n        \n        expression : LPAREN expression RPAREN\n        empty :'
    
_lr_action_items = {'PRINT':([0,8,],[5,5,]),'LET':([0,8,],[6,6,]),'IDENTIFIER':([0,6,8,9,11,14,23,24,28,29,30,31,32,33,34,35,36,37,38,39,40,],[7,10,7,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,19,]),'$end':([1,8,],[0,-1,]),'SEMICOLON':([2,3,4,10,12,13,17,18,19,20,21,22,25,27,41,42,43,44,45,47,48,49,50,51,52,53,54,55,56,57,58,],[8,-5,-6,-3,-7,-8,-10,-11,-12,-13,-14,-15,-4,-9,-29,-30,-16,-2,-33,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,]),'LPAREN':([5,9,11,14,23,24,28,29,30,31,32,33,34,35,36,37,38,39,40,],[9,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,14,]),'EQUALS':([7,10,],[11,24,]),'TRUE':([9,11,14,23,24,28,29,30,31,32,33,34,35,36,37,38,39,40,],[17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,17,]),'FALSE':([9,11,14,23,24,28,29,30,31,32,33,34,35,36,37,38,39,40,],[18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,18,]),'FLOATCONST':([9,11,14,23,24,28,29,30,31,32,33,34,35,36,37,38,39,40,],[20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,20,]),'INTCONST':([9,11,14,23,24,28,29,30,31,32,33,34,35,36,37,38,39,40,],[21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,21,]),'STRINGCONST':([9,11,14,23,24,28,29,30,31,32,33,34,35,36,37,38,39,40,],[22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,22,]),'MINUS':([9,11,14,16,17,18,19,20,21,22,23,24,25,26,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,],[23,23,23,30,-10,-11,-12,-13,-14,-15,23,23,30,30,23,23,23,23,23,23,23,23,23,23,23,23,23,-29,-30,-16,30,-33,30,-17,-18,-19,-20,-21,-22,30,30,30,30,30,30,]),'RPAREN':([15,16,17,18,19,20,21,22,26,41,42,43,45,46,47,48,49,50,51,52,53,54,55,56,57,58,],[27,-31,-10,-11,-12,-13,-14,-15,45,-29,-30,-16,-33,-32,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,]),'COMMA':([15,16,17,18,19,20,21,22,41,42,43,45,46,47,48,49,50,51,52,53,54,55,56,57,58,],[28,-31,-10,-11,-12,-13,-14,-15,-29,-30,-16,-33,-32,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,]),'PLUS':([16,17,18,19,20,21,22,25,26,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,],[29,-10,-11,-12,-13,-14,-15,29,29,-29,-30,-16,29,-33,29,-17,-18,-19,-20,-21,-22,29,29,29,29,29,29,]),'MUL':([16,17,18,19,20,21,22,25,26,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,],[31,-10,-11,-12,-13,-14,-15,31,31,-29,-30,-16,31,-33,31,31,31,-19,-20,-21,-22,31,31,31,31,31,31,]),'DIV':([16,17,18,19,20,21,22,25,26,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,],[32,-10,-11,-12,-13,-14,-15,32,32,-29,-30,-16,32,-33,32,32,32,-19,-20,-21,-22,32,32,32,32,32,32,]),'MOD':([16,17,18,19,20,21,22,25,26,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,],[33,-10,-11,-12,-13,-14,-15,33,33,-29,-30,-16,33,-33,33,33,33,-19,-20,-21,-22,33,33,33,33,33,33,]),'POW':([16,17,18,19,20,21,22,25,26,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,],[34,-10,-11,-12,-13,-14,-15,34,34,-29,-30,-16,34,-33,34,34,34,34,34,34,34,34,34,34,34,34,34,]),'GT':([16,17,18,19,20,21,22,25,26,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,],[35,-10,-11,-12,-13,-14,-15,35,35,-29,-30,-16,35,-33,35,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,]),'GE':([16,17,18,19,20,21,22,25,26,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,],[36,-10,-11,-12,-13,-14,-15,36,36,-29,-30,-16,36,-33,36,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,]),'LT':([16,17,18,19,20,21,22,25,26,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,],[37,-10,-11,-12,-13,-14,-15,37,37,-29,-30,-16,37,-33,37,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,]),'LE':([16,17,18,19,20,21,22,25,26,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,],[38,-10,-11,-12,-13,-14,-15,38,38,-29,-30,-16,38,-33,38,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,]),'EQ':([16,17,18,19,20,21,22,25,26,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,],[39,-10,-11,-12,-13,-14,-15,39,39,-29,-30,-16,39,-33,39,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,]),'NE':([16,17,18,19,20,21,22,25,26,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,],[40,-10,-11,-12,-13,-14,-15,40,40,-29,-30,-16,40,-33,40,-17,-18,-19,-20,-21,-22,-23,-24,-25,-26,-27,-28,]),'PLUSPLUS':([19,],[41,]),'MINUSMINUS':([19,],[42,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'line_statement':([0,],[1,]),'statement_list':([0,],[2,]),'statement':([0,8,],[3,12,]),'decl_statement':([0,8,],[4,13,]),'expr_list':([9,],[15,]),'expression':([9,11,14,23,24,28,29,30,31,32,33,34,35,36,37,38,39,40,],[16,25,26,43,44,46,47,48,49,50,51,52,53,54,55,56,57,58,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> line_statement","S'",1,None,None,None),
  ('line_statement -> statement_list SEMICOLON','line_statement',2,'p_line_statement','Parser.py',23),
  ('decl_statement -> LET IDENTIFIER EQUALS expression','decl_statement',4,'p_declaration','Parser.py',35),
  ('decl_statement -> LET IDENTIFIER','decl_statement',2,'p_declaration','Parser.py',36),
  ('decl_statement -> IDENTIFIER EQUALS expression','decl_statement',3,'p_decl_assign','Parser.py',46),
  ('statement_list -> statement','statement_list',1,'p_multiple_statement','Parser.py',53),
  ('statement_list -> decl_statement','statement_list',1,'p_multiple_statement','Parser.py',54),
  ('statement_list -> statement_list SEMICOLON statement','statement_list',3,'p_multiple_statement','Parser.py',55),
  ('statement_list -> statement_list SEMICOLON decl_statement','statement_list',3,'p_multiple_statement','Parser.py',56),
  ('statement -> PRINT LPAREN expr_list RPAREN','statement',4,'p_print_statement','Parser.py',67),
  ('expression -> TRUE','expression',1,'p_expression_bool_true','Parser.py',73),
  ('expression -> FALSE','expression',1,'p_expression_bool_false','Parser.py',79),
  ('expression -> IDENTIFIER','expression',1,'p_expression_var','Parser.py',85),
  ('expression -> FLOATCONST','expression',1,'p_expression_float','Parser.py',91),
  ('expression -> INTCONST','expression',1,'p_expression_integer','Parser.py',97),
  ('expression -> STRINGCONST','expression',1,'p_expression_string','Parser.py',103),
  ('expression -> MINUS expression','expression',2,'p_expression_neg','Parser.py',109),
  ('expression -> expression PLUS expression','expression',3,'p_expression_binop','Parser.py',115),
  ('expression -> expression MINUS expression','expression',3,'p_expression_binop','Parser.py',116),
  ('expression -> expression MUL expression','expression',3,'p_expression_binop','Parser.py',117),
  ('expression -> expression DIV expression','expression',3,'p_expression_binop','Parser.py',118),
  ('expression -> expression MOD expression','expression',3,'p_expression_binop','Parser.py',119),
  ('expression -> expression POW expression','expression',3,'p_expression_binop','Parser.py',120),
  ('expression -> expression GT expression','expression',3,'p_expression_binop','Parser.py',121),
  ('expression -> expression GE expression','expression',3,'p_expression_binop','Parser.py',122),
  ('expression -> expression LT expression','expression',3,'p_expression_binop','Parser.py',123),
  ('expression -> expression LE expression','expression',3,'p_expression_binop','Parser.py',124),
  ('expression -> expression EQ expression','expression',3,'p_expression_binop','Parser.py',125),
  ('expression -> expression NE expression','expression',3,'p_expression_binop','Parser.py',126),
  ('expression -> IDENTIFIER PLUSPLUS','expression',2,'p_expression_increment','Parser.py',132),
  ('expression -> IDENTIFIER MINUSMINUS','expression',2,'p_expression_decrement','Parser.py',138),
  ('expr_list -> expression','expr_list',1,'p_expression_list','Parser.py',144),
  ('expr_list -> expr_list COMMA expression','expr_list',3,'p_expression_list','Parser.py',145),
  ('expression -> LPAREN expression RPAREN','expression',3,'p_expression_parens','Parser.py',155),
  ('empty -> <empty>','empty',0,'p_empty','Parser.py',163),
]