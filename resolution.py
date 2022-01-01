import re
from enum import Enum
from typing import Union

__all__ = ['Operation', 'ClauseSentence', 'parse', 'prove']
__author__ = 'Mahdi Kashani'
__title__ = 'Resolution method'


replacement = {}
is_firstOrder = False

#=====================
class Operation(Enum):
#=====================
    """
        Attributs
        ---------
            NONE : no Operation
            NEGATION : ~
            CONJUNCTION : \\/
            DISJUNCTION : /\\
            IMPLICATION : ->
            EQUIVALENCE : <->

        Methods
        -------
            getOperation(operand)
                return your operand in Operation type
            symbol
                return the symbol of operation unicode
    """
    NONE        = ' '     # a , b
    NEGATION    = '~'     # ~a , ~b
    CONJUNCTION = '\\/'   # a \/ b
    DISJUNCTION = '/\\'   # a /\ b
    IMPLICATION = '->'    # a -> b
    EQUIVALENCE = '<->'   # a <-> b
    FORALL      = 'FA'    # FA ( f(x) )
    EXIST       = 'EX'    # EX ( f(x) )
    FUNCTION    = '()'    # f(x)

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
            return Operation.EQUIVALENCE
        elif(re.match("^FA\(\w+\)$", operand) != None):
            return Operation.FORALL
        elif(re.match("^EX\(\w+\)$", operand) != None):
            return Operation.EXIST
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
        elif(self == Operation.EQUIVALENCE):
            return '\u27F7'
        else:
            return ''   


#=====================
class ClauseSentence:
#=====================
    clause: Union[tuple, str]
    operand: Operation
    def __init__(self, operand: Operation, clause: tuple):
        self.operand = operand
        self.clause = clause

    def toString(self):
        if(self.operand == Operation.NONE):
            return self.clause
        elif(self.operand == Operation.NEGATION):
            return '~'+self.clause[0].clause
    
    def __key(self):
        return(self.operand, self.clause)
    
    def __hash__(self) -> int:
        return hash(self.__key())

    def __eq__(self, other) -> bool:
        return (isinstance(other, type(self)) and (self.clause, self.operand) == (other.clause, other.operand))        

    def __str__(self):
        if(self.operand == Operation.NONE or self.operand == Operation.NEGATION):
            op = self.operand.symbol
            return f'{op} {str(self.clause.__str__())}'
        elif(self.operand == Operation.FUNCTION):
            return f'{self.clause[0]}({self.clause[1]})'
        op = self.operand.symbol
        return f'{self.clause[0].__str__()} {op} {self.clause[1].__str__()}'
    
#----------------------------------
def convert(term: ClauseSentence):
#----------------------------------
    """
        convert implication and equivalence to disjunction or conjunction
        and if term has not implication or equivalence return term without changing
    """
    isNegation = False
    if(term.operand == Operation.NEGATION):
        # delete negation and then add in the end 
        term = term.clause[0]
        isNegation = True
    
    # implication convert to conjunction
    if(term.operand == Operation.IMPLICATION):
        clause = (applyNegation(ClauseSentence(Operation.NEGATION, (term.clause[0],) )), term.clause[1])
        res = ClauseSentence( Operation.CONJUNCTION, clause )
        if(isNegation):
            return applyNegation(ClauseSentence( Operation.NEGATION, (res,)))
        return res
    # equivalence convert to disjunction
    elif(term.operand == Operation.EQUIVALENCE):
        clause1 = applyNegation(ClauseSentence( Operation.CONJUNCTION, (applyNegation(ClauseSentence(Operation.NEGATION, (term.clause[0],))), term.clause[1])))
        clause2 = applyNegation(ClauseSentence( Operation.CONJUNCTION, (term.clause[0], applyNegation(ClauseSentence(Operation.NEGATION, (term.clause[1],))))))
        res = ClauseSentence(Operation.DISJUNCTION, (clause1, clause2))
        if(isNegation):
            return applyNegation(ClauseSentence( Operation.NEGATION, (res,)))
        return res

#------------------------------------------------
def simplificationNegation(term: ClauseSentence):
#------------------------------------------------
    """
        delete repetitious negations in a variable or terms
        for example ~ ( ~ A ) convert to A or ~ ( ~ ( ~ A ) ) covert to ~ A
    """
    while(term.operand == Operation.NEGATION and term.clause[0].operand == Operation.NEGATION):
        term = term.clause[0].clause[0]
    return term

#---------------------------------------
def distribution(term: ClauseSentence):
#---------------------------------------
    """
        if term in form of A \/ ( B /\ C ), this function converts this term
        in form of (A \/ B) /\ (A \/ C)
    """
    if(term.operand in [Operation.NEGATION, Operation.NONE]):
        return None
    
    # if term in format of ( B /\ C ) \/ A
    elif(
        not term.clause[0].operand == Operation.NONE
        and term.clause[1].operand == Operation.NONE
        and not term.clause[0].operand == term.operand
        and term.clause[0].operand == Operation.DISJUNCTION
        and term.operand == Operation.CONJUNCTION
    ):
        clause1 = ClauseSentence(term.operand, (term.clause[0].clause[0], term.clause[1]))
        clause2 = ClauseSentence(term.operand, (term.clause[0].clause[1], term.clause[1]))
        return ClauseSentence(term.clause[0].operand, (clause1, clause2))

    # if term in format of A \/ ( B /\ C )
    elif(
        not term.clause[1].operand == Operation.NONE
        and term.clause[0].operand == Operation.NONE
        and not term.clause[1].operand == term.operand
        and term.clause[1].operand == Operation.DISJUNCTION
        and term.operand == Operation.CONJUNCTION
    ):
        clause1 = ClauseSentence(term.operand, (term.clause[1].clause[0], term.clause[0]))
        clause2 = ClauseSentence(term.operand, (term.clause[1].clause[1], term.clause[0]))
        return ClauseSentence(term.clause[1].operand, (clause1, clause2))

#--------------------------------------------
def splitByDisjunction(term: ClauseSentence):
#--------------------------------------------
    """
        split term to a set of premises list for using in resolution
        
        (A /\ B /\ ...) to {A}, {B}, ...

        (A \/ B \/ ...) to {A,B,...}
    """
    result = []
    if(term.operand == Operation.NEGATION):
        term = applyNegation(term)

    # (A /\ B /\ ...)
    if(term.operand == Operation.DISJUNCTION):
        clause1 = term.clause[0]
        clause2 = term.clause[1]
        if(not clause1.operand == Operation.NONE and not (clause1.operand == Operation.NONE and clause1.clause[0].operand == Operation.NEGATION)):
            result += (splitByDisjunction(clause1))
        else:
            result.append({clause1.toString()})
        if(not clause2.operand == Operation.NONE and not (clause2.operand == Operation.NONE and clause1.clause[0].operand == Operation.NEGATION)):
            result += (splitByDisjunction(clause2))
        else:
            result.append({clause2.toString()})
        return result

    # (A \/ B \/ ...)
    elif(term.operand == Operation.CONJUNCTION):
        clause1 = splitByDisjunction(term.clause[0])
        clause2 = splitByDisjunction(term.clause[1])
        return clause1 + clause2
    
    # single variabale
    else:
        return [set([term.toString()])]

#----------------------------------------
def applyNegation(term: ClauseSentence):
#----------------------------------------
    """
        apply negation and return the simpilication for of clause
        for example ~ ( A \/ B) covert to ( ~A /\ ~B)
    """
    if(not term.operand == Operation.NEGATION):
        return term
    else:
        term = term.clause[0]
        # if still equivalence or implication did not converted
        if(term.operand in [Operation.EQUIVALENCE, Operation.IMPLICATION]):
            term = convert(term)
        
        # conjunction
        if(term.operand == Operation.CONJUNCTION):
            clause1 = applyNegation(simplificationNegation(ClauseSentence(Operation.NEGATION, (term.clause[0],))))
            clause2 = applyNegation(simplificationNegation(ClauseSentence(Operation.NEGATION, (term.clause[1],))))
            return ClauseSentence( Operation.DISJUNCTION, (clause1 , clause2) )
        
        # disjunction
        elif(term.operand == Operation.DISJUNCTION):
            clause1 = applyNegation(simplificationNegation(ClauseSentence(Operation.NEGATION, (term.clause[0],))))
            clause2 = applyNegation(simplificationNegation(ClauseSentence(Operation.NEGATION, (term.clause[1],))))
            return ClauseSentence( Operation.CONJUNCTION, (clause1 , clause2) )
        
        # first order operations
        elif(term.operand == Operation.EXIST):
            return ClauseSentence(Operation.FORALL, (applyNegation(ClauseSentence(Operation.NEGATION, (term.clause[0],))), term.clause[1]))
        elif(term.operand == Operation.FORALL):
            return ClauseSentence(Operation.EXIST, (applyNegation(Operation.NEGATION, (term.clause[0],)), term.clause[1]))
       
        elif(term.operand == Operation.NEGATION):
            return applyNegation(term.clause[0])
        else:
            return ClauseSentence(Operation.NEGATION, (term,))


#----------------------------------------
def deleteForalls(term: ClauseSentence):
#----------------------------------------
    """
        delete all 'for alls' operations
    """
    if(term.operand == Operation.FORALL):
        term = term.clause[0]
    elif(not term.operand in [Operation.NONE, Operation.FUNCTION]):
        if(not term.operand in [Operation.NEGATION, Operation.EXIST]):
            term.clause = (deleteForalls(term.clause[0]), term.clause[1])
            term.clause = (term.clause[0], deleteForalls(term.clause[1]))
        else:
            term.clause = (deleteForalls(term.clause[0]),)
    return term
            

def replace(term: ClauseSentence, var: str):
    if(term.operand == Operation.FUNCTION):
        if(term.clause[1] == var):
            rep = replacement.get(var, f'rep{len(replacement) + 1}')
            replacement[term.clause[1]] = rep
            term.clause = (term.clause[0], rep)
    else:
        if(not term.operand in [Operation.NONE, Operation.FUNCTION]):
            if(not term.operand in [Operation.NEGATION, Operation.FORALL]):
                replace(term.clause[0], var)
                replace(term.clause[1], var)
            else:
                replace(term.clause[0], var)


#-------------------------------------
def skolemizing(term: ClauseSentence):
#-------------------------------------
    """
        delete all exist and will change variables if need
    """
    if(term.operand == Operation.EXIST):
        replace(term.clause[0], term.clause[1])
        return term.clause[0]
    elif(not term.operand in [Operation.NONE, Operation.FUNCTION]):
        if(not term.operand in [Operation.NEGATION, Operation.FORALL]):
            term.clause = (skolemizing(term.clause[0]), term.clause[1])
            term.clause = (term.clause[0], skolemizing(term.clause[1]))
        else:
            term.clause = (skolemizing(term.clause[0]),)
    return term


#----------------------------------------
def functionsToStr(term: ClauseSentence):
#----------------------------------------
    """
        convert all functions to a object likes variables
    """
    if(term.operand == Operation.FUNCTION):
        return ClauseSentence(Operation.NONE, term.__str__())
    elif(term.operand == Operation.NONE):
        pass
    else:
        if(not term.operand in [Operation.NEGATION, Operation.EXIST]):
            term.clause = (functionsToStr(term.clause[0]), term.clause[1])
            term.clause = (term.clause[0], functionsToStr(term.clause[1]))
        else:
            term.clause = (functionsToStr(term.clause[0]),)
    return term


#-----------------------------------
def simplificationFirstOrder(term):
#-----------------------------------
    term = applyNegation(term)
    term = skolemizing(term)
    term = deleteForalls(term)
    term = functionsToStr(term)
    return term


#----------------------------------------------
def subscription(premise1: set, premise2: set):
#----------------------------------------------
    """
        return a set without every repetitious variables in 2 set of premises
        this function return a generator of set
    """
    for pre1 in premise1:
        for pre2 in premise2:
            if((pre1 in pre2 and pre2 == '~'+pre1) or (pre2 in pre1 and pre1 == '~'+pre2)):
                temp = premise1.copy()
                temp.remove(pre1)
                temp |= premise2.copy()
                temp = temp
                temp.remove(pre2)
                yield (temp)


#------------------------------
def isProvable(premises: list):
#------------------------------
    """
        if premises (whitout preprocess) can prove conclusion return True otherwise False
        premises is a set of variable list for check with resolution principle are these conflict or not 
    """
    for pre in premises:
        for other in premises:
            if(other != pre):
                new = subscription(pre, other)
                for x in new:
                    if(x == None):
                        continue
                    elif(len(x) == 0):
                        return True
                    elif(not x in premises):
                        premises.append(x)
    return False


#-----------------------------------------------------
def prove(premises: list[str], conclusion: str = ""):
#-----------------------------------------------------
    """
        preprocess and check could prove conclusion from premises

        convert all premisers to set of 

        Parameter
        ----------
        premises: list[str]
            list of premises

        conclusion: str
            the clause should conclude
    
        Return
        ------
        bool
            return True if provable otherwise return False

        Examples:
        ---------
            >>> prove(['p /\\ q', 'q'], 'p')
            True
            >>> prove(['~ q' , ' p -> q'], '~ p')
            True
            >>> prove(['p \\/ q', 'p'], 'q')
            False
            
            also you can see example.py for more examples.

        Note
        ----
            your input should have space between each symbols
            (constant, variable, operation, braces) and for each couple
            variable and a operation put a braces. 

    """
    global is_firstOrder
    tempPremises = premises.copy()
    if (conclusion != ""):
        tempPremises.append('~ ( ' + conclusion + ' )')
    premisesClause = []
    for pre in tempPremises:
        clause = parse(pre.split())
        if(is_firstOrder):
            clause = simplificationFirstOrder(clause)
        if(not clause.operand == Operation.NONE):
            if(clause.operand == Operation.NEGATION):
                clause = simplificationNegation(clause)
            if(clause.operand == Operation.IMPLICATION or clause.operand == Operation.EQUIVALENCE):
                clause = convert(clause)
            res = distribution(clause)
            if(not res == None):
                clause = res
        is_firstOrder = False
        premisesClause += splitByDisjunction(clause)
    
    temp = []
    [temp.append(x) for x in premisesClause if x not in temp]
    premisesClause = temp
    return isProvable(premisesClause), premisesClause

#------------------------------------------
def parse(input: list) -> ClauseSentence:
#------------------------------------------
    """
        parse a logic term to a ClauseSentence

        Parameter
        ---------
        input: list 
            operation and clauses of a term

        Return
        ------
        ClauseSentence
            operation and clause inform a ClauseSentence object 

        Examples
        -------
            >>> rawInput = 'p -> q'
            >>> input = rawInput.split()
            >>> print(parse(input))
            (<Operation.IMPLICATION: '->'>, ((<Operation.NONE: ' '>, 'p'), (<Operation.NONE: ' '>, 'q')))
            >>> rawInput = '( ~ p) \\/ ( q <->)'
            >>> input = rawInput.split()
            >>> print(parse(input))
            (<Operation.DISJUNCTION: '/\'>, ((<Operation.NEGATION: '~'>, ((<Operation.NONE: ' '>, 'p'),)), (<Operation.EQUIVALENCE: '<->'>, ((<Operation.NONE: ' '>, 'q'), (<Operation.NONE: ' '>, 'p')))))
    """
    global is_firstOrder
    if(len(input) == 1):
        if(re.match("^\w+\(\w+\)", input[0]) != None):
            name = re.findall("^\w+(?=\()", input[0])[0]
            var = re.findall("(?<=\()\w+(?=\))", input[0])[0]
            return ClauseSentence(Operation.FUNCTION, (name, var))
        return ClauseSentence( Operation.NONE, input[0] )
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
            clause = parse(input[i+1:])
            return ClauseSentence( Operation.getOperation(input[i]), (clause,) )
        if(Operation.getOperation(input[0]) == Operation.FORALL
            or Operation.getOperation(input[0]) == Operation.EXIST
        ):
            is_firstOrder = True
            name = re.findall("(?<=\()\w+(?=\))", input[0])[0]
            clause = parse(input[i+1:])
            return ClauseSentence( Operation.getOperation(input[i]), (clause,name) )
        if(Operation.getOperation(input[i]) != Operation.NONE):
            clause = ( parse(input[0:i]), parse(input[i+1:len(input)]) )
            return ClauseSentence( Operation.getOperation(input[i]) , clause )
        i+=1
    

if __name__ == "__main__":
    import cmd
    commands = []
    class CmdParse(cmd.Cmd):
        intro = 'Welcome to the resolution shell.   Type help or ? to list commands.\n' 
        prompt = "> "
        def default(self, line):
            line = line.split(',')
            if len(line) == 1:
                print(prove(line))
            else:
                print(prove(line[:-1], line[-1]))
            commands.append(line)
        def do_help(self, line):
            if line == "exit":
                print(self.do_exit.__doc__)
            else:
                print(" your clause should be written with space between symbols and variable and also put tuple variable in ( )")
        def empty(self, line):
            self.do_help()
        def do_exit(self, arg):
            """ exit from shell mode """
            exit(0)
    CmdParse().cmdloop()