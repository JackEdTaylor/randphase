from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os.path as op

import draw
import phase

# save smaller images
small_img1 = draw.text('erudition', size=50)
small_img1.save(op.join('img', 'small_img1.png'))
small_img1_ph = phase.randomise(small_img1, noise='normal')
small_img1_ph.save(op.join('img', 'small_img1_ph.png'))

# plot large figure
text_img1 = draw.text('Arial', size=100)
text_img2 = draw.text('Arial', bg=(0,0,0), colour=(255,255,255), size=100)
luke = Image.open(op.join('img', 'luke.png'))
luke_grey = luke.convert('LA')

imgs = [text_img1, text_img2, luke, luke_grey]
plt_labs = ['Raw Image',
            'Phase-Randomised\nwith Uniform Noise',
            'Phase-Randomised\nwith Gaussian Noise']
fig, axs = plt.subplots(len(plt_labs), len(imgs), figsize=(20, 5))

for im_nr, im in enumerate(imgs):
    axs[0, im_nr].imshow(im)
    axs[1, im_nr].imshow(phase.randomise(im, noise='uniform'))
    axs[2, im_nr].imshow(phase.randomise(im, noise='normal'))

for lab_nr, lab in enumerate(plt_labs):
    axs[lab_nr, 0].set_ylabel(lab, rotation=0, fontsize=25, labelpad=200, verticalalignment='center')

for plt_y in range(len(imgs)):
    for plt_x in range(len(plt_labs)):
        axs[plt_x, plt_y].tick_params(which='both',
                                      bottom=False, top=False, left=False, right=False,
                                      labelbottom=False, labeltop=False, labelleft=False, labelright=False)
        axs[plt_x, plt_y].set_aspect('equal')

plt.subplots_adjust(left=0.275, top = 0.99, bottom = 0, right = 0.99, wspace=0.1, hspace=0.25)

fig.savefig(fname=op.join('img', 'examples.png'), dpi=100)
