% ====================
% Values & Types
% ====================

empty_value(0).
attacker_value(1).
defender_value(2).
king_value(3).

opposite_team(Board, Row1, Col1, Row2, Col2) :-
    king_cell(Board, Row1, Col1),
    attacker_cell(Board, Row2, Col2).

opposite_team(Board, Row1, Col1, Row2, Col2) :-
    defender_cell(Board, Row1, Col1),
    attacker_cell(Board, Row2, Col2).


opposite_team(Board, Row1, Col1, Row2, Col2) :-
    attacker_cell(Board, Row1, Col1),
    defender_cell(Board, Row2, Col2).

% ====================
% Cells & Boundary
% ====================
cell_value(Board, Row, Col, Value) :-
    nth0(Row, Board, BoardRow),
    nth0(Col, BoardRow, Value).

empty_cell(Board, Row, Col) :-
    empty_value(EmptyValue),
    cell_value(Board, Row, Col, EmptyValue).

attacker_cell(Board, Row, Col) :-
    attacker_value(AttackerValue),
    cell_value(Board, Row, Col, AttackerValue).

defender_cell(Board, Row, Col) :-
    defender_value(DefenderValue),
    cell_value(Board, Row, Col, DefenderValue).

king_cell(Board, Row, Col) :-
    king_value(KingValue),
    cell_value(Board, Row, Col, KingValue).

throne(Board, Row, Col) :-
    board_size(Board, Size),
    M is Size // 2,
    Row = M,
    Col = M.

corner(Board, Row, Col) :-
    board_size(Board, Size),
    M is Size - 1,
    (Row = 0; Row = M),
    (Col = 0; Col = M).

board_size(Board, Size) :-
    nth0(0, Board, Row),
    length(Row, Size).

within_board(Board, Row, Col) :-
    board_size(Board, Size),
    Row >= 0, 
    Row < Size,
    Col >= 0, 
    Col < Size.


% ====================
% Clear Path
% ====================

clear_horizontal_path(_, _, Col, Col).

clear_horizontal_path(Board, Row, SC, EC) :-
    SC < EC,
    NextCol is SC + 1,
    empty_cell(Board, Row, NextCol),
    clear_horizontal_path(Board, Row, NextCol, EC).

clear_horizontal_path(Board, Row, SC, EC) :-
    SC > EC,
    NextCol is SC - 1,
    empty_cell(Board, Row, NextCol),
    clear_horizontal_path(Board, Row, NextCol, EC).

clear_vertical_path(_, Row, Row, _).

clear_vertical_path(Board, SR, ER, Col) :-
    SR < ER,
    NextRow is SR + 1,
    empty_cell(Board, NextRow, Col),
    clear_vertical_path(Board, NextRow, ER, Col).

clear_vertical_path(Board, SR, ER, Col) :-
    SR > ER,
    NextRow is SR - 1,
    empty_cell(Board, NextRow, Col),
    clear_vertical_path(Board, NextRow, ER, Col).

clear_path(Board, Row, SC, Row, EC) :-
    within_board(Board, Row, SC),
    within_board(Board, Row, EC),
    clear_horizontal_path(Board, Row, SC, EC).

clear_path(Board, SR, Col, ER, Col) :-
    within_board(Board, SR, Col),
    within_board(Board, ER, Col),
    clear_vertical_path(Board, SR, ER, Col).

% ====================
% Capturing 
% ====================
blocked_by_rules_cell(Board, Row, Col) :-
    board_size(Board, Size),
    (
        Row < 0 ;
        Row >= Size ;
        Col < 0 ;
        Col >= Size ;
        throne(Board, Row, Col) ;
        corner(Board, Row, Col)
    ).

sandwich_cell(Board, Row, Col) :-
    UpRow is Row - 1,
    DownRow is Row + 1,
    (blocked_by_rules_cell(Board, UpRow, Col) ; opposite_team(Board, Row, Col, UpRow, Col)),
    (blocked_by_rules_cell(Board, DownRow, Col) ; opposite_team(Board, Row, Col, DownRow, Col)).

sandwich_cell(Board, Row, Col) :-
    LeftCol is Col - 1,
    RightCol is Col + 1,
    (blocked_by_rules_cell(Board, Row, LeftCol) ; opposite_team(Board, Row, Col, Row, LeftCol)),
    (blocked_by_rules_cell(Board, Row, RightCol) ; opposite_team(Board, Row, Col, Row, RightCol)).

trapped_cell(Board, Row, Col) :-
    UpRow is Row - 1,
    DownRow is Row + 1,
    (blocked_by_rules_cell(Board, UpRow, Col) ; opposite_team(Board, Row, Col, UpRow, Col)),
    (blocked_by_rules_cell(Board, DownRow, Col) ; opposite_team(Board, Row, Col, DownRow, Col)),
    LeftCol is Col - 1,
    RightCol is Col + 1,
    (blocked_by_rules_cell(Board, Row, LeftCol) ; opposite_team(Board, Row, Col, Row, LeftCol)),
    (blocked_by_rules_cell(Board, Row, RightCol) ; opposite_team(Board, Row, Col, Row, RightCol)).

capturable_cell(Board, Row, Col) :-
    within_board(Board, Row, Col),
    king_cell(Board, Row, Col),
    trapped_cell(Board, Row, Col).

capturable_cell(Board, Row, Col) :-
    within_board(Board, Row, Col),
    (attacker_cell(Board, Row, Col) ; defender_cell(Board, Row, Col)),
    sandwich_cell(Board, Row, Col).

check_capturing(Board, Row, Col, NewBoard) :-
    UpRow is Row - 1,
    capturable_cell(Board, UpRow, Col),
    empty_value(EmptyValue),
    set_cell(Board, UpRow, Col, EmptyValue, NewBoard).

check_capturing(Board, Row, Col, NewBoard) :-
    DownRow is Row + 1,
    capturable_cell(Board, DownRow, Col),
    empty_value(EmptyValue),
    set_cell(Board, DownRow, Col, EmptyValue, NewBoard).

check_capturing(Board, Row, Col, NewBoard) :-
    LeftCol is Col - 1,
    capturable_cell(Board, Row, LeftCol),
    empty_value(EmptyValue),
    set_cell(Board, Row, LeftCol, EmptyValue, NewBoard).

check_capturing(Board, Row, Col, NewBoard) :-
    RightCol is Col + 1,
    capturable_cell(Board, Row, RightCol),
    empty_value(EmptyValue),
    set_cell(Board, Row, RightCol, EmptyValue, NewBoard).

check_capturing(Board, _, _, Board).


% ====================
% Board & Update 
% ====================
replace_nth0(0, [_|Xs], X, [X|Xs]).
replace_nth0(I, [Y|Ys], X, [Y|Zs]) :-
    I > 0,
    I1 is I - 1,
    replace_nth0(I1, Ys, X, Zs).

set_cell(Board, R, C, Value, Board) :-
    king_cell(Board, R, C),
    trapped_cell(Board, R, C).

set_cell(Board, R, C, Value, NewBoard) :-
    nth0(R, Board, Row),
    replace_nth0(C, Row, Value, NewRow),
    replace_nth0(R, Board, NewRow, NewBoard).

update_board(Board, SR, SC, ER, EC, NewBoard) :-
    cell_value(Board, SR, SC, Value),
    empty_value(EmptyValue),
    set_cell(Board, SR, SC, EmptyValue, TempBoard),
    set_cell(TempBoard, ER, EC, Value, NewBoard).

terminal_state(Board, Winner) :-
    king_cell(Board, Row, Col),
    corner(Board, Row, Col),
    Winner = defender.

terminal_state(Board, Winner) :-
    king_cell(Board, Row, Col),
    trapped_cell(Board, Row, Col),
    Winner = attacker.

% ====================
% Movement
% ====================
valid_move(Board, SR, SC, ER, EC) :-
    king_cell(Board, SR, SC),
    within_board(Board, ER, EC),
    clear_path(Board, SR, SC, ER, EC),
    cell_value(Board, SR, SC, Value),
    set_cell(Board, ER, EC, Value, TempBoard),
    \+ capturable_cell(TempBoard, ER, EC).

valid_move(Board, SR, SC, ER, EC) :-
    \+ king_cell(Board, SR, SC),
    within_board(Board, SR, SC),
    within_board(Board, ER, EC),
    \+ blocked_by_rules_cell(Board, ER, EC),
    clear_path(Board, SR, SC, ER, EC),
    cell_value(Board, SR, SC, Value),
    set_cell(Board, ER, EC, Value, TempBoard),
    \+ capturable_cell(TempBoard, ER, EC).

make_move(Board, SR, SC, ER, EC, NewBoard) :-
    valid_move(Board, SR, SC, ER, EC),
    update_board(Board, SR, SC, ER, EC, TempBoard),
    check_capturing(TempBoard, ER, EC, TempBoard1),
    check_capturing(TempBoard1, ER, EC, TempBoard2),
    check_capturing(TempBoard2, ER, EC, NewBoard).

% ====================
% Alpha-Beta Score Evaluation & State transition
% ====================
number_of_pieces(Board, attacker, Count) :-
    findall(1, attacker_cell(Board, Row, Col), Pieces),
    length(Pieces, Count).

number_of_pieces(Board, defender, Count) :-
    findall(1, defender_cell(Board, Row, Col), Pieces),
    length(Pieces, DefCount),
    Count is DefCount + 1.

king_pressure(Board, Row, Col, Pressure) :-
    Up is Row - 1,
    Down is Row + 1,
    Left is Col - 1,
    Right is Col + 1,
    findall(1,
        (
            (within_board(Board, Up, Col), attacker_cell(Board, Up, Col));
            (within_board(Board, Down, Col), attacker_cell(Board, Down, Col));
            (within_board(Board, Row, Left), attacker_cell(Board, Row, Left));
            (within_board(Board, Row, Right), attacker_cell(Board, Row, Right))
        ),
        Pieces),
    length(Pieces, Pressure).

min_corner_dist(Board, Row, Col, Dist) :-
    corner(Board, CR, CC),
    Dist is abs(Row - CR) + abs(Col - CC).

king_mobility(Board, Row, Col, Mobility) :-
    findall(1,
        (
            empty_cell(Board, ER, EC),
            valid_move(Board, Row, Col, ER, EC)
        ),
        Moves),
    length(Moves, Mobility).

attackers_evaluation(Board, Score) :-
    king_cell(Board, Row, Col),
    king_pressure(Board, Row, Col, A),
    number_of_pieces(Board, attacker, B),
    Score is (A * 25) + (B * 10).
    
defenders_evaluation(Board, Score) :-
    king_cell(Board, Row, Col),
    min_corner_dist(Board, Row, Col, A),
    king_mobility(Board, Row, Col, B),
    number_of_pieces(Board, defender, C),
    Score is (A * 50) + (B * 25) + (C * 5).

evaluation(Board, Score) :-
    terminal_state(Board, attacker),
    Score is 10000000.

evaluation(Board, Score) :-
    terminal_state(Board, defender),
    Score is -10000000.

evaluation(Board, Score) :-
    attackers_evaluation(Board, AttackersScore),
    defenders_evaluation(Board, DefendersScore),
    Score is AttackersScore - DefendersScore.

next_state(Board, attacker, SR, SC, ER, EC, NewBoard) :-
    attacker_cell(Board, SR, SC),
    empty_cell(Board, ER, EC),
    valid_move(Board, SR, SC, ER, EC),
    make_move(Board, SR, SC, ER, EC, NewBoard).

next_state(Board, defender, SR, SC, ER, EC, NewBoard) :-
    ( defender_cell(Board, SR, SC) ; king_cell(Board, SR, SC) ),
    empty_cell(Board, ER, EC),
    valid_move(Board, SR, SC, ER, EC),
    make_move(Board, SR, SC, ER, EC, NewBoard).

next_states(Board, attacker, _Alpha, _Beta, NextStates) :-
    findall(
        state(SR, SC, ER, EC, NewBoard),
        next_state(Board, attacker, SR, SC, ER, EC, NewBoard),
        NextStates
    ).

next_states(Board, defender, _Alpha, _Beta, NextStates) :-
    findall(
        state(SR, SC, ER, EC, NewBoard),
        next_state(Board, defender, SR, SC, ER, EC, NewBoard),
        NextStates
    ).

% ====================
% Alpha-Beta Algorithm
% ====================

alpha_beta(Board, Depth, _, _, _, best(Score, none, none, none, none, Board)) :-
    ( Depth =< 0 ; terminal_state(Board, _) ),
    evaluation(Board, Score).

alpha_beta(Board, Depth, attacker, Alpha, Beta, BestMove) :-
    Depth > 0,
    \+ terminal_state(Board, _),
    next_states(Board, attacker, Alpha, Beta, States),
    States \= [],
    Depth1 is Depth - 1,
    alpha_beta_max(
        States,
        Depth1,
        Alpha,
        Beta,
        best(-1000000000, none, none, none, none, Board),
        BestMove
    ).

alpha_beta(Board, Depth, defender, Alpha, Beta, BestMove) :-
    Depth > 0,
    \+ terminal_state(Board, _),
    next_states(Board, defender, Alpha, Beta, States),
    States \= [],
    Depth1 is Depth - 1,
    alpha_beta_min(
        States,
        Depth1,
        Alpha,
        Beta,
        best(1000000000, none, none, none, none, Board),
        BestMove
    ).

alpha_beta_max([], _, _, _, Best, Best).

alpha_beta_max([state(SR, SC, ER, EC, ChildBoard) | Rest], Depth, Alpha, Beta, CurrentBest, BestMove) :-
    alpha_beta(ChildBoard, Depth, defender, Alpha, Beta, ChildBest),
    ChildBest = best(Score, _, _, _, _, _),
    CurrentBest = best(BestScore, _, _, _, _, _),
    (
        Score > BestScore
    ->
        NewBest = best(Score, SR, SC, ER, EC, ChildBoard),
        NewAlpha is max(Alpha, Score)
    ;
        NewBest = CurrentBest,
        NewAlpha = Alpha
    ),
    (
        NewAlpha >= Beta
    ->
        BestMove = NewBest
    ;
        alpha_beta_max(Rest, Depth, NewAlpha, Beta, NewBest, BestMove)
    ).

alpha_beta_min([], _, _, _, Best, Best).

alpha_beta_min([state(SR, SC, ER, EC, ChildBoard) | Rest], Depth, Alpha, Beta, CurrentBest, BestMove) :-
    alpha_beta(ChildBoard, Depth, attacker, Alpha, Beta, ChildBest),
    ChildBest = best(Score, _, _, _, _, _),
    CurrentBest = best(BestScore, _, _, _, _, _),
    (
        Score < BestScore
    ->
        NewBest = best(Score, SR, SC, ER, EC, ChildBoard),
        NewBeta is min(Beta, Score)
    ;
        NewBest = CurrentBest,
        NewBeta = Beta
    ),
    (
        NewBeta =< Alpha
    ->
        BestMove = NewBest
    ;
        alpha_beta_min(Rest, Depth, Alpha, NewBeta, NewBest, BestMove)
    ).

% ====================
% Interface (REAL)
% ====================

best_attacker_move(Board, Depth, SR, SC, ER, EC) :-
    alpha_beta(Board, Depth, attacker, -1000000000, 1000000000,
               best(_, SR, SC, ER, EC, _)).

best_defender_move(Board, Depth, SR, SC, ER, EC) :-
    alpha_beta(Board, Depth, defender, -1000000000, 1000000000,
               best(_, SR, SC, ER, EC, _)).
