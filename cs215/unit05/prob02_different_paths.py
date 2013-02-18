"""
Use your code from earlier to change the Marvel graph to only have characters
as nodes. Use 1.0/count as the weight, where count is the number of comic books
each character appeared in together.

For each character in this list
    'SPIDER-MAN/PETER PAR'
    'GREEN GOBLIN/NORMAN '
    'WOLVERINE/LOGAN '
    'PROFESSOR X/CHARLES '
    'CAPTAIN AMERICA'
search your weighted graph. Find all the characters where the shortest path by
weight to that character is different by weight from the shortest path measured
by counting the number of hops.

For example, there is a direct link between 'SPIDER-MAN/PETER PAR' and 'YAP',
but the shortest weighted path between the two is
['SPIDER-MAN/PETER PAR', 'WOLVERINE/LOGAN ', 'SHADOWCAT/KATHERINE ', 'YAP']

As another example, the shortest path by hops between 'WOLVERINE/LOGAN ' and
'HOARFROST/' is
    ['WOLVERINE/LOGAN ', 'CITIZEN V II/HELMUT ', 'HOARFROST/']
but by weight, the shortest path is
    ['WOLVERINE/LOGAN ', 'CYCLOPS/SCOTT SUMMER', 'BEAST/HENRY &HANK& P',
        'CAPTAIN AMERICA', 'HAWK', 'HOARFROST/']

We've given you two of the paths. There are over 20 000 more.
When you've found the total number, fill your answer in box.
"""
