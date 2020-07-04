from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os.path as op

import draw
import phase

# simple examples
im = draw.text('erudition', size=50, font='courbd.ttf')
im.save(op.join('img', 'im.png'))
rp_im = phase.randomise(im, noise='uniform')
rp_im.save(op.join('img', 'rp_im.png'))
pp_im = phase.randomise(im, noise='uniform')
pp_im.save(op.join('img', 'pp_im.png'))

# simple examples with contrast adjustment
rp_im_adj = phase.randomise(im, noise='uniform', contrast_adj=0.5)
rp_im_adj.save(op.join('img', 'rp_im_adj.png'))
pp_im_adj = phase.randomise(im, noise='uniform', contrast_adj=0.5)
pp_im_adj.save(op.join('img', 'pp_im_adj.png'))

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

# show noise_prop effect
u_010 = phase.randomise(im, noise_prop=0.1, contrast_adj=0.5)
u_025 = phase.randomise(im, noise_prop=0.25, contrast_adj=0.5)
u_050 = phase.randomise(im, noise_prop=0.50, contrast_adj=0.5)
u_075 = phase.randomise(im, noise_prop=0.75, contrast_adj=0.5)
u_100 = phase.randomise(im, noise_prop=1, contrast_adj=0.5)
u_010.save(op.join('img', 'u_010.png'))
u_025.save(op.join('img', 'u_025.png'))
u_050.save(op.join('img', 'u_050.png'))
u_075.save(op.join('img', 'u_075.png'))
u_100.save(op.join('img', 'u_100.png'))

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
text_img2 = draw.text('Arial', bg=(0,0,0), colour=(127,127,0), size=100)
luke_grey = luke.convert('LA')

imgs = [text_img1, text_img2, luke, luke_grey]
plt_labs = ['Raw Image',
            '25%  Phase-Randomised\nwith Uniform Noise',
            '50% Phase-Randomised\nwith Uniform Noise',
            '100% Phase-Randomised\nwith Uniform Noise',
            '25% Phase-Permuted',
            '50% Phase-Permuted',
            '100% Phase-Permuted']
fig, axs = plt.subplots(len(plt_labs), len(imgs), figsize=(20, 18))

for im_nr, im in enumerate(imgs):
    axs[0, im_nr].imshow(im)
    axs[1, im_nr].imshow(phase.randomise(im, noise='uniform', noise_prop=0.25))
    axs[2, im_nr].imshow(phase.randomise(im, noise='uniform', noise_prop=0.5))
    axs[3, im_nr].imshow(phase.randomise(im, noise='uniform', noise_prop=1))
    axs[4, im_nr].imshow(phase.randomise(im, noise='permute', noise_prop=0.25))
    axs[5, im_nr].imshow(phase.randomise(im, noise='permute', noise_prop=0.5))
    axs[6, im_nr].imshow(phase.randomise(im, noise='permute', noise_prop=1))

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
