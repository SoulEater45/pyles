from scipy.special import spherical_jn, spherical_yn

def T_entry(tau, l, kM, kS, R, field_type = 'scattered'):
  m  = kS / kM
  x  = kM * R
  mx = kS * R

  jx  = spherical_jn(l, x)
  jmx = spherical_jn(l, mx)
  hx  = spherical_jn(l, x) + 1j * spherical_yn(l, x)

  # djx  = spherical_jn(l, x, derivative=True)
  # djmx = spherical_jn(l, mx, derivative=True)
  # dhx  = spherical_jn(l, x, derivative=True) + 1j * spherical_yn(l, x, derivative=True)
  djx  = x *  spherical_jn(l-1, x)  - l * jx
  djmx = mx * spherical_jn(l-1, mx) - l * jmx
  dhx  = x * (spherical_jn(l-1, x) + 1j * spherical_yn(l-1, x)) - l * hx

  match (field_type, tau):
    case ('scattered', 1):
      return -(jmx * djx - jx * djmx) / (jmx * dhx - hx * djmx) # -b
    case ('scattered', 2):
      return -(m**2 * jmx * djx - jx * djmx) / (m**2 * jmx * dhx - hx * djmx) # -a
    case ('internal', 1):
      return (jx * dhx - hx * djx) / (jmx * dhx - hx * djmx); # c
    case ('internal', 2):
      return (m * jx * dhx - m * hx * djx) / (m**2 * jmx * dhx - hx * djmx); # d
    case _:
      print('Not a valid field type provided. Returning None!')
      return None