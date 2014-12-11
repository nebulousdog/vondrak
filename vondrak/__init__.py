# -*- coding: utf-8 -*-
from numpy import array, sin, cos, sqrt, append

# 2Pi
tau =  6.283185307179586476925287e0

# Arcseconds to radians
as2r = 4.848136811095359935899141e-6

# Obliquity at J2000.0 (radians)
eps0 = 84381.406 * as2r

def ltp_PECL(epj):
    '''Long-term precession of the ecliptic'''

    # There is a typographical error in the original coefficient
    # C₇ for Qₐ should read 198.296701 instead of 198.296071
    # Src: http://www.aanda.org/articles/aa/abs/2012/05/aa17274e-11/aa17274e-11.html

    # Number of polynomial and periodic coefficients
    npol = 4
    nper = 8

    # Polynomial coefficients
    pqpol = array([
        [+5851.607687,-1600.886300],
        [-0.1189000,+1.1689818],
        [-0.00028913,-0.00000020],
        [+0.000000101,-0.000000437],
    ])

    # Periodic coefficients
    pqper = array([
        [708.15, -5486.751211, -684.661560, 667.666730, -5523.863691],
        [2309.00, -17.127623, 2446.283880, -2354.886252, -549.747450],
        [1620.00, -617.517403, 399.671049, -428.152441, -310.998056],
        [492.20, 413.442940, -356.652376, 376.202861, 421.535876],
        [1183.00, 78.614193, -186.387003, 184.778874, -36.776172],
        [622.00, -180.732815, -316.800070, 335.321713, -145.278396],
        [882.00, -87.676083, 198.296701, -185.138669, -34.744450], # corrected coefficient per erratum
        [547.00, 46.140315, 101.135679, -120.972830, 22.885731],
    ])

    # Centuries since J2000
    T = (epj-2000.0)/100.0

    # Initialize Pₐ and Qₐ accumulators
    P = 0.0
    Q = 0.0

    # Periodic Terms
    for i in range(0,nper):
        W = tau*T
        A = W/pqper[i][0]
        S = sin(A)
        C = cos(A)
        P = P + C*pqper[i][1] + S*pqper[i][3]
        Q = Q + C*pqper[i][2] + S*pqper[i][4]

    # Polynomial Terms
    W = 1.0
    for i in range(0,npol):
        P = P + pqpol[i][0]*W
        Q = Q + pqpol[i][1]*W
        W = W*T

    # Pₐ and Qₐ (radians)
    P = P*as2r
    Q = Q*as2r

    # Form the ecliptic pole vector
    Z = sqrt(max(1.0-P*P-Q*Q,0.0))
    S = sin(eps0)
    C = cos(eps0)
    vec0 = P
    vec1 = -Q*C - Z*S
    vec2 = -Q*S + Z*C
    vec = array([vec0,vec1,vec2])
    return vec

def ltp_PEQU(epj):
    '''Long-term precession of the equator'''

    # Number of polynomial and periodic coefficients
    npol = 4
    nper = 14

    # Polynomial coefficients
    xypol = array([
        [+5453.282155,-73750.930350],
        [+0.4252841,-0.7675452],
        [-0.00037173,-0.00018725],
        [-0.000000152,+0.000000231],
    ])

    # Periodic coefficients
    xyper = array([
        [256.75, -819.940624, 75004.344875, 81491.287984, 1558.515853],
        [708.15, -8444.676815, 624.033993, 787.163481, 7774.939698,],
        [274.20, 2600.009459, 1251.136893, 1251.296102, -2219.534038],
        [241.45, 2755.175630, -1102.212834, -1257.950837, -2523.969396],
        [2309.00, -167.659835, -2660.664980, -2966.799730, 247.850422],
        [492.20, 871.855056, 699.291817, 639.744522, -846.485643],
        [396.10, 44.769698, 153.167220, 131.600209, -1393.124055],
        [288.90, -512.313065, -950.865637, -445.040117, 368.526116],
        [231.10, -819.415595, 499.754645, 584.522874, 749.045012],
        [1610.00, -538.071099, -145.188210, -89.756563, 444.704518],
        [620.00, -189.793622, 558.116553, 524.429630, 235.934465],
        [157.87, -402.922932, -23.923029, -13.549067, 374.049623],
        [220.30, 179.516345, -165.405086, -210.157124, -171.330180],
        [1200.00, -9.814756, 9.344131, -44.919798, -22.899655],
    ])

    # Centuries since J2000
    T = (epj-2000.0)/100.0

    # Initialize Pₐ and Qₐ accumulators
    X = 0.0
    Y = 0.0

    # Periodic Terms
    for i in range(0,nper):
        W = tau*T
        A = W/xyper[i][0]
        S = sin(A)
        C = cos(A)
        X = X + C*xyper[i][1] + S*xyper[i][3]
        Y = Y + C*xyper[i][2] + S*xyper[i][4]

    # Polynomial Terms
    W = 1.0
    for i in range(0,npol):
        X = X + xypol[i][0]*W
        Y = Y + xypol[i][1]*W
        W = W*T

    # X and Y (direction cosines)
    X = X*as2r
    Y = Y*as2r

    # Form the equator pole vector
    veq0 = X
    veq1 = Y
    W = X*X + Y*Y
    veq2 = 0.0
    if(W < 1.0):
        veq2 = sqrt(1.0-W)
    veq = array([veq0, veq1, veq2])
    return veq

def pxp(a,b):
    '''p-vector outer (=vector=cross) product.
    Given: two p-vectors (a and b)
    Return: a x b
    '''

    xa = a[0]
    ya = a[1]
    za = a[2]
    xb = b[0]
    yb = b[1]
    zb = b[2]
    axb = array([])
    axb = append(axb,ya*zb - za*yb)
    axb = append(axb,za*xb - xa*zb)
    axb = append(axb,xa*yb - ya*xb)
    return axb

def pn(p):
    '''Convert a p-vector into modulus and unit vector.
    Given: p-vector (p)
    Return: modulus (r), and unit vector (u)
    '''

    # Modulus of p-vector
    # http://www.iausofa.org/2013_1202_C/sofa/pm.c
    w = sqrt(p[0]*p[0] + p[1]*p[1] + p[2]*p[2])
    u = array([])
    if(w == 0.0):
        # zero a p-vector
        # http://www.iausofa.org/2013_1202_C/sofa/zp.c
        u = append(u,[0.0, 0.0, 0.0])
    else:
        # unit vector
        # http://www.iausofa.org/2013_1202_C/sofa/sxp.c
        s = 1.0/w
        u = append(u, s*p[0])
        u = append(u, s*p[1])
        u = append(u, s*p[2])
    r = w
    return r, u

def ltp_PMAT(epj):
    '''Long-term precession matrix
    Given: EPJ d Julian epoch (TT)
    Return: RP d precession matrix, J2000.0 to date

    The matrix is in the sense P_date = RP x P_J2000,
    where P_J2000 is a vector with respect to the J2000.0 mean
    equator and equinox and P_date is the same vector with respect to
    the equator and equinox of epoch EPJ.
    '''

    # Equator pole (bottom row of matrix)
    peqr = ltp_PEQU(epj)

    # Ecliptic pole
    pecl = ltp_PECL(epj)

    # Equinox (top row of matrix)
    V = pxp(peqr, pecl) # P-vector outer product.
    w, EQX = pn(V) # Convert a p-vector into modulus and unit vector

    # Middle row of matrix
    V = pxp(peqr, EQX)

    # The matrix elements
    rp = array([])
    rp = append(rp, [EQX, V, peqr])
    rp = rp.reshape(3,3)
    return rp

def ltp_PBMAT(epj):
    '''Long-term precession matrix, including GCRS frame bias.
    Given: EPJ d Julian epoch (TT)
    Return: RPB d precession-bias matrix, J2000.0 to date

    The matrix is in the sense P_date = RPB x P_J2000,
    where P_J2000 is a vector in the Geocentric Celestial Reference
    System, and P_date is the vector with respect to the Celestial
    Intermediate Reference System at that date but with nutation
    neglected.

    A first order bias formulation is used, of sub-microarcsecond
    accuracy compared with a full 3D rotation.
    '''

    # Frame bias (IERS Conventions 2010, Eqs. 5.21 and 5.33)
    DX = -0.016617 * as2r
    DE = -0.0068192 * as2r
    DR = -0.0146 * as2r

    # Precession matrix.
    rp = ltp_PMAT(epj)

    # Apply the bias
    rpb = array([])
    rpb = append(rpb,  rp[0][0]    - rp[0][1]*DR + rp[0][2]*DX)
    rpb = append(rpb,  rp[0][0]*DR + rp[0][1]    + rp[0][2]*DE)
    rpb = append(rpb, -rp[0][0]*DX - rp[0][1]*DE + rp[0][2]   )
    rpb = append(rpb,  rp[1][0]    - rp[1][1]*DR + rp[1][2]*DX)
    rpb = append(rpb,  rp[1][0]*DR + rp[1][1]    + rp[1][2]*DE)
    rpb = append(rpb, -rp[1][0]*DX - rp[1][1]*DE + rp[1][2]   )
    rpb = append(rpb,  rp[2][0]    - rp[2][1]*DR + rp[2][2]*DX)
    rpb = append(rpb,  rp[2][0]*DR + rp[2][1]    + rp[2][2]*DE)
    rpb = append(rpb, -rp[2][0]*DX - rp[2][1]*DE + rp[2][2]   )
    rpb = rpb.reshape(3,3)
    return rpb

# def epj(dj):
#     '''Julian Date to Julian Epoch'''
#     # based on http://www.iausofa.org/2013_1202_C/sofa/epj.c
#     DJ00 = 2451545.0 # Reference epoch (J2000.0), Julian Date
#     DJY = 365.25 # Days per Julian year
#     epj = 2000.0 + (dj - DJ00)/DJY;
#     return epj