from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.
        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.
        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))
        Returns:
            A Tuple of Tuples that represent the game state
        """
        state_tup= []
        peg_1 = []
        peg_2 = []
        peg_3 = []
        ask_1 = self.kb.kb_ask(parse_input('fact: (on ?disk peg1'))
        if ask_1:
            for each in ask_1:
                num = int(str(each.bindings[0].constant)[-1])
                peg_1.append(num)
        ask_2 = self.kb.kb_ask(parse_input('fact: (on ?disk peg2'))

        peg_1.sort()

        if ask_2:
            for each in ask_2:
                num = int(str(each.bindings[0].constant)[-1])
                peg_2.append(num)
        peg_2.sort()
        ask_3 = self.kb.kb_ask(parse_input('fact: (on ?disk peg3'))

        if ask_3:
            for each in ask_3:

                num = int(str(each.bindings[0].constant)[-1])
                peg_3.append(num)
        peg_3.sort()
        #state_tup.append(ask_1)
        #state_tup.append(ask_2)
        #state_tup.append(ask_3)

        state_tup = (tuple(peg_1), tuple(peg_2), tuple(peg_3))

        return state_tup

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.
        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)
        Args:
            movable_statement: A Statement object that contains one of the currently viable moves
        Returns:
            None
        """
        curr_state = self.getGameState()

        disk = str(movable_statement.terms[0])
        from_peg = str(movable_statement.terms[1])
        to_peg = str(movable_statement.terms[2])
        indx1 = curr_state[int(from_peg[-1]) - 1]
        indx2 = curr_state[int(to_peg[-1]) - 1]
        if len(indx1) - 1 != 0:
            self.kb.kb_assert(parse_input("fact: (top disk" + str(indx1[1]) + " " + from_peg + ")"))
        else:
            self.kb.kb_assert(parse_input("fact: (empty " + from_peg + ")"))

        self.kb.kb_assert(parse_input("fact: (on " + disk + " " + to_peg + ")"))
        self.kb.kb_assert(parse_input("fact: (top " + disk + " " + to_peg + ")"))

        if len(indx2) == 0:
            self.kb.kb_retract(parse_input("fact: (empty " + to_peg + ")"))
        else:
            self.kb.kb_retract(parse_input("fact: (top disk" + str(indx2[0]) + " " + to_peg + ")"))

        self.kb.kb_retract(parse_input("fact: (on " + disk + " " + from_peg + ")"))
        self.kb.kb_retract(parse_input("fact: (top " + disk + " " + from_peg + ")"))




    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.
        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))
        Returns:
            A Tuple of Tuples that represent the game state
        """

        state = []
        facts = ['fact: (coordinate ?tile ?x pos1)',
                'fact: (coordinate ?tile ?x pos2)',
                'fact: (coordinate ?tile ?x pos3)']

        for each_fact in facts:
            tup = [0, 0, 0]
            ask = self.kb.kb_ask(parse_input(each_fact))

            for each in ask:
                if each.bindings[0].constant.element == 'empty':
                    tup[int(each.bindings[1].constant.element[-1]) - 1] = -1;
                else:
                    tup[int(each.bindings[1].constant.element[-1]) - 1] = int(each.bindings[0].constant.element[-1])
            state.append(tuple(tup))

        return tuple(state)
    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.
        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)
        Args:
            movable_statement: A Statement object that contains one of the currently viable moves
        Returns:
            None
        """

        tile = movable_statement.terms[0].term.element
        x1 = movable_statement.terms[1].term.element
        y1 = movable_statement.terms[2].term.element


        fact_1 = parse_input("fact: (coordinate " + tile + " " + x1 + " " + y1 + ")")
        self.kb.kb_retract(fact_1)
        fact_2 = parse_input("fact: (coordinate empty " + x1 + " " + y1 + ")")
        self.kb.kb_assert(fact_2)

        x2 = movable_statement.terms[3].term.element
        y2 = movable_statement.terms[4].term.element
        fact_3 = parse_input("fact: (coordinate " + tile + " " + x2 + " " + y2 + ")")
        self.kb.kb_assert(fact_3)

        fact_4 = parse_input("fact: (coordinate"+ "empty " + x2 + " " + y2 + ")")
        self.kb.kb_retract(fact_4)


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
