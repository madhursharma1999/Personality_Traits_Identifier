path='img/e.jpg'

thresh_hold = 197
dx=130
dy=2

from ratio_of_left_margin_and_width import *
LeftMargin(path,dx,dy,thresh_hold)
print()

from ratio_of_right_margin_and_width import *
RightMargin(path,dx,dy,thresh_hold)
print()

from ratio_of_top_margin_and_height import *
TopMargin(path,dx,dy,thresh_hold)
print()

from constant_or_irregular_margins import *
MarginVariance(path,dx,dy,thresh_hold)
print()

dxw=20
dyw=5

from constant_or_irregular_spacing import *
spacing(path,dx,dy,dxw,dyw,thresh_hold)
print()



