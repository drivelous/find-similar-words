<h1>Find Similar Words</h1>

<p>This is a little script I wrote for the extra credit portion of the final assignment of a a computer algorithms MOOC.
I believe it shows that I have a basic fundamental understanding of Big O and understand the underlying time complexity of
Python operations.</p>

<p>I also think it's really cool!</p>

<p>The naive implementation of this algorithm takes a word from user input and computes a score for every word in the
Scrabble dictionary. This score helps compute the edit distance, which is the minimum amount of alterations to turn
one word into another word (EX: 'humble' is an edit distance of 1 away from 'bumble' and 'firefly' is an edit distance
of 2 away from 'finely').</p>

<h3>Analysis of naive implementation</h3>
```python
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
```

<p>Taking a word of length <em><strong>x</strong></em> and a list of words <em><strong>w</strong></em> consisting of words length <em><strong>y</strong></em>, the time 
complexity of finding the global alignment is <em><strong>O(wxy)</strong></em>. Since the Scrabble word list has almost 80,000 words and
the average length of each word is 6.74, an algorithm that needs to compute the alignment of each word has a cap on speed.</p>

<h3>Analysis of optimized implementation</h3>

```python
def check_spelling_optimized(checked_word, word_list):
    """
    Returns set of words within distance of 2 that match
    misspelled word
    """
    matched = set([])
    for idx1 in range(len(checked_word) + 1):
        for letter1 in ALPHABET:
            for idx2 in range(idx1, len(checked_word) + 2):
                for letter2 in ALPHABET: 
                    try_rep = (checked_word[0:idx1] + letter1
                                        + checked_word[idx1+1:idx2]
                                        + letter2
                                        + checked_word[idx2+1:])
                    try_hyb1 = (checked_word[0:idx1] + letter1
                                        + checked_word[idx1+1:idx2]
                                        + letter2
                                        + checked_word[idx2:])
                    try_hyb2 = (checked_word[0:idx1] + letter1
                                        + checked_word[idx1:idx2]
                                        + letter2
                                        + checked_word[idx2+1:])
                    try_ins = (checked_word[0:idx1] + letter1
                                        + checked_word[idx1:idx2]
                                        + letter2
                                        + checked_word[idx2:])

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
```

<p>Given a word of length <em><strong>x</strong></em> and an edit distance <em><strong>d</strong></em>, the optimized version that takes <em><strong>O(x^d)</strong></em> running time.
It takes advantage of the facts that:</p>

<ol>
<li>Python set's membership check is <em><strong>O(1)</strong></li>
<li>The average letter of each word in the Scrabble list is 6.74</li>
<li>There are only 27 characters in each word to check against (A-Z + the empty string)</li>
</ol>

<p>Since the extra credit question asked for an edit distance of 2, the algorithm uses two for loops that iterate over every position of the word (the levels of nesting depends on the desired edit distance). In each loop, four strings are created that take the target word and add two letters at a position, replace two letters at a
position, add at one position and replace in one position, and vice versa. If any of these new strings are in the Scrabble
word list, it's added to the 'matched' list.</p>

<h3>In practice</h3>
<p>You can pass the desired word as an argument at execution or you can enter it at the prompt.</p>
<code><pre>python check_spelling.py internet</pre></code>
<p>Results:</p>
<pre><code>
Loaded 79339 data points
Slow algorithm results
1 internee
2 intercut
3 interned
4 interns
5 intersex
6 interbed
7 interrex
8 internes
9 intern
10 internal
11 intent
12 interest
13 inturned
14 intermit
15 interred
16 interact
17 interne

Fast algorithm results
1 intercut
2 internee
3 interned
4 interns
5 interact
6 interbed
7 intern
8 internes
9 interrex
10 internal
11 intent
12 interest
13 inturned
14 intermit
15 interred
16 intersex
17 interne

The starting word was internet.
The resulting lists are identical at 17 words a piece
Slow version:  6.25483703613 seconds
Optimized version:  0.0676369667053 seconds
</pre></code>

