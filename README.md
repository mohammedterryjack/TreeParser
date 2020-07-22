# TreeParser
Parse any string into a nested Tree objects

## Dependency Tree Example
```python 
EXAMPLE = "(GREETING (hi) (nice) (to) (meet) (you) (NAME (FIRSTNAME (Bob) LASTNAME (Bezos))) (QUESTION (do) (you) (know) (the) (capital) (of) (LOCATION (Brazil))(?)))"

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