# SVG path to tags

This program generates SVG tags from an SVG path. For example, given:
M100 100L200 200

It will generate:
<line x1="100" y1="100" x2="200" y2="200" />

# Run

Just use the command line to provide a PATH and have tags generated in standard output:

$ python svg-path_to_tags < M100 100L200 200
<line x1="100" y1="100" x2="200" y2="200" />

