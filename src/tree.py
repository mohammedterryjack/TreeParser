from json import dumps
from typing import Iterable, List, Dict
from collections import defaultdict
###############################
class Bracket:
    """ Bracket manipulation """

    OPEN = "("
    CLOSE = ")"
    OPEN_REPLACEMENT = '",["'
    CLOSE_REPLACEMENT = '"],"'
    COMMA = ","
    SQUARE_CLOSE = "]"
    _EMPTY_SPACE_LRG = '," "'
    _EMPTY_SPACE_SML = ',""'
    _TRAILING = '",'

    @staticmethod
    def s_are_even(text:str) -> bool:
        return text.count(Bracket.OPEN) == text.count(Bracket.CLOSE)

    @staticmethod
    def string_to_list(text:str) -> str:
        """ 
        (1(2(3)4)5) -> ['1',['2',['3'],'4'],'5']
        """
        text = Bracket.OPEN_REPLACEMENT.join(text.split(Bracket.OPEN))
        text = Bracket.CLOSE_REPLACEMENT.join(text.split(Bracket.CLOSE))
        return Bracket.strip_off_excess(text)
    
    @staticmethod
    def strip_off_excess(text:str) -> str:
        return text.replace(
            f'{Bracket._EMPTY_SPACE_LRG}{Bracket.COMMA}',Bracket.COMMA
        ).replace(
            f'{Bracket._EMPTY_SPACE_SML}{Bracket.COMMA}',Bracket.COMMA
        ).replace(
            f'{Bracket._EMPTY_SPACE_LRG}{Bracket.SQUARE_CLOSE}',Bracket.SQUARE_CLOSE
        ).replace(
            f'{Bracket._EMPTY_SPACE_SML}{Bracket.SQUARE_CLOSE}',Bracket.SQUARE_CLOSE
        ).strip(Bracket._TRAILING)

class Tree:
    """ parse tree strings """
    def __init__(self, representation:str) -> None:
        assert(Bracket.s_are_even(text=representation))
        self.as_nested_list = eval(Bracket.string_to_list(representation.strip()))
        assert(self.only_one_root(self.as_nested_list))
        self.as_list = self.avoid_duplicate_keys(self.flatten(self.as_nested_list))
        self.as_nested_dictionary = self.construct_nested_dictionary(
            flat_list=self.as_list,
            depths=list(self.enumerate_depth(self.as_nested_list))
        )

    def __str__(self) -> str:
        return dumps(self.as_nested_dictionary,indent=3)
    
    @staticmethod
    def flatten(nested_list:list) -> Iterable:
        """
        [1,[2],[3,[4,5],[6]],[[[[7]]]]] 
        -> [1,2,3,4,5,6,7] 
        """
        for sublist in nested_list:
            if isinstance(sublist, list):
                yield from Tree.flatten(sublist)
            else:
                yield sublist.strip()
    
    @staticmethod
    def enumerate_depth(nested_list:list,depth:int=0):
        """
        [A,[B],[C,[D,E],[F]],[[[[G]]]]] 
        -> [0,1,1,2,2,2,4] 
        """ 
        for sublist in nested_list:
            if isinstance(sublist, list):
                yield from Tree.enumerate_depth(sublist,depth+1)
            else:
                yield depth
    
    @staticmethod
    def construct_nested_dictionary(flat_list:List[str],depths:List[int]) -> Dict[str,List[str]]:
        indexes = range(len(flat_list))
        return Tree.replace_indexes_for_strings(
            slot_word_index_map = Tree.convert_reference_slot_list_to_map(
                reference_slot_indexes = Tree.map_words_to_slots(
                    indexes = indexes,
                    depths = depths,
                    depth_changes = Tree.value_difference(values=depths)
                ),
                word_indexes = indexes
            ),
            indexes_to_words = dict(zip(indexes,flat_list)),
        )

    @staticmethod
    def avoid_duplicate_keys(words:List[str]) -> List[str]:
        """
        ensures all keys are unique to avoid key clash in dictionary
        """
        word_counter = {}
        words_without_duplicate_keys = []
        for word_ in words:
            if ":" in word_:
                if word_ in word_counter:
                    word_counter[word_] += 1
                else:
                    word_counter[word_] = 0
                word = f"{word_}_{word_counter[word_]}"
            else:
                word = word_
            words_without_duplicate_keys.append(word)
        return words_without_duplicate_keys

    @staticmethod
    def map_words_to_slots(indexes:List[int],depths:List[int],depth_changes:List[int]) -> Iterable[int]:
        """
        indexes:       [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21]
        depth_changes: [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1,-1, 0, 1,-1, 0, 1,-1, 0, 1, 0]
        -->            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,10, 1, 1,13, 1, 1,16, 1, 1,19,19]
        """
        depth_to_slot_index_map = {0:0}
        return map(
            lambda index,depth,depth_change: Tree.update_map_in_place_and_retrieve_index(
                current_depth=depth,
                reference_index=index-1,
                update_map=bool(max(0,depth_change)),
                depth_index_map=depth_to_slot_index_map
            ), 
            indexes, 
            depths, 
            depth_changes
        )

    @staticmethod
    def update_map_in_place_and_retrieve_index(
        current_depth:int, 
        reference_index:int, 
        update_map:bool, 
        depth_index_map:Dict[int,int]
    ) -> int:
        if update_map: 
            depth_index_map[current_depth] = reference_index
        return depth_index_map[current_depth]
    
    @staticmethod
    def value_difference(values:List[int]) -> List[int]:
        """
        get difference between current and previous values
        values:  [0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 2, 2, 3, 2, 2, 3, 2, 2, 3, 3]
        detlas:  [0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1,-1, 0, 1,-1, 0, 1,-1, 0, 1, 0]
        """
        return [0] + list(
            map(
                lambda current_value,next_value: next_value-current_value, 
                values, 
                values[1:]
            )
        )

    @staticmethod
    def convert_reference_slot_list_to_map(reference_slot_indexes:List[int], word_indexes:List[int]) -> Dict[int,List[int]]:
        """
        reference_slot_indexes:  [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1,10, 1, 1,13, 1, 1,16, 1, 1,19,19]
        word_indexes:            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21]
        -> {
            0:  [0,1],
            1:  [2,3,4,5,6,7,8,9,12,13,15,16,18,19],
            10: [11],
            13: [14],
            16: [17],
            19: [20,21]
        }
        """
        map_slot_indexes_to_word_indexes = defaultdict(list)
        for slot_index,word_index in zip(reference_slot_indexes, word_indexes):
            map_slot_indexes_to_word_indexes[slot_index].append(word_index)
        return map_slot_indexes_to_word_indexes
    
    @staticmethod
    def replace_indexes_for_strings(slot_word_index_map:Dict[int,List[int]],indexes_to_words:Dict[int,str]) -> Dict[str,List[str]]:
        return dict(
            map(
                lambda slot_index,word_indices: (
                    indexes_to_words.get(slot_index),
                    list(map(indexes_to_words.get,word_indices))
                ), 
                slot_word_index_map, 
                slot_word_index_map.values()
            )
        )    
    
    @staticmethod
    def only_one_root(parsed_tree:list) -> bool:
        """ 
        if there is more than one root node, 
        the parsed tree will be a tuple of lists 
        rather than a single list
        """
        return isinstance(parsed_tree, list)