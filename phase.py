from PIL import Image
import numpy as np

def randomise (img, noise='normal', loc=0, scale=1):
    """Randomise the phase of an image.
    
     Keyword arguments:
    img -- a PIL image
    noise -- the type of distribution to draw the noise from. Can be one of:
        'normal': normal distribution, with mean of 0, and sd of 1
        'uniform': uniform distribution, between -1 and 1
    """
    
    # fast fourier transform of the image as-is
    img_fft = np.fft.fftn(img)
    # get amplitude as distance from origin in complex plane
    amp = np.abs(img_fft)
    # get randomised phase    
    if noise == 'normal':
        ph_noise = np.random.normal(0, 1, img_fft.shape)
    elif noise == 'uniform':
        ph_noise = np.random.uniform(-1, 1, img_fft.shape)
    
    rand_ph = np.angle(np.fft.fftn(ph_noise))
    
    # inverse fourier transform using the new phases
    # (absolute result is rounded to nearest integer)
    img_ph_rand = np.round(np.abs( np.fft.ifftn(amp * np.exp(1j * rand_ph)) ))
    
    img_out = Image.fromarray(np.uint8(img_ph_rand))
    
    return(img_out)
    