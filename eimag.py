from math import pi, e

def e_imaginary_degrees(degrees: float):
    """Raises e^(degrees*i).
    Note that in Python, the math number i is called j."""
    return e**(degrees*1j)

def round_e_imaginary_degrees(degrees: float, precision: int = 10):
    return round(e_imaginary_degrees(degrees).imag, precision)

def round_e_real_degrees(degrees: float, precision: int = 10):
    return round(e_imaginary_degrees(degrees).real, precision)

if __name__ == '__main__':
    _ri = round_e_imaginary_degrees(2*pi)
    _rr = round_e_real_degrees(2*pi)
    _nii = round_e_imaginary_degrees(3/2*pi)
    _nir = round_e_real_degrees(3/2*pi)
    _r_not_rounded = e_imaginary_degrees(2*pi)
    _ni_not_rounded = e_imaginary_degrees(3/2*pi)
    print("e^2pi without rounding:", _r_not_rounded.real, '+', str(_r_not_rounded.imag)+'i',
        "Real right" if _r_not_rounded.real == 1 else "Real WRONG",
        "Imaginary right" if _r_not_rounded.imag == 0 else "Imaginary WRONG")
    print("e^((3/2)pi) without rounding:", _ni_not_rounded.real, '+', str(_ni_not_rounded.imag)+'i',
        "Real right" if _ni_not_rounded.real == 0 else "Real WRONG",
        "Imaginary right" if _ni_not_rounded.imag == -1 else "Imaginary WRONG")
    assert _ri == 0
    assert _rr == 1
    assert _nii == -1
    assert _nir == 0
    print("e^2pi after rounding: ", _rr, " + ", _ri, "i", sep="")
    print("e^((3/2)pi) after rounding: ", _nir, " + ", _nii, "i", sep="")
    print("After rounding it works better.")
