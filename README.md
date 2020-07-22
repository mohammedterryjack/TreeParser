# TreeParser
Parse any string into a nested Tree objects

## e.g.
```python 
EXAMPLE = "(GREETING (hi) (nice) (to) (meet) (you) (NAME (FIRSTNAME (Bob) LASTNAME (Bezos))) (QUESTION (do) (you) (know) (the) (capital) (of) (LOCATION (Brazil))(?)))"

tree = Tree(representation=EXAMPLE)
tree.as_nested_dictionary
>>>{
   "GREETING": [
      "GREETING",
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
