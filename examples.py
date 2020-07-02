from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os.path as op

import draw
import phase

# save smaller images
text_im = draw.text('erudition', size=50)
text_im.save(op.join('img', 'text_im.png'))
rp_im = phase.randomise(text_im, noise='normal')
rp_im.save(op.join('img', 'rp_im.png'))

# compare cropping
crop1 = draw.text('brine', size=50, crop_x = 'font', crop_y='font')
crop1.save(op.join('img', 'crop1.png'))
crop2 = draw.text('bring', size=50, crop_x = 'font', crop_y='font')
crop2.save(op.join('img', 'crop2.png'))
crop3 = draw.text('WWWWW', size=50, crop_x = 'font', crop_y='font')
crop3.save(op.join('img', 'crop3.png'))

# compare alignment
align_a = draw.text('brine', size=50, crop_x='font', align_x='centre')
align_b = draw.text('brine', size=50, crop_x='font', align_x='left')
align_c = draw.text('brine', size=50, crop_x='font', align_x='right')

# show other text options
text_spec = draw.text('fancy', font='BRUSHSCI.TTF', colour=(255,127,0), bg=(100,0,100),
                      border=(0,0,10,10), size=75, crop_x='font', align_x='centre')
text_spec.save(op.join('img', 'text_spec.png'))

# luke examples
luke = Image.open(op.join('img', 'luke.png')).convert('RGB')
luke_rp = phase.randomise(luke)
luke_rp.save(op.join('img', 'luke_rp.png'))

# plot large figure
text_img1 = draw.text('Arial', size=100)
text_img2 = draw.text('Arial', bg=(0,0,0), colour=(255,255,255), size=100)
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
