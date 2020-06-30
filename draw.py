from PIL import Image, ImageDraw, ImageFont
import numpy as np

def text (text,  font='arial.ttf', size=32, colour=(255,255,255), bg=(127,127,127), border=(0,0,0,0), crop_to='text'):
    """Return a PIL image of the specified text, cropped to its boundaries.
    
     Keyword arguments:
    text -- the text to display (str).
    font -- the .ttf font file to use (str)
    size -- the font size (int; see PIL docs)
    colour -- a tuple specifying the font colour in hex, in the form (R,G,B)
    bg -- a tuple specifying the background colour in hex, in the form (R,G,B)
    border -- a tuple of pixel sizes for a border in the form (left_x, right_x, top_y, bottom_y)
    crop_to -- should be 'text' or 'font', specifiying whether the output be cropped to the boundary of the text or the font
    """
    
    # get font info
    pil_font = ImageFont.truetype(font, size=size, encoding="unic")
    pil_fontsize = list(pil_font.getsize(text))
    
    pil_fontsize[0] += border[0] + border[1]
    pil_fontsize[1] += border[2] + border[3]
    
    # draw image
    im = Image.new('RGB', pil_fontsize, bg)
    im_draw = ImageDraw.Draw(im)
    im_draw.text((border[0], border[2]), text, font=pil_font, fill=colour)
    
    if crop_to=='text':
        im_arr = np.array(im)
        text_px = np.where(np.sum(im_arr==bg, 2)!=im_arr.shape[2])  # find non-background pixels
        min_x = np.min(text_px[1]) - border[0]
        min_y = np.min(text_px[0]) - border[2]
        max_x = np.max(text_px[1])+1 + border[1]
        max_y = np.max(text_px[0])+1 + border[3]
        im_cropped = im.crop((min_x, min_y, max_x, max_y))
    
    elif crop_to=='font':
        im_cropped = im
    
    return(im_cropped)
    