
# coding: utf-8

# # Module imports

# In[1]:


import ROOT as r
import math
from array import array
import numpy as np
import thread
import matplotlib.pyplot as plt
import sys
from scipy.optimize import curve_fit

printPlot = 0

# # Get command line arguments

cmdargs = str(sys.argv)

t0 = float( str(sys.argv[1]) )
tS = float( str(sys.argv[2]) )
tm = float( str(sys.argv[3]) )
fieldIndex = float( str(sys.argv[4]) )
outTextFile = str(sys.argv[5])
inputFile = str(sys.argv[6])

print ' ================ '
print '   t0 = ', t0
print '   tS = ', tS
print '   tm = ', tm
print '   n  = ', fieldIndex
print ' ================ '

# # Set Canvas style

# In[2]:


c = r.TCanvas('c1','c1',900,600)
c.SetGridx()
c.SetGridy()
c.SetTicks(1)
r.gStyle.SetOptStat(0)


# # Retrieve and plot histogram from ROOT file

# In[4]:

#fileName = '~/python/' + inputFile
fileName = inputFile
file = r.TFile(fileName)
fr = file.Get('fr')
fr.SetTitle("Toy Model Fast Rotation")

# In[5]:


fr.Draw()
fr.GetXaxis().SetRangeUser(4,100)
c.Draw("")   
if ( printPlot == 1 ):
    c.Print("DataFRS.eps")


# # Real transform

# In[ ]:


def calc_freq_dist(t0):
    
    startBin = fr.FindBin(tS) # assume we do not have the first 4 micro-seconds of data
    endBin   = fr.FindBin(tm)
        
    for i in range(150):
        
        frequency = 6.630 + i*0.001
        integral = 0.
        
        for j in range(startBin, endBin):
        
            integral += fr.GetBinContent(j)*math.cos(2*math.pi*frequency*(fr.GetBinCenter(j)-t0))*0.001

        
        real.SetBinContent(i+1,integral)


# In[ ]:


intensity, radius, minDelta, t0Array = array( 'd' ), array( 'd' ), array( 'd' ), array( 'd' )

real = r.TH1D("freq","freq",150,6630,6780)
calc_freq_dist(t0)

real.GetXaxis().SetRangeUser(6630, 6700)
minBin1 = real.GetMinimum()
real.GetXaxis().SetRangeUser(6700, 6780)
minBin2 = real.GetMinimum()
real.GetXaxis().SetRangeUser(6630, 6780)

fom = minBin1-minBin2

minDelta.append(minBin1-minBin2)
t0Array.append(t0)

realClone = real.Clone()
realClone.SetTitle('Real transform (t0= {0:.4f} #mus)'.format(t0))
realClone.GetXaxis().SetTitle("Frequency [kHz]")
realClone.GetXaxis().CenterTitle()
realClone.GetXaxis().SetTitleOffset(1.3)
realClone.SetLineColor(4)
realClone.SetLineWidth(2)

realClone.SetMaximum( realClone.GetMaximum()*1.3 ) 
realClone.SetMinimum( realClone.GetMinimum()*1.2 ) 

innerLine = r.TLine(6662.799323395121, realClone.GetMinimum(), 6662.799323395121, realClone.GetMaximum())
innerLine.SetLineWidth(3)
outerLine = r.TLine(6747.651727400435, realClone.GetMinimum(), 6747.651727400435, realClone.GetMaximum())
outerLine.SetLineWidth(3)    

pt=r.TPaveText(6650,realClone.GetMaximum()*0.38,6674,realClone.GetMaximum()*0.52);
pt2=r.TPaveText(6737,realClone.GetMaximum()*0.38,6759,realClone.GetMaximum()*0.52);
pt.AddText("collimators");
pt.AddText("aperture");
pt.SetShadowColor(0);
pt.SetBorderSize(1);
pt.SetFillColor(0);
pt.SetLineWidth(1);
pt.SetLineColor(1);
pt.SetTextAngle(90);
pt2.AddText("collimators");
pt2.AddText("aperture");
pt2.SetShadowColor(0);
pt2.SetBorderSize(1);
pt2.SetFillColor(0);
pt2.SetLineWidth(1);
pt2.SetLineColor(1);
pt2.SetTextAngle(90);    

realClone.Draw()
innerLine.Draw("same")
outerLine.Draw("same")
pt.Draw("same")
pt2.Draw("same")

c.Draw()
if ( printPlot == 1 ):
    c.Print('Real_t0_{0:.5f}_tS_{1}_tm_{2}.eps'.format(t0, tS, tm))

# In[ ]:


#scaledt0Array = [i * 1000 for i in t0Array]
#
#def func(x, a, b, ):
#    return a * x * x + b
#
#parameter, covariance_matrix = curve_fit(func, scaledt0Array, minDelta)
#x = np.linspace(min(scaledt0Array), max(scaledt0Array), 5)
#
#plt.plot(scaledt0Array, minDelta, 'rx', label='data')
#plt.ylabel('FOM')
#plt.xlabel('t0 [ns]')
#plt.plot(x, func(x, *parameter), '-b', label='fit')
#plt.savefig('t0Opt_TM1_fine.eps', format='eps')
#plt.show()


# # First Apprxomiation

# In[ ]:


approx = real.Clone()

maxBin = approx.GetMaximumBin()

approx.GetXaxis().SetRangeUser(6630, 6700)
minBin1 = approx.GetMinimumBin()

approx.GetXaxis().SetRangeUser(6700, 6780)
minBin2 = approx.GetMinimumBin()

#print minBin1, freq.GetBinContent(minBin1), minBin2, freq.GetBinContent(minBin2)

minA =  (approx.GetBinContent(minBin1) + approx.GetBinContent(minBin2)) / 2

for iBin in range(1, minBin1):
    approx.SetBinContent(iBin, 0)
    
for iBin in range(minBin2+1, 151):
    approx.SetBinContent(iBin, 0)    
    
approx.GetXaxis().SetRangeUser(6630, 6780)    

for iBin in range(minBin1, minBin2+1):
    approx.AddBinContent(iBin, -1*minA)
    
approxClone = approx
approxClone.SetTitle("First approximation")    
    
approxClone.GetXaxis().SetTitle("Frequency [kHz]")
approxClone.GetXaxis().CenterTitle()
approxClone.GetXaxis().SetTitleOffset(1.3)
approxClone.SetLineColor(4)
approxClone.SetLineWidth(2)
    
approxClone.SetMaximum( approxClone.GetMaximum()*1.3 ) 
approxClone.SetMinimum( -0.5 ) 
    
innerLine = r.TLine(6662.799323395121, approxClone.GetMinimum(), 6662.799323395121, approxClone.GetMaximum())
innerLine.SetLineWidth(3)
outerLine = r.TLine(6747.651727400435, approxClone.GetMinimum(), 6747.651727400435, approxClone.GetMaximum())
outerLine.SetLineWidth(3)    

pt=r.TPaveText(6650,approxClone.GetMaximum()*0.9,6674,approxClone.GetMaximum()*1);
pt2=r.TPaveText(6737,approxClone.GetMaximum()*0.9,6759,approxClone.GetMaximum()*1);
pt.AddText("collimators");
pt.AddText("aperture");
pt.SetShadowColor(0);
pt.SetBorderSize(1);
pt.SetFillColor(0);
pt.SetLineWidth(1);
pt.SetLineColor(1);
pt.SetTextAngle(90);
pt2.AddText("collimators");
pt2.AddText("aperture");
pt2.SetShadowColor(0);
pt2.SetBorderSize(1);
pt2.SetFillColor(0);
pt2.SetLineWidth(1);
pt2.SetLineColor(1);
pt2.SetTextAngle(90);    

approxClone.Draw()
innerLine.Draw("same")
outerLine.Draw("same")
pt.Draw("same")
pt2.Draw("same")   
c.Draw()    

if ( printPlot == 1 ):
    c.Print('FirstApproximation_t0_{0:.5f}_tS_{1}_tm_{2}.eps'.format(t0, tS, tm))


# # Delta Correction

# In[ ]:


# Correction
rcorrs = real.Clone()
rcorrs.Scale(0)
for i in range(150):

        frq = 6630.5 + i*1
        integral = 0

        for j in range(1, 150):
            if (approx.GetBinCenter(j)-frq) != 0:
                integral += approx.GetBinContent(j)*math.sin(2*math.pi*(frq-approx.GetBinCenter(j))*(tS-0.0745)/1000)/(1000*(frq-approx.GetBinCenter(j))  )
            else:
                integral += 2*math.pi*approx.GetBinContent(j)*(tS-0.0745)/1000000

        rcorrs.SetBinContent(i+1,integral)
rcorrs.Draw()
rcorrs.SetTitle("The parabola")
c.Update()
c.Draw()


# # 'a' and 'b'optimization

# In[ ]:


# a and b minimization
def minimization():


    x = []
    y = []

    for i in range(32):
        x.append(rcorrs.GetBinContent(i+1))
        y.append(real.GetBinContent(i+1))
        x.append(rcorrs.GetBinContent(150-i))
        y.append(real.GetBinContent(150-i))

    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y,rcond=None)[0]

    return m, c


# In[ ]:


real.Draw()
c.Draw()
a,b = minimization()

# # Scaled parabola

# In[ ]:


for iBin in range(1,151):
    rcorrs.SetBinContent(iBin, -1*( a*rcorrs.GetBinContent(iBin)+b) )
    
    
rcorrsClone = rcorrs.Clone()
rcorrsClone.SetTitle("Parabola")    
    
rcorrsClone.GetXaxis().SetTitle("Frequency [kHz]")
rcorrsClone.GetXaxis().CenterTitle()
rcorrsClone.GetXaxis().SetTitleOffset(1.3)
rcorrsClone.SetLineColor(4)
rcorrsClone.SetLineWidth(2)
    
rcorrsClone.SetMaximum( rcorrsClone.GetMaximum()*1.15 ) 
rcorrsClone.SetMinimum( rcorrsClone.GetMinimum()*0.85 ) 
    
innerLine = r.TLine(6662.799323395121, rcorrsClone.GetMinimum(), 6662.799323395121, rcorrsClone.GetMaximum())
innerLine.SetLineWidth(3)
outerLine = r.TLine(6747.651727400435, rcorrsClone.GetMinimum(), 6747.651727400435, rcorrsClone.GetMaximum())
outerLine.SetLineWidth(3)    

pt=r.TPaveText(6650,rcorrsClone.GetMaximum()*0.9,6674,rcorrsClone.GetMaximum()*1);
pt2=r.TPaveText(6737,rcorrsClone.GetMaximum()*0.9,6759,rcorrsClone.GetMaximum()*1);
pt.AddText("collimators");
pt.AddText("aperture");
pt.SetShadowColor(0);
pt.SetBorderSize(1);
pt.SetFillColor(0);
pt.SetLineWidth(1);
pt.SetLineColor(1);
pt.SetTextAngle(90);
pt2.AddText("collimators");
pt2.AddText("aperture");
pt2.SetShadowColor(0);
pt2.SetBorderSize(1);
pt2.SetFillColor(0);
pt2.SetLineWidth(1);
pt2.SetLineColor(1);
pt2.SetTextAngle(90);    
    
rcorrsClone.Draw()
innerLine.Draw("same")
outerLine.Draw("same")
pt.Draw("same")
pt2.Draw("same")    
c.Draw()    
if ( printPlot == 1 ):
    c.Print('Parabola_t0_{0:.5f}_tS_{1}_tm_{2}.eps'.format(t0, tS, tm))    


# # Complete distribution

# In[ ]:


full = real.Clone()
for iBin in range(1,151):
    full.AddBinContent(iBin, rcorrs.GetBinContent(iBin) )
full.SetTitle("Complete distribution")    

fullClone = full.Clone()
fullClone.SetTitle("Complete distribution")    
    
fullClone.GetXaxis().SetTitle("Frequency [kHz]")
fullClone.GetXaxis().CenterTitle()
fullClone.GetXaxis().SetTitleOffset(1.3)
fullClone.SetLineColor(4)
fullClone.SetLineWidth(2)
    
fullClone.SetMaximum( fullClone.GetMaximum()*1.15 ) 
fullClone.SetMinimum( -0.5 ) 
    
innerLine = r.TLine(6662.799323395121, fullClone.GetMinimum(), 6662.799323395121, fullClone.GetMaximum())
innerLine.SetLineWidth(3)
outerLine = r.TLine(6747.651727400435, fullClone.GetMinimum(), 6747.651727400435, fullClone.GetMaximum())
outerLine.SetLineWidth(3)    

pt=r.TPaveText(6650,fullClone.GetMaximum()*0.9,6674,fullClone.GetMaximum()*1);
pt2=r.TPaveText(6737,fullClone.GetMaximum()*0.9,6759,fullClone.GetMaximum()*1);
pt.AddText("collimators");
pt.AddText("aperture");
pt.SetShadowColor(0);
pt.SetBorderSize(1);
pt.SetFillColor(0);
pt.SetLineWidth(1);
pt.SetLineColor(1);
pt.SetTextAngle(90);
pt2.AddText("collimators");
pt2.AddText("aperture");
pt2.SetShadowColor(0);
pt2.SetBorderSize(1);
pt2.SetFillColor(0);
pt2.SetLineWidth(1);
pt2.SetLineColor(1);
pt2.SetTextAngle(90);    
    
fullClone.Draw()
innerLine.Draw("same")
outerLine.Draw("same")
pt.Draw("same")
pt2.Draw("same")    
c.Draw()    
if ( printPlot == 1 ):
    c.Print('CompleteDistribution_t0_{0:.5f}_tS_{1}_tm_{2}.eps'.format(t0, tS, tm))    


# # Conversion frequency -> radius

# In[ ]:


muonMass = .105658
magicP = 3.094
E = math.sqrt(muonMass*muonMass+magicP*magicP)
gamma = E / muonMass
beta = magicP / ( gamma * muonMass )
speed = beta * 299792458
#print 'Total Energy = ', E
#print 'Gamma = ', gamma
#print 'Beta = ', beta
#print 'Speed = ', speed, ' m/s'


# In[ ]:


intensity, radius = array( 'd' ), array( 'd' )

for i in range(1, 150):
    #print i, full.GetBinCenter(i)
    radius.append( speed / (2*math.pi*full.GetBinCenter(i)) )
    intensity.append( full.GetBinContent(i))

xe = np.average(radius, axis=0, weights=intensity)    
    
graph = r.TGraph(150,radius,intensity)
graph.SetTitle('Radial distribution')
graph.GetXaxis().SetTitle("x_{e} [mm]")
graph.GetYaxis().SetTitle("")
graph.GetXaxis().CenterTitle()
graph.GetXaxis().SetTitleOffset(1.3)
graph.GetXaxis().SetRangeUser(7067,7157)
graph.GetXaxis().SetRangeUser(7067,7157)
graph.SetMarkerStyle(20)
graph.SetMarkerSize(0.6)
graph.SetMarkerColor(4)

std = 0
sum = 0
for i,j in zip(radius,intensity):
    sum += j
    std += (j) * (i-xe) * (i-xe)

std /= sum
std = math.sqrt(std)

sum = 0
msd = 0
for i,j in zip(radius,intensity):
    sum += j
    msd += (j) * (i-7112) * (i-7112 )
    
msd /= sum

#print std

graph.Draw('AP')
c.Draw()
if ( printPlot == 1 ):
    c.Print('Radial_t0_{0:.5f}_tS_{1}_tm_{2}.eps'.format(t0, tS, tm))    


#print 'a = ', a
#print 'b = ', b
xe -= 7112

C_E_reco  = -2*beta*beta*fieldIndex*(1-fieldIndex)*msd/(7112*7112)*1e9
#print 'C_E truth ', C_E_truth, ' ppb'
#print 'C_E reco  ', C_E_reco, ' ppb'

text_file = open(str(outTextFile), "a")
text_file.write('t0 %f tS %f tm %f fieldIndex %f fom %f xe_reco %f std_reco %f C_E_reco %f \n' % 
        (t0, tS, tm, fieldIndex, fom, xe, std, C_E_reco) )
text_file.close()

# In[ ]:
