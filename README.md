# randphase
Python functions for generating phase-randomised images of text. Fourier transform is used to extract amplitude. Inverse Fourier transform is used to generate an image with the same amplitude spectrum but with phase generated from normally or uniformly distributed noise.

## Summary

The `draw.text()` function makes it easy to create an image of text.

```python
import draw
raw = draw.text('erudition', size=50, crop_to='text')
raw.show()
```

![](img/small_img1.png)

To randomise the phase of an image with normally distributed noise, use `phase.randomise()`

```python
import phase
rp = phase.randomise(text_img, noise='normal')
rp.show()
```

![](img/small_img1_ph.png)

## Notes

* `draw.text()` also accepts different fonts and colours
* `phase.randomise()` accepts any PIL image, and can work with colour or greyscale images

![](img/examples.png)
