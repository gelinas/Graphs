from util import Stack, Queue  # These may come in handy

'''
Given two words (begin_word and end_word), and a dictionary's word list, 
return the shortest transformation sequence from begin_word to end_word, such that:
Only one letter can be changed at a time.
Each transformed word must exist in the word list. 
Note that begin_word is not a transformed word.
Note:
Return None if there is no such transformation sequence.
All words contain only lowercase alphabetic characters.
You may assume no duplicates in the word list.
You may assume begin_word and end_word are non-empty and are not the same.

Sample:
begin_word = "hit"
end_word = "cog"
return: ['hit', 'hot', 'cot', 'cog']
begin_word = "sail"
end_word = "boat"
['sail', 'bail', 'boil', 'boll', 'bolt', 'boat']
beginWord = "hungry"
endWord = "happy"
None
'''

# 1. Translate the problem into graph terminology

# 2. Build your graph
# Load words from dictionary
f = open('words.txt', 'r')
# array will have O(n) lookup
# words = f.read().lower().split("\n")
# set will have O(1) lookup
words_set = set(f.read().lower().split("\n"))
f.close()

def get_neighbors(word):
    '''
    Get all words that are one letter
    away from the given word
    '''
    # get same length words first
    # find which words differ from 'word' by just one character
    # compare every word and count different characters

    # list comprehension: works, but slow
    # results = [x for x in words if len(x) == len(word) and words_are_neighbors(x, word)]
    # O(26n) or O(n) for loop
    results = []
    list_word = list(word)
    # go through each letter in the word
    for i in range(len(list_word)):
        # swap with each letter in the alphabet
        for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']:
            temp_word = list_word.copy()
            temp_word[i] = letter
            joined_word = "".join(temp_word)
            if joined_word in words_set and joined_word != word:
                results.append(joined_word)
    return results

def words_are_neighbors(w1, w2):
    '''
    remove a character index, if words still equal, words are neighbors
    w1, w2 must be equal length
    '''
    length = len(w1)
    if len(w2) != length:
        print("ERROR: w1 and w2 must be same length")
        return
    if w1 == w2:
        # print("ERROR: w1 and w2 must not be the same word")
        return False
    for i in range(1, length + 1):
        truncated_w1 = w1[:i-1] + w1[i:]
        truncated_w2 = w2[:i-1] + w2[i:]
        if truncated_w1 == truncated_w2:
            return True
    return False

# 3. Traverse your graph (BFS - shortest route)
def word_ladder(begin_word, end_word):
    '''
    Return a list containing the shortest path from
    starting_Vertex to destination_vertex in
    breadth-first order
    '''
    # Create a queue
    q = Queue()
    # Enqueue a path to starting word
    q.enqueue([begin_word])
    # Create a visited set
    visited = set()
    # While queue is not empty:
    while q.size() > 0:
        # dequeue path
        current_path = q.dequeue()
        # grab the last word from the path
        last_word = current_path[-1]
        # check if it's our target word
        if last_word == end_word:
            # if so return path
            return current_path
        # Check if it's been visited
        if last_word not in visited:
            # If not, mark as visited
            visited.add(last_word)
            # Enqueue paths to each neighbording word
            for neighbor in get_neighbors(last_word):
                new_path = current_path.copy()
                new_path.append(neighbor)
                q.enqueue(new_path)