# ternary

Full context is discussed in this blog post - [Hidden Messages and an Optimal Ternary Scarf](https://oatzy.github.io/2024/01/20/hidden-message-ternary-scarf.html)

But the gist of it is - find a way of translating text into a base 3 string such that the result is 'aesthetically pleasing'

There are three scripts, which feed into each other:
1) processes an input text to generate n-gram frequencies (2-gram by default)
2) using the frequencies, generate a mapping of letters to base3 triples
3) use the generated mapping to translate an input text into a base 3 string

The format for the generate mappings is a string of the alphabet such that the first character maps to 1, the second to 2, etc.
