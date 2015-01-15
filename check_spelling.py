import sys
import time

from matrices import build_scoring_matrix
from matrices import compute_alignment_matrix
from matrices import compute_global_alignment

ALPHABET = set(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
              'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '', '-'])

SCORING = build_scoring_matrix(ALPHABET, 2, 1, 0)

def load_words(txt_file):
    """
    Loads words from word TXT file
    into list format
    """
    word_set = set([])
    data_file = open(txt_file, 'r+')
    data = data_file.read()
    data_lines = data.split('\n')
    data_lines.pop()
    print "Loaded", len(data_lines), "data points"
    data_tokens = [line for line in data_lines]
    for token in data_tokens:
    	word_set.add(str(token))

    return word_set

def check_spelling(checked_word, dist, word_list):
  """
  Returns set of words from word_list that match
  checked_word within provided edit distance dist
  """
  matched = set([])
  for word in word_list:
      len_words = len(checked_word) + len(word)
      alignment = compute_alignment_matrix(checked_word, word, SCORING, True)
      g_align = compute_global_alignment(checked_word, word, SCORING, alignment)
      if len_words - g_align[0] <= dist:
          matched.add(word)

  return matched

def check_spelling_optimized(checked_word, word_list):
    """
    Returns set of words within distance of 2 that match
    misspelled word
    """
    matched = set([])
    #if checked_word not in word_list:
    for idx1 in range(len(checked_word) + 1):
        for letter1 in ALPHABET:
            for idx2 in range(idx1, len(checked_word) + 2):
                for letter2 in ALPHABET: 
                    try_rep = checked_word[0:idx1] + letter1 + checked_word[idx1+1:idx2] + letter2 + checked_word[idx2+1:]
                    try_hyb1 = checked_word[0:idx1] + letter1 + checked_word[idx1+1:idx2] + letter2 + checked_word[idx2:]
                    try_hyb2 = checked_word[0:idx1] + letter1 + checked_word[idx1:idx2] + letter2 + checked_word[idx2+1:]
                    try_ins = checked_word[0:idx1] + letter1 + checked_word[idx1:idx2] + letter2 + checked_word[idx2:]

                    # Checks if either word is in word_list
                    if try_ins in word_list:
                        matched.add(try_ins)
                    if try_hyb1 in word_list:
                        matched.add(try_hyb1)
                    if try_hyb2 in word_list:
                        matched.add(try_hyb2)
                    if try_rep in word_list:
                        matched.add(try_rep)

    return matched

def main():
    if len(sys.argv) > 1:
        check_word = sys.argv[1]
    else:
        try:
            check_word = raw_input('Enter a word: ')
        except (KeyboardInterrupt, EOFError):
             print "\n\nYou stopped the process. Aborting.\n"
             return
    if not check_word:
        print "You didn't enter a word\n"
        return

    word_list = load_words('scrabble_words.txt')

    try:
        start_slow = time.time()
        results1 = check_spelling(check_word, 2, word_list)
        end_slow = time.time()
        results_slow = end_slow - start_slow

        start_fast = time.time()
        results2 = check_spelling_optimized(check_word, word_list)
        end_fast = time.time()
        results_fast = end_fast - start_fast

        print "\nSlow algorithm results"
        for count, word in enumerate(results1, start=1):
            print count, word

        print "\nFast algorithm results"
        for count, word in enumerate(results2, start=1):
            print count, word

        print "\nThe starting word was %s." % check_word
        if len(results1) == len(results2):
            print "The resulting lists are identical at %d words a piece" % len(results1)
        print "Slow version: ", results_slow, "seconds"
        print "Optimized version: ", results_fast, "seconds\n"

    except KeyboardInterrupt:
        print "\nYou stopped the process. Aborting."
        return

if __name__ == '__main__':
    main()