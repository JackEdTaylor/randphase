from PIL import Image, ImageEnhance
import numpy as np

def randomise (img, noise='uniform', noise_prop=1, contrast_adj=1):
    """Randomise the phase of an image.
    
     Keyword arguments:
    img -- a PIL image
    noise -- the type of distribution to draw the noise from. Can be one of:
        'uniform': uniform distribution, between -pi and pi
        'permute': randomly shuffle the image's existing phase
        'normal': normal distribution, with mean of 0, and sd of 1
    noise_prop -- a float from 0 to 1 specifying how much of the image should be noise (e.g. 0.3 will produce an image with phase of 30% noise, 70% original)
    contrast_adj -- a float specifying a proportion of contrast adjustment. The contrast of `img` will be adjusted to this value before the fft is run, and the phase-altered output will then be reverted to the original image's contrast. Contrast artefacts can often be removed from phase-altered images by reducing this value from 1.
    """
    
    # adjust contrast
    if contrast_adj!=1:
        img_ie = ImageEnhance.Contrast(img)
        img = img_ie.enhance(contrast_adj)
    
    # fast fourier transform of the image as-is
    img_fft = np.fft.fftn(img)
    # get amplitude as distance from origin in complex plane
    amp = np.abs(img_fft)
    # get original image's phase
    ph = np.angle(img_fft)
    # get randomised phase values
    if noise == 'uniform':
        ph_noise = np.random.uniform(-np.pi, np.pi, img_fft.shape)
    elif noise == 'permute':
        ph_noise = np.random.permutation(ph)
    elif noise == 'normal':
        ph_noise = np.random.normal(0, 1, img_fft.shape)
    
    # get phase values with the desired proportion of noise
    ph_new = ph * (1-noise_prop) + ph_noise * noise_prop
    
    # inverse fourier transform using the new phases
    # (rounded to nearest integer to account for rounding errors)
    img_ph_rand = np.round(np.abs( np.fft.ifftn(amp * np.exp(1j * ph_new)) ))
    
    # convert to PIL image
    img_out = Image.fromarray(np.uint8(img_ph_rand))
    
    # revert contrast to original value
    if contrast_adj!=1:
        img_out_ie = ImageEnhance.Contrast(img_out)
        img_out = img_out_ie.enhance(1/contrast_adj)
    
    return(img_out)
    
