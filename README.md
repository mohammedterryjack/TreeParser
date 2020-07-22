# TreeParser
Parse any string into a `Tree` object for easy manipulation
Attributes include:
-    `.leaves` (these are the terminal/leaf nodes of the tree. useful to strip away labels for example)
-    `.as_nested_dictionary`  (this is a nested dictionary of the tree structure. useful to see the adult-child relation of nodes in the tree)
-    `.as_nested_list` (this is a python list of the exact tree string given)
-    `.as_list`  (a flattened list of each node in the tree in the order given in the string)
   

## Dependency Tree Example
```python 
EXAMPLE = "(GREETING (hi) (nice) (to) (meet) (you) (NAME (FIRSTNAME (Bob)) (LASTNAME (Bezos))) (QUESTION (do) (you) (know) (the) (capital) (of) (LOCATION (Brazil))(?)))"

tree = Tree(representation=EXAMPLE)
```

```
tree.leaves
>>> ['hi', 'nice', 'to', 'meet', 'you', 'Bob', 'Bezos', 'do', 'you', 'know', 'the', 'capital', 'of', 'Brazil', '?']
```

```
tree.as_nested_dictionary
>>>{
   "GREETING": [
      "hi",
      "nice",
      "to",
      "meet",
      "you",
      "NAME",
      "QUESTION"
   ],
   "NAME": [
      "FIRSTNAME",
      "LASTNAME"
   ],
   "FIRSTNAME": [
      "Bob"
   ],
   "LASTNAME": [
      "Bezos"
   ],
   "QUESTION": [
      "do",
      "you",
      "know",
      "the",
      "capital",
      "of",
      "LOCATION",
      "?"
   ],
   "LOCATION": [
      "Brazil"
   ]
}
```

```
tree.as_nested_list
>>>['GREETING ', ['hi'], ['nice'], ['to'], ['meet'], ['you'], ['NAME ', ['FIRSTNAME ', ['Bob'], ' LASTNAME ', ['Bezos']]], ['QUESTION ', ['do'], ['you'], ['know'], ['the'], ['capital'], ['of'], ['LOCATION ', ['Brazil']], ['?']]]
```

```
tree.as_list
>>>['GREETING', 'hi', 'nice', 'to', 'meet', 'you', 'NAME', 'FIRSTNAME', 'Bob', 'LASTNAME', 'Bezos', 'QUESTION', 'do', 'you', 'know', 'the', 'capital', 'of', 'LOCATION', 'Brazil', '?']
```

## Arithmetic Example
```
EXAMPLE = "( * (+ (5) (2) ) (- (3) (4) ) )"
tree = Tree(representation=EXAMPLE)
```

```
tree.leaves
>>>['5', '2', '3', '4']
```

```
tree.as_nested_dictionary
>>>{
   "*": [
      "+",
      "-"
   ],
   "+": [
      "5",
      "2"
   ],
   "-": [
      "3",
      "4"
   ]
}
```
