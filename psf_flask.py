from flask import Flask, render_template, request, url_for
from psf_form import PSFForm
import psf
from PIL import Image
import numpy as np
app = Flask(__name__)
    
@app.route('/calculate_psf',methods=['GET','POST'])
def calculate_psf():
    form = PSFForm()
    if request.method == 'POST' and form.validate_on_submit():
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
        args = dict(shape=(32,32), dims=(4,4), ex_wavelen=ex_wavelen, em_wavelen=em_wavelen,
                 num_aperture=num_aperture, refr_index=refr_index,
                 pinhole_radius=0.50, pinhole_shape='round')
        obsvol = psf.PSF(psf.GAUSSIAN | scope, **args)
        im = Image.fromarray(np.log10(obsvol.data))
        im = im.convert('RGBA')
        im.save('psf.jpg')
        sigma = obsvol.sigma.um
        scope = scope
    else:
        sigma = None
        microscope = None
    return render_template('psf.html',form=form,sigma=sigma,microscope=microscope)

if __name__ == '__main__':
    app.debug = True
    app.secret_key = 's3cr3t'
    app.run()