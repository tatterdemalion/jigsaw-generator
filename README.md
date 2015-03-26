# jigsaw-generator

# Convert this:

![original](https://raw.githubusercontent.com/tatterdemalion/jigsaw-generator/master/images/test.jpg)

# To this:

![output](https://raw.githubusercontent.com/tatterdemalion/jigsaw-generator/master/images/output.jpg)

```
                 filename | directory | piece count
python jigsaw.py test.jpg   output      10
```

Every piece is a class that holds the information of the underlying image and the order on the jigsaw.

```
[0x0][1x0][2x0][3x0][4x0][5x0][6x0][7x0][8x0][9x0]
[0x1][1x1][2x1][3x1][4x1][5x1][6x1][7x1][8x1][9x1]
[0x2][1x2][2x2][3x2][4x2][5x2][6x2][7x2][8x2][9x2]
[0x3][1x3][2x3][3x3][4x3][5x3][6x3][7x3][8x3][9x3]
[0x4][1x4][2x4][3x4][4x4][5x4][6x4][7x4][8x4][9x4]
[0x5][1x5][2x5][3x5][4x5][5x5][6x5][7x5][8x5][9x5]
[0x6][1x6][2x6][3x6][4x6][5x6][6x6][7x6][8x6][9x6]
[0x7][1x7][2x7][3x7][4x7][5x7][6x7][7x7][8x7][9x7]
[0x8][1x8][2x8][3x8][4x8][5x8][6x8][7x8][8x8][9x8]
[0x9][1x9][2x9][3x9][4x9][5x9][6x9][7x9][8x9][9x9]
```
