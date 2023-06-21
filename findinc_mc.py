#! /usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

from sys import argv
from sklearn.neighbors import KernelDensity

def helpf():
    print("\n  Program findinc_mc.py for Linux, MacOS, and Windows written by K. Bicz, ver. of Apr. 19, 2023.")
    print("  Estimate inclination angle of the star using its parameters and monte-carlo methods.\n")
    print("  Usage: findinc_mc.py [-vsini=float] [-verr=float] [-prot=float] [-perr=float] [-rad=float] [-rerr=float]")
    print("         [-ntrials=int] [--plot]")
    print()
    print("         option -vsini : vsin(i) of the star (default vsini = 170 km/s).")
    print("                -verr : uncertainty of vsin(i) of the star (default verr = 17 km/s).")
    print("                -prot : rotational period of the star (default prot = 0.23540915 days).")
    print("                -perr : uncertainty of rotational period of the star (default perr = 4.5929e-04 days).")
    print("                -rad : radius of the star in solar radii (default rad = 0.799503 Rsun).")
    print("                -rerr : uncertainty of the radius of the star in solar radii (default rerr = 0.0540905 Rsun).")
    print("                -ntrials: : number of MC simulations (default ntrials = 100000).")
    print("                --plot : plot the histogram with the results.")
    print()
    exit()

def str_to_num(string,ntype,name):
    try:
        return ntype(string)
    except ValueError:
        print("\a# Error! {} has to be number!".format(name))
        exit()

def density_function(x, kde, mean, power):
    if type(x) is not np.ndarray:
           x = np.array([np.array([x])])
    return np.exp(kde.score_samples(x))*(x[0][0]-mean)**power

def main(vsini,vsinierr,prot,perr,r,rerr,mc_trials,plotctrl):

    legpara = {'size':12,'weight':'bold'}
    yts, ytw = 14, 'normal'
    yls, ylw = 18, 'bold'
    xts, xtw = 14, 'normal'
    xls, xlw = 18, 'bold'
    ylp, xlp = 12, 12 


    radius = np.random.choice(np.arange(r-rerr,r+rerr,rerr/100),mc_trials)
    per = np.random.choice(np.arange(prot-perr,prot+perr,perr/100),mc_trials)
    vsi = np.random.choice(np.arange(vsini-vsinierr,vsini+vsinierr,vsinierr/100),mc_trials)
    
    cpt = np.vstack([radius,per,vsi])

    mc = []
    for i in range(mc_trials):
        val = cpt[2][i]*cpt[1][i]*24*60*60/(2*np.pi*cpt[0][i]*695700)
        if np.abs(val) <= 1:
            mc.append(np.arcsin(val)*180/np.pi)

    mc_function_trials = np.array(mc)
    kde = (KernelDensity(kernel='gaussian', bandwidth=2).fit(mc_function_trials[:, np.newaxis]))

    time_values = np.linspace(0,90,1000)[:, np.newaxis]
    #mean = integrate.quad(density_function,-np.inf,np.inf,args=(kde,0,1))[0]
    values = density_function(time_values,kde,0,0)
    mean = time_values[values.argmax()][0]
    std = np.sqrt(integrate.quad(density_function,-np.inf,np.inf,args=(kde,mean,2)))
    print("i = {:.0f} +/- {:.0f} deg".format(mean,std[0]))

    if plotctrl:
        _,ax = plt.subplots(figsize=(10,5))
        ax.hist(mc,bins='auto',color="C0")#,edgecolor='black'
        ax.set_xlabel("Inclination [deg]",fontsize=xls, weight=xlw, labelpad=xlp)
        ax.set_ylabel("Count", fontsize=yls, weight=ylw, labelpad=ylp)
        ax.set_xlim([0,90])
        ax2=ax.twinx()
        ax2.plot(time_values, values,"C3",linewidth=2)
        ax2.set_ylabel("Probability distribution", fontsize=yls, weight=ylw, labelpad=ylp)
        ax2.set_ylim(0)
        for tick in ax.xaxis.get_major_ticks():
            tick.label1.set_fontsize(xts) 
            tick.label1.set_weight(xtw)
        for tick in ax.yaxis.get_major_ticks():
            tick.label1.set_fontsize(yts) 
            tick.label1.set_weight(ytw)
        ax.minorticks_on()
        ax2.minorticks_on()
        ax.tick_params('both', length=7, width=1, which='major')
        ax2.tick_params('both', length=7, width=1, which='major')
        ax.tick_params('both', length=3, width=1, which='minor')
        ax2.tick_params('both', length=3, width=1, which='minor')
        ylim = ax2.set_ylim()
        ax2.plot([np.round(mean),np.round(mean)], ylim ,"k--",label="i = {:.0f} +/- {:.0f} deg".format(mean,std[0]),lw=2)
        ax2.tick_params(labelsize=yts)
        ax2.set_ylim(ylim)
        leg = ax2.legend(prop=legpara)
        leg.get_frame().set_linewidth(0.0)
        plt.subplots_adjust(top=0.945,bottom=0.15,left=0.11,right=0.89)
        plt.show()

    return 0

if __name__ == "__main__":
    vsini = 170
    vsinierr = 17
    prot = 0.23540915
    perr = 4.5929e-04
    r = 0.799503
    rerr = 0.0540905
    mc_trials = 100000
    plotctrl = False

    for arg in argv:
        if "-vsini=" in arg: vsini = abs(str_to_num(arg.split("=")[-1],float,"vsini"))
        elif "-verr=" in arg: vsinierr = abs(str_to_num(arg.split("=")[-1],float,"vsini error"))
        elif "-prot=" in arg: prot = abs(str_to_num(arg.split("=")[-1],float,"prot"))
        elif "-perr=" in arg: proterr = abs(str_to_num(arg.split("=")[-1],float,"prot error"))
        elif "-rad=" in arg: r = abs(str_to_num(arg.split("=")[-1],float,"radius"))
        elif "-rerr=" in arg: rerr = abs(str_to_num(arg.split("=")[-1],float,"radius error"))
        elif "-ntrials=" in arg: mc_trials = abs(str_to_num(arg.split("=")[-1],int,"number of trails"))
        elif arg == "--plot": plotctrl = True
        elif arg == '-h' or arg == "--help": helpf()

    main(vsini,vsinierr,prot,perr,r,rerr,mc_trials,plotctrl)
