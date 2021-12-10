from enum import Enum
from typing import Union

__all__ = ['Operation', 'Cluese', 'parse', 'prove']
__author__ = 'Mahdi Kashani'
__title__ = 'Resolution method'

class Operation(Enum):
    """
        Attributs
        ---------
            NONE : no Operation
            NEGATION : ~
            CONJUNCTION : \\/
            DISJUNCTION : /\\
            IMPLICATION : ->
            EQUVALENCE : <->

        Methods
        -------
            getOperation(operand)
                return your operand in Operation type
    """
    NONE        = ' '     # a , b
    NEGATION    = '~'     # ~a , ~b
    CONJUNCTION = '\\/'   # a \/ b
    DISJUNCTION = '/\\'   # a /\ b
    IMPLICATION = '->'    # a -> b
    EQUVALENCE  = '<->'   # a <-> b

    @staticmethod
    def getOperation(operand: str):
        if(operand == '~'):
            return Operation.NEGATION
        elif(operand ==  '\\/'):
            return Operation.CONJUNCTION
        elif(operand == '/\\'):
            return Operation.DISJUNCTION
        elif(operand == '->'):
            return Operation.IMPLICATION
        elif(operand == '<->'):
            return Operation.EQUVALENCE
        else:
            return Operation.NONE

    @property
    def symbol(self) -> str:
        if(self == Operation.NEGATION):
            return '\u02DC'
        elif(self == Operation.CONJUNCTION):
            return '\u2228'
        elif(self == Operation.DISJUNCTION):
            return '\u2227'
        elif(self == Operation.IMPLICATION):
            return '\u2192'
        elif(self == Operation.EQUVALENCE):
            return '\u27F7'
        else:
            return ''   

class CluaseSentence:
    cluase: Union[tuple, str]
    operand: Operation
    def __init__(self, operand: Operation, cluase: Union[tuple, str]):
        if(operand == Operation.NONE):
            assert isinstance(cluase, str), "you should use str or tuple with Cluse type element"
        elif(operand == Operation.NEGATION):
            assert isinstance(cluase, CluaseSentence), "you should use str or tuple with Cluse type element"
        else:
            assert all(isinstance(i, CluaseSentence) for i in cluase), "you should use str or tuple with Cluse type element"
        self.operand = operand
        self.cluase = cluase
    
    def __key(self):
        return(self.operand, self.cluase)
    
    def __hash__(self) -> int:
        return hash(self.__key())

    def __eq__(self, other) -> bool:
        return (isinstance(other, type(self)) and (self.cluase, self.operand) == (other.cluase, other.operand))        

    def __str__(self):
        if(self.operand == Operation.NONE or self.operand == Operation.NEGATION):
            op = self.operand.symbol
            return f'{op} {str(self.cluase.__str__())}'
        op = self.operand.symbol
        return f'{self.cluase[0].__str__()} {op} {self.cluase[1].__str__()}'

def convert(term: CluaseSentence):
    """ convert implication and equavalnce to disjunction """
    if(term.operand == Operation.IMPLICATION):
        cluase = ( (Operation.NEGATION, (term.cluase[0],) ), term.cluase[1] )
        return ( Operation.DISJUNCTION, cluase ) 
    elif(term.operand == Operation.EQUVALENCE):
        cluase1 = ( Operation.CONJUNCTION, ((Operation.NEGATION, term.cluase[0],), term.cluase[1]))
        cluase2 = ( Operation.CONJUNCTION, (term.cluase[0], (Operation.NEGATION, term.cluase[1],)))
        return (Operation.DISJUNCTION, (cluase1, cluase2))

def simplificationNegation(term: CluaseSentence):
    while(term.operand == Operation.NEGATION and term.cluase.operand == Operation.NEGATION):
        term = term.cluasecluasee
    return term

def distribution(term: CluaseSentence):
    if(
        not term.cluase[0].operand == Operation.NONE
        and term.cluase[1].operand == Operation.NONE
        and not term.cluase[0].operand == term.operand
    ):
        cluase1 = CluaseSentence(term.operand, (term.cluase[0].cluase[0], term.cluase[1]))
        cluase2 = CluaseSentence(term.operand, (term.cluase[0].cluase[1], term.cluase[1]))
        return CluaseSentence(term.cluase[0].operand, (cluase1, cluase2))

    elif(
        not term.cluase[1].operand == Operation.NONE
        and term.cluase[0].operand == Operation.NONE
        and not term.cluase[1].operand == term.operand
    ):
        cluase1 = CluaseSentence(term.operand, (term.cluase[1].cluase[0], term.cluase[0]))
        cluase2 = CluaseSentence(term.operand, (term.cluase[1].cluase[0], term.cluase[0]))
        return CluaseSentence(term.cluase[0].operand, (cluase1, cluase2))

def splitByDisjunction(term: CluaseSentence):
    result = set()
    if(term.operand == Operation.DISJUNCTION):
        cluase1 = term.cluase[0]
        cluase2 = term.cluase[1]
        if(not cluase1.operand == Operation.NONE and not cluase1.operand == Operation.NEGATION):
            result |= (splitByDisjunction(cluase1))
        else:
            result.add(cluase1)
        if(not cluase2.operand == Operation.NONE and not cluase2.operand == Operation.NEGATION):
            result |= (splitByDisjunction(cluase2))
        else:
            result.add(cluase2)
        return result
    elif(term.operand == Operation.CONJUNCTION):
        return set([term.cluase])         

def prove(cluases: list, coclusion):
    """
        if cluases can prove conlusion return True otherwise False
    """
    pass
        


def parse(input: list) -> CluaseSentence:
    """
        parse a logic term to a tuple of operation and cluases

        Parameter
        ---------
        input: list 
            operation and cluases of a term

        Return
        ------
        CluaseSentence
            operation and cluase in form a CluaseSentence object 
        Examples
        -------
            >>> rawInput = 'p -> q'
            >>> input = rawInput.split()
            >>> print(parse(input))
            (<Operation.IMPLICATION: '->'>, ((<Operation.NONE: ' '>, 'p'), (<Operation.NONE: ' '>, 'q')))
            >>> rawInput = '( ~ p) \\/ ( q <->)'
            >>> input = rawInput.split()
            >>> print(parse(input))
            (<Operation.DISJUNCTION: '/\'>, ((<Operation.NEGATION: '~'>, ((<Operation.NONE: ' '>, 'p'),)), (<Operation.EQUVALENCE: '<->'>, ((<Operation.NONE: ' '>, 'q'), (<Operation.NONE: ' '>, 'p')))))
    """
    if(len(input) == 1):
        return CluaseSentence( Operation.NONE, input[0] )
    i = 0
    while (i != len(input)):
        if(input[i] == '('):
            begin = i+1
            countBraces = 0
            i+=1
            while(True):
                if(input[i] == '('):
                    countBraces += 1
                elif(input[i] == ')'):
                    if(countBraces == 0):
                        break
                    else:
                        countBraces -= 1
                i+=1
            if (begin == 1 and i == len(input)-1):
                return parse(input[begin:i])

        if(Operation.getOperation(input[0]) == Operation.NEGATION):
            cluase = parse(input[i+1:],)
            return CluaseSentence( Operation.getOperation(input[i]), cluase )
        if(Operation.getOperation(input[i]) != Operation.NONE):
            cluase = ( parse(input[0:i]), parse(input[i+1:len(input)]) )
            return CluaseSentence( Operation.getOperation(input[i]) , cluase )
        i+=1