from PIL import Image, ImageDraw, ImageFont
import numpy as np
from string import ascii_letters

def text (text,  font='arial.ttf', size=32, colour=(255,255,255), bg=(127,127,127), border=(0,0,0,0), crop_x='text', crop_y='text', crop_chars=ascii_letters, fontcrop_n=None, align_x='centre', greyscale=False):
    """Return a PIL image of the specified text, cropped to its boundaries.
    
     Keyword arguments:
    text -- the text to display (str).
    font -- the .ttf font file to use (str)
    size -- the font size (int; see PIL docs)
    colour -- a tuple specifying the font colour in hex, in the form (R,G,B)
    bg -- a tuple specifying the background colour in hex, in the form (R,G,B)
    border -- a tuple of pixel sizes for a border in the form (left_x, right_x, top_y, bottom_y), surrounding the crop
    crop_x -- should be one of the following, specifiying whether the output's width be cropped to the maximum boundaries of the current text or the font:
        'text': the width limits of the rendered text
        'font': the width limits of the font's ascii characters given the text's length, with centred alignment
    crop_y -- should be one of the following, specifiying whether the output's height be cropped to the maximum boundaries of the current text or the font:
        'text': the height limits of the rendered text
        'font': the height limits of the font's ascii characters given the text's length
    crop_chars -- a list of characters that should be used to find the font extremities when cropping. Default is string.ascii_letters
    fontcrop_n -- if crop_x or crop_y are 'font', how many characters should the crop assume are available to the font? If None (default) will use len(text).
    align_x -- how to horizontally align the text (if any white space):
        'left': align to the left
        'centre': align to the centre
        'right': align to the right
    greyscale -- should the resulting image be converted to greyscale?
    """
    
    # get font info
    pil_font = ImageFont.truetype(font, size=size, encoding="unic")
    pil_fontsize = pil_font.getsize(text)
    
    # draw image
    im = Image.new('RGB', pil_fontsize, bg)
    im_draw = ImageDraw.Draw(im)
    im_draw.text((0,0), text, font=pil_font, fill=colour)
    
    # find which pixels could be filled by text
    if crop_x=='font' or crop_y=='font':
        if fontcrop_n is None:
            crop_nchar = len(text)
        else:
            crop_nchar = fontcrop_n
        letter_fontsizes = [pil_font.getsize(letter*crop_nchar) for letter in crop_chars]
        canvas_max_size = (max([tup[0] for tup in letter_fontsizes]), max([tup[1] for tup in letter_fontsizes]))
        im_lims = Image.new('RGB', canvas_max_size, bg)
        im_lims_draw = ImageDraw.Draw(im_lims)
        for letter in crop_chars:
            im_lims_draw.text((0,0), letter*crop_nchar, font=pil_font, fill=colour)
        im_lims_arr = np.array(im_lims)
        text_lims_px = np.where(np.sum(im_lims_arr==bg, 2)!=im_lims_arr.shape[2])
        
    # find which pixels are filled with text
    im_arr = np.array(im)
    text_px = np.where(np.sum(im_arr==bg, 2)!=im_arr.shape[2])  # find non-background pixels   
    
    # get x crop from either font or text limits
    if crop_x=='font':
        min_x = np.min(text_lims_px[1])
        max_x = np.max(text_lims_px[1])+1
    elif crop_x=='text':
        min_x = np.min(text_px[1])
        max_x = np.max(text_px[1])+1
    
    # get y crop from either font or text limits
    if crop_y=='font':
        min_y = np.min(text_lims_px[0])
        max_y = np.max(text_lims_px[0])+1
    elif crop_y=='text':
        min_y = np.min(text_px[0])
        max_y = np.max(text_px[0])+1
    
    min_x = int(min_x)
    max_x = int(max_x)
    min_y = int(min_y)
    max_y = int(max_y)
    
    # get the horizontal and vertical text size info (for alignment & drawing location)
    min_x_text = np.min(text_px[1])
    max_x_text = np.max(text_px[1])+1
    min_y_text = np.min(text_px[0])
    max_y_text = np.max(text_px[0])+1
    text_width = max_x_text - min_x_text
    
    # apply crop (create as new image to avoid default black background)
    im_out = Image.new('RGB', (border[0] + border[1] + max_x - min_x, border[2] + border[3] + max_y - min_y), bg)
    im_out_draw = ImageDraw.Draw(im_out)
    
    # get the text position adjustment (dictated by alignment)
    if align_x=='centre':
        align_adjust = round((max_x - min_x) * 0.5 - text_width * 0.5)
    elif align_x=='left':
        align_adjust = 0
    elif align_x=='right':
        align_adjust = max_x - text_width
    
    # draw the text in the necessary position
    im_out_draw.text((-min_x_text + border[0] + align_adjust, -min_y + border[2]), text, font=pil_font, fill=colour)
    
    # convert to greyscale if necessary
    if greyscale:
        im_out=im_out.convert('L')
    
    return(im_out)