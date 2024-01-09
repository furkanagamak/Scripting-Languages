def isValid(s):
    if not s:
        return 'YES'
    
    theCharacterCounter = {}
    for theCharacter in s:
        if theCharacter in theCharacterCounter:
            theCharacterCounter[theCharacter] += 1
        else:
            theCharacterCounter[theCharacter] = 1
    
    theCharacterRepeats = {}
    for counterOfRepeats in theCharacterCounter.values():
        if counterOfRepeats in theCharacterRepeats:
            theCharacterRepeats[counterOfRepeats] += 1
        else:
            theCharacterRepeats[counterOfRepeats] = 1

    keysOftheCharacters = list(theCharacterRepeats.keys())
    
    if len(keysOftheCharacters) == 1:
        return 'YES'
    
    if len(keysOftheCharacters) == 2:
        minimumCharacterRepeat = min(keysOftheCharacters)
        maximumCharacterRepeat = max(keysOftheCharacters)
        
        if (1 in theCharacterRepeats and theCharacterRepeats[1] == 1) or (theCharacterRepeats[minimumCharacterRepeat] == 1 and minimumCharacterRepeat + 1 == maximumCharacterRepeat):
            return 'YES'
        
        if theCharacterRepeats[maximumCharacterRepeat] == 1 and maximumCharacterRepeat - 1 == minimumCharacterRepeat:
            return 'YES'
    
    return 'NO'

def isBalanced(seqBrackets: str) -> str:
    bracketsStack = []
    listOfBrackets = {')': '(', '}': '{', ']': '['}

    for theCharacter in seqBrackets:
        if theCharacter in "({[":
            bracketsStack.append(theCharacter)
        elif theCharacter in ")}]":
            lastCharacter = bracketsStack.pop() if bracketsStack else 'g'
            
            if listOfBrackets[theCharacter] != lastCharacter:
                return "NO"
            
    return "YES" if not bracketsStack else "NO"

from collections import deque

def isBalancedString(seqBrackets):
    theBracketsStack = []
    for theCharacter in seqBrackets:
        if theCharacter in ["(", "{", "["]:
            theBracketsStack.append(theCharacter)
        else:
            if not theBracketsStack:
                return False
            if theCharacter == ")" and theBracketsStack[-1] != "(":
                return False
            if theCharacter == "}" and theBracketsStack[-1] != "{":
                return False
            if theCharacter == "]" and theBracketsStack[-1] != "[":
                return False
            theBracketsStack.pop()
    return not theBracketsStack

def countValidStrings(seqBrackets):
    if isBalancedString(seqBrackets):
        return 0
    
    bracketsVisited = set()
    queueOfBrackets = deque([seqBrackets])
    balancedSequences = set()
    isBracketFound = False
    
    while queueOfBrackets and not isBracketFound:
        lengthOfSequence = len(queueOfBrackets)
        for iteration in range(lengthOfSequence):
            iteration = iteration + 1
            theBracketString = queueOfBrackets.popleft()
            for i in range(len(theBracketString)):
                uniqueString = theBracketString[:i] + theBracketString[i+1:]
                if uniqueString not in bracketsVisited:
                    bracketsVisited.add(uniqueString)
                    if isBalancedString(uniqueString):
                        balancedSequences.add(uniqueString)
                        isBracketFound = True
                    else:
                        queueOfBrackets.append(uniqueString)
                    
    return len(balancedSequences)

class Node:
    def __init__(self, elementTree, descendantTreeLeft=None, descendantTreeRight=None):
        self.elementTree = elementTree
        self.descendantTreeLeft = descendantTreeLeft
        self.descendantTreeRight = descendantTreeRight
    
    def preOrder(self):
        if self is None:
            return []
        finalOrder = [self.elementTree]
        if self.descendantTreeLeft:
            finalOrder.extend(self.descendantTreeLeft.preOrder())
        if self.descendantTreeRight:
            finalOrder.extend(self.descendantTreeRight.preOrder())
        return finalOrder
    
    def inOrder(self):
        if self is None:
            return []
        finalOrder = []
        if self.descendantTreeLeft:
            finalOrder.extend(self.descendantTreeLeft.inOrder())
        finalOrder.append(self.elementTree)
        if self.descendantTreeRight:
            finalOrder.extend(self.descendantTreeRight.inOrder())
        return finalOrder
    
    def postOrder(self):
        if self is None:
            return []
        finalOrder = []
        if self.descendantTreeLeft:
            finalOrder.extend(self.descendantTreeLeft.postOrder())
        if self.descendantTreeRight:
            finalOrder.extend(self.descendantTreeRight.postOrder())
        finalOrder.append(self.elementTree)
        return finalOrder
    
    def getHeight(self, elementTree):
        if self is None:
            return -1
        if self.elementTree == elementTree:
            return 0
        heightOfLeftSubtree = self.descendantTreeLeft.getHeight(elementTree) if self.descendantTreeLeft else -1
        heightOfRightSubtree = self.descendantTreeRight.getHeight(elementTree) if self.descendantTreeRight else -1
        maxHeightOfTrees = max(heightOfLeftSubtree, heightOfRightSubtree)
        return maxHeightOfTrees + 1 if maxHeightOfTrees != -1 else -1
    
    def sumTree(self):
        if self is None:
            return 0
        sumOfRootTree = self.elementTree
        if self.descendantTreeLeft:
            sumOfRootTree += self.descendantTreeLeft.sumTree()
        if self.descendantTreeRight:
            sumOfRootTree += self.descendantTreeRight.sumTree()
        return sumOfRootTree
