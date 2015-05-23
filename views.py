from flask import Flask, render_template, request, url_for
from psf_form import PSFForm
import psf
from PIL import Image
import numpy as np
from math import asin,sin,cos
from scipy.ndimage.interpolation import zoom
app = Flask(__name__)


def samples(wavelen,num_aperture,refr_index,mf=1):
    alpha = arcsin(num_aperture/refr_index)
    nyx = wavelen/(4*mf)/refr_index/sin(alpha)
    nyz = wavelen/(2*mf)/refr_index/(1 - cos(alpha))
    return (nyx,nyz)
    
def calculate_nyquist(microscope,ex_wavelen,em_wavelen,num_aperture,refr_index):
    
    if ('confocal' in microscope) or ('twophoton' in microscope):
        return samples(ex_wavelen,num_aperture,refr_index,mf=2)
    if 'widefield' in microscope:
        return samples(em_wavelen,num_aperture,refr_index)
        
def save_psf(data):
    arr = psf.mirror_symmetry(np.log10(data))
    arr[np.isneginf(arr)] = 0.0
    arr[np.where(arr < -2.5)] = 0.0
    arr = arr + abs(np.amin(arr))
    disp_min = np.amin(arr)
    disp_max = np.amax(arr)
    newarr = (arr * (255 / (disp_max - disp_min))).astype(np.uint8)
    newarr[np.where(newarr == 255)] = 0
    newarr[31,31] = 255
    im = Image.fromarray(newarr)
    im = im.convert("RGB")
    im.save("static/images/psf.png")
        
def calculate_psf(model,scope,ex_wavelen,em_wavelen,num_aperture,refr_index):
    args = dict(shape=(32,32), dims=(4,4), ex_wavelen=ex_wavelen, em_wavelen=em_wavelen,
             num_aperture=num_aperture, refr_index=refr_index,
             pinhole_radius=0.50, pinhole_shape='round')
    return psf.PSF(model | scope, **args)        
    
@app.route('/psf',methods=['GET','POST'])
def get_psf():
    form = PSFForm()
    if request.method == 'POST' and form.validate_on_submit():
        calc_model = form.model.data
        if 'gaussian' in calc_model:
            model = psf.GAUSSIAN
        if 'isotropic' in calc_model:
            model = psf.ISOTROPIC
            
        microscope = form.microscope.data
        if 'confocal' in microscope:
            scope = psf.CONFOCAL
        if 'widefield' in microscope:
            scope = psf.WIDEFIELD
        if 'twophoton' in microscope:
            scope = psf.TWOPHOTON
            
        ex_wavelen = float(form.ex_wavelen.data)
        em_wavelen = float(form.em_wavelen.data)
        num_aperture = float(form.num_aperture.data)
        refr_index = float(form.refr_index.data)
        
        obsvol = calculate_psf(model,scope,ex_wavelen,em_wavelen,num_aperture,refr_index)
        save_psf(obsvol.data)

        if 'gaussian' in calc_model:
            sigma = obsvol.sigma.um
        else:
            sigma = ['N/A','N/A']
        nyquist = calculate_nyquist(microscope,ex_wavelen,em_wavelen,num_aperture,refr_index)
    else:
        sigma = None
        microscope = None
        nyquist = None
    return render_template('psf.html',form=form,sigma=sigma,microscope=microscope,nyquist=nyquist)

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 's3cr3t'
    app.run()