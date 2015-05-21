from flask.ext.wtf import Form
from wtforms import TextField, SelectField, validators

class PSFForm(Form):
    ex_wavelen = TextField('Excitation wavelength:', [validators.Required()])
    em_wavelen = TextField('Emission wavelength:', [validators.Required()])
    num_aperture = TextField('Numerical aperture:', [validators.Required()])
    refr_index = TextField('Refractive index:', [validators.Required()])
    microscope = SelectField('Microscope:',[validators.Required()],\
                             choices=[('confocal','Confocal'),\
                                      ('widefield','Widefield'),\
                                      ('twophoton','Two photon')])