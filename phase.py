from PIL import Image
import numpy as np

def randomise (img, noise='uniform', noise_prop=1):
    """Randomise the phase of an image.
    
     Keyword arguments:
    img -- a PIL image
    noise -- the type of distribution to draw the noise from. Can be one of:
        'uniform': uniform distribution, between -pi and pi
        'permute': randomly shuffle the image's existing phase
        'normal': normal distribution, with mean of 0, and sd of 1
    noise_prop -- a float from 0 to 1 specifying how much of the image should be noise (e.g. 0.3 will produce an image with phase of 30% noise, 70% original)
    """
    
    # fast fourier transform of the image as-is
    img_fft = np.fft.fftn(img)
    # get amplitude as distance from origin in complex plane
    amp = np.abs(img_fft)
    # get original image's phase
    ph = np.angle(img_fft)
    # get randomised phas
    if noise == 'uniform':
        ph_noise = np.random.uniform(-np.pi, np.pi, img_fft.shape)
    elif noise == 'permute':
        ph_noise = np.random.permutation(ph)
    elif noise == 'normal':
        ph_noise = np.random.normal(0, 1, img_fft.shape)
    
    # get new phase
    ph_new = ph * (1-noise_prop) + ph_noise * noise_prop
    
    # inverse fourier transform using the new phases
    # (absolute result is rounded to nearest integer)
    img_ph_rand = np.round(np.abs( np.fft.ifftn(amp * np.exp(1j * ph_new)) ))
    
    img_out = Image.fromarray(np.uint8(img_ph_rand))
    
    return(img_out)
    