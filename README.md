# findinc_mc
Python code to estimate the inclination angle of the star using MC.
  
      Program findinc_mc.py for Linux, MacOS, and Windows written by K. Bicz, ver. of Apr. 19, 2023.
      Estimate inclination angle of the star using its parameters and monte-carlo methods.

      Usage: findinc_mc.py [-vsini=float] [-verr=float] [-prot=float] [-perr=float] [-rad=float] [-rerr=float]
             [-ntrials=int] [--plot]

         option -vsini : vsin(i) of the star (default vsini = 170 km/s).
                -verr : uncertainty of vsin(i) of the star (default verr = 17 km/s).
                -prot : rotational period of the star (default prot = 0.23540915 days).
                -perr : uncertainty of rotational period of the star (default perr = 4.5929e-04 days).
                -rad : radius of the star in solar radii (default rad = 0.799503 Rsun).
                -rerr : uncertainty of the radius of the star in solar radii (default rerr = 0.0540905 Rsun).
                -ntrials: : number of MC simulations (default ntrials = 100000).
                --plot : plot the histogram with the results.
