import numpy as np

def spherical_functions_trigon(theta, lmax):
  ct = np.cos(np.ravel(theta))
  st = np.sin(np.ravel(theta))

  plm = np.zeros((lmax+1, lmax+1, ct.shape[0])) * np.nan
  pilm = np.zeros(plm.shape) * np.nan
  taulm = np.zeros(plm.shape) * np.nan
  pprimel0 = np.zeros((lmax+1, ct.shape[0])) * np.nan

  plm[0,0,:] = np.sqrt(1/2) * np.ones_like(ct)
  plm[1,0,:] = np.sqrt(3/2) * ct

  pilm[0,0,:] = np.zeros_like(ct)
  pilm[1,0,:] = np.zeros_like(ct)

  pprimel0[0,:] = np.zeros_like(ct)
  pprimel0[1,:] = np.sqrt(3) * plm[0,0,:]

  taulm[0,0,:] = -st * pprimel0[0,:]
  taulm[1,0,:] = -st * pprimel0[1,:]
  
  for l in range(1, lmax):
    plm[l+1,0,:] = 1/(l+1) * np.sqrt((2*l + 1) * (2*l + 3)) * ct * plm[l,0,:] - l/(l+1) * np.sqrt((2*l + 3) / (2*l - 1)) * plm[l-1,0,:]
    pilm[l+1,0,:] = np.zeros_like(ct)
    pprimel0[l+1,:] = np.sqrt((2*l + 3)/(2*l + 1)) * ((l+1) * plm[l,0,:] + ct * pprimel0[l,:])
    taulm[l+1,0,:] = -st * pprimel0[l+1,:]

  for m in range(1,lmax+1):
    plm[m-1,m,:] = np.zeros_like(ct)
    pilm[m-1,m,:] = np.zeros_like(ct)
    coeff = np.sqrt((2*m + 1) / 2 / np.math.factorial(2*m)) * np.prod(np.arange(1, 2*m, 2))
    plm[m,m,:] = coeff * np.power(st, m)
    pilm[m,m,:] = coeff * np.power(st, m-1)
    taulm[m,m,:] = m * ct * pilm[m,m,:]
    for l in range(m,lmax):
      coeff1 = np.sqrt((2*l + 1) * (2*l + 3) / (l + 1 - m) / (l + 1 + m)) * ct
      coeff2 = np.sqrt((2*l + 3) * (l - m) * (l + m) / (2*l - 1) / (l + 1 - m) / (l + 1 + m))
      plm[l+1,m,:] = coeff1 * plm[l,m,:] - coeff2 * plm[l-1,m,:]
      pilm[l+1,m,:] = coeff1 * pilm[l,m,:] - coeff2 * pilm[l-1,m,:]
      taulm[l+1,m,:] = (l + 1) * ct * pilm[l+1,m,:] - (l + 1 + m) * np.sqrt((2 * l + 3) * (l + 1 -m) / (2 * l + 1) / (l + 1 + m)) * pilm[l,m,:]
  
  pilm  = np.reshape(pilm,  np.concatenate(([lmax+1, lmax+1], theta.shape)))
  taulm = np.reshape(taulm, np.concatenate(([lmax+1, lmax+1], theta.shape)))
  return pilm, taulm