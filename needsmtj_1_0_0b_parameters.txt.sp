**********************************************************************
***                    Parameters/Definitions                      ***
**********************************************************************
.param pi='4*atan(1)'
.param kB='1.3806503e-23'
.param Temperature='25'
.param Ms='700'
.param alpha='0.028'
.param W='25e-9'
.param L='pi*25e-9'
.param Tm='1.4e-9'
.param Ea='56*kB*(300)*1e7'
.param Volume='W*L*Tm*1e6'
.param K='(Ea/Volume)'
.param P_L='0.8'
.param P_R='0.3'
.param Lambda_L='2'
.param Lambda_R='2'

** Coefficients for fitting Rap
.param c1_ap = -6.7524
.param c2_ap = 23.2848
.param c3_ap = -7.56891
.param c4_ap = 24.144
.param c5_p = 1

** Coefficients for fitting Rp
.param c1_p = -5.90497
.param c2_p = 21.5434
.param c3_p = -7.46919
.param c4_p = 25.0243
.param c5_ap = 1
