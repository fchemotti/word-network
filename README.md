word-network
============

Tools for playing with the word network underlying google keyboard's predictive text feature.

Due to the experimental nature of the project, there is no interface. It is intended to be used in interactive Python.

This project is concerned with the phrases that can be constructed exclusively from the suggested words that the google on-screen keyboard (default for Android systems) provides. The google keyboard, after each word is entered, provides three words that are predicted likely to come next. These three suggestions depend only on the single previous word and are always the same, always in the same order. So the word suggestions together form a directed graph in which each node (word) has exactly three outgoing edges (to the three suggested next words). It turns out that there is a minimal closed subgraph of 91 words, and every path of a certain length (probably something small, like 3 or 4) ends up inside that subgraph eventually. Some of the functions in word-network.py (input_words, closure_of, find_closed_subgraph) were used to discover that graph of 91 words, which is stored as a dictionary in base91.json. The other functions (get_path, find_terminal_loop, run_until_loop4, loop_poem) are used to study the patterns that arise from repeated patterns of outgoing edge choices. All for fun.
