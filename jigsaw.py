import numpy
from PIL import Image, ImageDraw
from random import getrandbits


class Jigsaw(object):
    def __init__(self, image, output, piece_count):
        self.image = Image.open(image)
        self.image_width, self.image_height = self.image.size
        self.piece_width = int(self.image_width / piece_count)
        self.piece_height = int(self.image_height / piece_count)
        self.output = output
        self.piece_count = piece_count
        self.margin = (self.piece_width + self.piece_height) / 2 / 5
        self.rows = []

        for y in range(self.piece_count):
            row = []
            for x in range(self.piece_count):
                left = x * self.piece_width
                up = y * self.piece_height
                right = left + self.piece_width
                bottom = up + self.piece_height
                box = (left, up, right, bottom)
                piece = self.image.crop(box)

                new_width, new_height = map(lambda x: x + self.margin * 2,
                                            piece.size)

                new_im = Image.new('RGBA', (new_width, new_height))
                portions = (self.margin,
                            self.margin,
                            self.piece_width + self.margin,
                            self.piece_height + self.margin)

                transparent_area = (0, 0, new_width, new_height)
                draw = ImageDraw.Draw(new_im)
                draw.rectangle(transparent_area, fill=0)

                new_im.paste(piece, portions)
                row.append(Piece(new_im, x, y, self))
            self.append(row)
        for row in self.rows:
            for piece in row:
                piece.create_connections()
        self.save()

    def __repr__(self):
        text = ""
        for row in self.rows:
            for piece in row:
                text += '[%s]' % piece
            text += '\n'
        return text

    def save(self):
        for row in self.rows:
            for piece in row:
                piece.save(self.output)

    def get(self, x, y):
        return self.rows[y][x]

    def append(self, row):
        self.rows.append(row)

    def get_pieces(self):
        rows = []
        for row in self.rows:
            columns = []
            for piece in row:
                columns.append({'x': piece.x, 'y': piece.y})
            rows.append(columns)
        return rows


class Piece(object):
    def __init__(self, image, x, y, jigsaw):
        self.image = image
        self.w, self.h = self.image.size
        self.x = x
        self.y = y
        self.jigsaw = jigsaw

    def __repr__(self):
        return '%sx%s' % (self.x, self.y)

    @property
    def filename(self):
        return '%sx%s.png' % (self.x, self.y)

    def save(self, output):
        self.image.save('%s/%s' % (output, self.filename))

    def left(self):
        if self.x == 0:
            return False
        return self.jigsaw.get(self.x - 1, self.y)

    def up(self):
        if self.y == 0:
            return False
        return self.jigsaw.get(self.x, self.y - 1)

    def right(self):
        if self.x == self.jigsaw.piece_count - 1:
            return False
        return self.jigsaw.get(self.x + 1, self.y)

    def down(self):
        if self.y == self.jigsaw.piece_count - 1:
            return False
        return self.jigsaw.get(self.x, self.y + 1)

    def copy(self, polygon, x=0, y=0):
        polygon, box, coords = self._calculate_polygon(polygon, x, y)
        im_array = numpy.asarray(self.image)
        mask_im = Image.new('L', (im_array.shape[1], im_array.shape[0]), 0)
        drw = ImageDraw.Draw(mask_im)
        drw.polygon(polygon, outline=1, fill=1)
        mask = numpy.array(mask_im)

        new_im_array = numpy.empty(im_array.shape, dtype='uint8')

        new_im_array[:, :, :3] = im_array[:, :, :3]

        new_im_array[:, :, 3] = mask * 255

        piece = Image.fromarray(new_im_array, 'RGBA')
        piece = piece.crop(box)
        return piece

    def cut(self, polygon, x=0, y=0):
        polygon, box, coords = self._calculate_polygon(polygon, x, y)
        piece = self.copy(polygon)
        drw = ImageDraw.Draw(self.image)
        drw.polygon(polygon, fill=(255, 255, 255, 0))
        return piece

    def paste(self, piece, polygon, x=0, y=0):
        polygon, box, coords = self._calculate_polygon(polygon, x, y)
        self.image.paste(piece, box)

    def draw_merge_piece(self, polygon, other, x=0, y=0, other_x=0, other_y=0):
        merge_piece = self.cut(polygon, x, y)
        if other:
            other.paste(merge_piece, polygon, other_x, other_y)

    def create_connections(self):
        w, h = self.image.size
        m = self.jigsaw.margin
        hw = w/2
        hh = h/2
        polygon = [(0, 0), (m, 0), (m, m), (0, m)]

        other = self.left()
        if other:
            if bool(getrandbits(1)):
                self.draw_merge_piece(polygon, other, x=m, y=hh-m/2,
                                      other_x=w-m, other_y=hh-m/2)
            else:
                other.draw_merge_piece(polygon, self, x=w-m*2, y=hh-m/2,
                                       other_x=0, other_y=hh-m/2)

        other = self.up()
        if other:
            if bool(getrandbits(1)):
                self.draw_merge_piece(polygon, other, x=hw-m/2, y=m,
                                      other_x=hw-m/2, other_y=h-m)
            else:
                other.draw_merge_piece(polygon, self, x=hw-m/2, y=h-m*2,
                                       other_x=hw-m/2, other_y=0)

    def _calculate_polygon(self, polygon, x=0, y=0):
        polygon = [(i[0] + x, i[1] + y) for i in polygon]
        box = (min([i[0] for i in polygon]),
               min([i[1] for i in polygon]),
               max([i[0] for i in polygon]),
               max([i[1] for i in polygon]))
        coords = (box[0], box[1])
        return polygon, box, coords


if __name__ == '__main__':
    import sys
    import shutil
    import os
    import webbrowser
    image = sys.argv[1]
    output = sys.argv[2]
    piece_count = sys.argv[3]
    if os.path.exists(output):
        shutil.rmtree(output)
    os.mkdir(output)
    Jigsaw(image, output, int(piece_count))
    with open('template.html', 'r') as f:
        template = f.read()
        template = template.replace('{{ piece_count }}', piece_count)
    with open('index.html', 'w') as f:
        f.write(template)
    index_html_path = 'file://' + os.path.join(os.getcwd(), 'index.html')
    webbrowser.open(index_html_path, 2)
