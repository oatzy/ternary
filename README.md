# ternary

Full context will be discussed in a blog post, but the gist of it is - find a way of translating text into a base 3 string such that the result is 'aesthetically pleasing'

There are three scripts, which feed into each other:
1) processes an input text to generate n-gram frequencies (2-gram by default)
2) using the frequencies, generate a mapping of letters to base3 triples
3) use the generated mapping to translate an input text into a base 3 string
