"""Typing test implementation"""

from utils import *
from ucb import main, interact, trace
from datetime import datetime


###########
# Phase 1 #
###########


def choose(paragraphs, select, k):
    """Return the Kth paragraph from PARAGRAPHS for which SELECT called on the
    paragraph returns true. If there are fewer than K such paragraphs, return
    the empty string.
    """
    # BEGIN PROBLEM 1
    "*** YOUR CODE HERE ***"
    k_true = 0
    for elem in range(len(paragraphs)):
        if select(paragraphs[elem]):
            if k_true == k:
                return paragraphs[elem]
            k_true += 1
    if k_true <= k:
        return ''
    if len(paragraphs)-k<= k or len(paragraphs)==0:
        return ''


    # END PROBLEM 1


def about(topic):
    """Return a select function that returns whether a paragraph contains one
    of the words in TOPIC.

    >>> about_dogs = about(['dog', 'dogs', 'pup', 'puppy'])
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup!'], about_dogs, 0)
    'Cute Dog!'
    >>> choose(['Cute Dog!', 'That is a cat.', 'Nice pup.'], about_dogs, 1)
    'Nice pup.'
    """
    assert all([lower(x) == x for x in topic]), 'topics should be lowercase.'
    # BEGIN PROBLEM 2
    "*** YOUR CODE HERE ***"
    def helper(lst):
        erase_punc = remove_punctuation(lst)
        erase_case = lower(erase_punc)
        paragraph = split(erase_case)
        for elem in topic:
            for i in paragraph:
                if i == elem:
                    return True
        return False
    return helper
    ##Make it a dictionaryyyyy

    # END PROBLEM 2


def accuracy(typed, reference):
    """Return the accuracy (percentage of words typed correctly) of TYPED
    when compared to the prefix of REFERENCE that was typed.

    >>> accuracy('Cute Dog!', 'Cute Dog.')
    50.0
    >>> accuracy('A Cute Dog!', 'Cute Dog.')
    0.0
    >>> accuracy('cute Dog.', 'Cute Dog.')
    50.0
    >>> accuracy('Cute Dog. I say!', 'Cute Dog.')
    50.0
    >>> accuracy('Cute', 'Cute Dog.')
    100.0
    >>> accuracy('', 'Cute Dog.')
    0.0
    """
    typed_words = split(typed)
    reference_words = split(reference)
    # BEGIN PROBLEM 3
    "*** YOUR CODE HERE ***"
    x = 0
    counter = 0
    smallest = min(len(typed_words), len(reference_words))
    for elem in range(smallest):
            if typed_words[elem] == reference_words[elem]:
                counter += 1
                x = counter/len(typed_words)
    return x*100.00

    # END PROBLEM 3


def wpm(typed, elapsed):
    """Return the words-per-minute (WPM) of the TYPED string."""
    assert elapsed > 0, 'Elapsed time must be positive'
    # BEGIN PROBLEM 4
    "*** YOUR CODE HERE ***"
    length = len(typed)
    words = length/5
    time = elapsed/60
    return words/time
    # END PROBLEM 4


def autocorrect(user_word, valid_words, diff_function, limit):
    """Returns the element of VALID_WORDS that has the smallest difference
    from USER_WORD. Instead returns USER_WORD if that difference is greater
    than LIMIT.
    """
    # BEGIN PROBLEM 5
    "*** YOUR CODE HERE ***"
    smallest_diff = []
    for elem in valid_words:
        if elem == user_word:
            return user_word
        else:
            difference = diff_function(user_word, elem, limit)
            smallest_diff.append(difference)
    for i in range(len(smallest_diff)):
        mini = min(smallest_diff)
        if mini > limit:
            return user_word
        elif smallest_diff[i]==mini:
            return (valid_words[i])
    # END PROBLEM 5


def swap_diff(start, goal, limit):
    """A diff function for autocorrect that determines how many letters
    in START need to be substituted to create GOAL, then adds the difference in
    their lengths.
    """
    # BEGIN PROBLEM 6
    def helper(begin, end, total, counter):
        if start == goal:
            return 0
        if len(begin)<= 0 or len(end)<=0:
            return total + abs(len(begin)-len(end))
        elif total > limit:
            return limit+1
        else:
            if begin[0:1] != end[0:1]:
                total += 1
            return helper(start[counter:len(start)], goal[counter:len(goal)], total, counter+1)
    return helper(start[0:len(start)], goal[0:len(goal)], 0, 1)
    # END PROBLEM 6

def edit_diff(start, goal, limit, tracker=0):
    """A diff function that computes the edit distance from START to GOAL."""
    if start == goal:
        return 0
    if min(len(start),len(goal))== 0:
        return max(len(start), len(goal))
    if start[0] == goal[0]: # Fill in the condition
        return 0 + edit_diff(start[1:], goal[1:], limit, tracker)
    if tracker > limit: # Feel free to remove or add additional cases
        return limit + 1
    else:
        add_diff = 1 + edit_diff(start, goal[1:], limit, tracker + 1)
        remove_diff = 1 + edit_diff(start[1:], goal, limit, tracker + 1)
        substitute_diff = 1+ edit_diff(start[1:], goal[1:], limit, tracker + 1)
        return min(add_diff, remove_diff, substitute_diff)



def final_diff(start, goal, limit):
    """A diff function. If you implement this function, it will be used."""
    assert False, 'Remove this line to use your final_diff function'




###########
# Phase 3 #
###########


def report_progress(typed, prompt, id, send):
    """Send a report of your id and progress so far to the multiplayer server."""
    # BEGIN PROBLEM 8
    "*** YOUR CODE HERE ***"
    count= 0
    for elem in range(len(typed)):
        if typed[elem] == prompt[elem]:
            count +=1
        else:
            break
    progress = count/len(prompt)
    dict = {'id': id, 'progress': progress}
    i = send(dict)
    return progress

    # END PROBLEM 8


def fastest_words_report(word_times):
    """Return a text description of the fastest words typed by each player."""
    fastest = fastest_words(word_times)
    report = ''
    for i in range(len(fastest)):
        words = ','.join(fastest[i])
        report += 'Player {} typed these fastest: {}\n'.format(i + 1, words)
    return report


def fastest_words(word_times, margin=1e-5):
    """A list of which words each player typed fastest."""
    n_players = len(word_times)
    n_words = len(word_times[0]) - 1
    assert all(len(times) == n_words + 1 for times in word_times)
    assert margin > 0
    # BEGIN PROBLEM 9
    "*** YOUR CODE HERE ***"
    time, final = [], []
    for i in range(1, len(word_times[0])):
        delta = []
        for player in word_times:
            delta += [elapsed_time(player[i]) - elapsed_time(player[i-1])]
        time.append(delta)
    for p in range(len(word_times)):
        temp = []
        for i in range(len(time)):
            if time[i][p] <= min(time[i]) + margin:
                temp += [word(word_times[p][i+1])]
        final += [temp]
    return final

    # END PROBLEM 9


def word_time(word, elapsed_time):
    """A data abstrction for the elapsed time that a player finished a word."""
    return [word, elapsed_time]


def word(word_time):
    """An accessor function for the word of a word_time."""
    return word_time[0]


def elapsed_time(word_time):
    """An accessor function for the elapsed time of a word_time."""
    return word_time[1]


enable_multiplayer = False  # Change to True when you


##########################
# Command Line Interface #
##########################


def run_typing_test(topics):
    """Measure typing speed and accuracy on the command line."""
    paragraphs = lines_from_file('data/sample_paragraphs.txt')
    select = lambda p: True
    if topics:
        select = about(topics)
    i = 0
    while True:
        reference = choose(paragraphs, select, i)
        if not reference:
            print('No more paragraphs about', topics, 'are available.')
            return
        print('Type the following paragraph and then press enter/return.')
        print('If you only type part of it, you will be scored only on that part.\n')
        print(reference)
        print()

        start = datetime.now()
        typed = input()
        if not typed:
            print('Goodbye.')
            return
        print()

        elapsed = (datetime.now() - start).total_seconds()
        print("Nice work!")
        print('Words per minute:', wpm(typed, elapsed))
        print('Accuracy:        ', accuracy(typed, reference))

        print('\nPress enter/return for the next paragraph or type q to quit.')
        if input().strip() == 'q':
            return
        i += 1


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions."""
    import argparse
    parser = argparse.ArgumentParser(description="Typing Test")
    parser.add_argument('topic', help="Topic word", nargs='*')
    parser.add_argument('-t', help="Run typing test", action='store_true')

    args = parser.parse_args()
    if args.t:
        run_typing_test(args.topic)
