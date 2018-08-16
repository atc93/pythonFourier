# coding: utf-8

## Module importS

import ROOT as r
import math
from array import array
import numpy as np
import thread
import matplotlib.pyplot as plt
import sys
from scipy.optimize import curve_fit

printPlot = 1
saveROOT  = 1

## Get command line argumentS

cmdargs = str(sys.argv)

t0 = float( str(sys.argv[1]) )
tS = float( str(sys.argv[2]) )
tm = float( str(sys.argv[3]) )
fieldIndex = float( str(sys.argv[4]) )
outTextFile = str(sys.argv[5])
inputFile = str(sys.argv[6])
outputFile = str(sys.argv[7])

print ' ================ '
print '   t0 = ', t0
print '   tS = ', tS
print '   tm = ', tm
print '   n  = ', fieldIndex
print ' ================ '

## Set Canvas style

c = r.TCanvas('c1','c1',900,600)
#c.SetGridx()
#c.SetGridy()
c.SetTicks(1)
r.gStyle.SetOptStat(0)
c.SetLeftMargin(0.15);
c.SetRightMargin(0.05);
c.SetTopMargin(0.05);
c.SetBottomMargin(0.15);


## Retrieve and plot histogram from ROOT file


#fileName = '~/python/' + inputFile
fileName = inputFile
file = r.TFile(fileName)
fr = file.Get('fr')
fr.SetTitle("")
fr.GetYaxis().SetTitle("Intensity [a.u.]")

fr.Draw()
fr.GetXaxis().SetRangeUser(tS,tS+1)
c.Draw("")   
if ( printPlot == 1 ):
    c.Print('plots/eps/FRS_{3}us_{4}us_t0_{0:.5f}_tS_{1}_tm_{2}.eps'.format(t0, tS, tm, tS,tS+1))    
    c.Print('plots/png/FRS_{3}us_{4}us_t0_{0:.5f}_tS_{1}_tm_{2}.png'.format(t0, tS, tm, tS,tS+1))    
fr.GetXaxis().SetRangeUser(tS,tS+10)
c.Draw("")   
if ( printPlot == 1 ):
    c.Print('plots/eps/FRS_{3}us_{4}us_t0_{0:.5f}_tS_{1}_tm_{2}.eps'.format(t0, tS, tm, tS,tS+10))    
    c.Print('plots/png/FRS_{3}us_{4}us_t0_{0:.5f}_tS_{1}_tm_{2}.png'.format(t0, tS, tm, tS,tS+10))    
fr.GetXaxis().SetRangeUser(tS,tS+50)
c.Draw("")   
if ( printPlot == 1 ):
    c.Print('plots/eps/FRS_{3}us_{4}us_t0_{0:.5f}_tS_{1}_tm_{2}.eps'.format(t0, tS, tm, tS,tS+50))    
    c.Print('plots/png/FRS_{3}us_{4}us_t0_{0:.5f}_tS_{1}_tm_{2}.png'.format(t0, tS, tm, tS,tS+50))    
fr.GetXaxis().SetRangeUser(tS,tm)
c.Draw("")   
if ( printPlot == 1 ):
    c.Print('plots/eps/FRS_{3}us_{4}us_t0_{0:.5f}_tS_{1}_tm_{2}.eps'.format(t0, tS, tm, tS,tm))    
    c.Print('plots/png/FRS_{3}us_{4}us_t0_{0:.5f}_tS_{1}_tm_{2}.png'.format(t0, tS, tm, tS,tm))    


# # Real transform

startBin = fr.FindBin(tS) 
endBin   = fr.FindBin(tm)

# Copy histogram to numpy array
# Need intermediate list step for good performance
# Otherwise need to copy over and over the array to itSelf addingt one value...
binCenter = np.array([])
binContent = np.array([])
a = []
b = []
for j in range(startBin, endBin):
    a.append( fr.GetBinContent(j) )
    b.append( fr.GetBinCenter(j) )   
    binContent = np.asarray(a)  
    binCenter = np.asarray(b)   

# Compute the cosine transform
def calc_freq_dist(t0):

    for i in range(150):
        frequency = 6.6305 + i*0.001
        integral = binContent*np.cos(2*math.pi*frequency*(binCenter-t0))*0.001
        real.SetBinContent(i+1, (np.sum(integral))) 


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
    c.Print('plots/eps/Real_t0_{0:.5f}_tS_{1}_tm_{2}.eps'.format(t0, tS, tm))

## First Apprxomiation

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
    c.Print('plots/eps/FirstApproximation_t0_{0:.5f}_tS_{1}_tm_{2}.eps'.format(t0, tS, tm))


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
    m, c = np.linalg.lstSq(A, y,rcond=None)[0]

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
    c.Print('plots/eps/Parabola_t0_{0:.5f}_tS_{1}_tm_{2}.eps'.format(t0, tS, tm))    


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
    c.Print('plots/eps/CompleteDistribution_t0_{0:.5f}_tS_{1}_tm_{2}.eps'.format(t0, tS, tm))    


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


xe = np.average(radius, axis=0, weightS=intensity)   
maxI = np.amax(intensity)
intensity = intensity/maxI

graph = r.TGraph(149,radius,intensity)
graph.SetTitle('')
graph.GetXaxis().SetTitle("Radius [mm]")
graph.GetYaxis().SetTitle("Arbitrary unitS")
graph.GetXaxis().CenterTitle()
graph.GetYaxis().CenterTitle()
graph.GetXaxis().SetTitleOffset(1.4)
graph.GetXaxis().SetTitleSize(0.055);
graph.GetXaxis().SetLabelSize(0.05);
graph.GetYaxis().SetTitleOffset(1.4)
graph.GetYaxis().SetTitleSize(0.055);
graph.GetYaxis().SetLabelSize(0.05);
graph.GetXaxis().SetRangeUser(7052,7172)
graph.SetMarkerStyle(20)
graph.SetMarkerSize(0.6)
graph.SetMarkerColor(4)
graph.SetLineColor(4)
graphMin = -0.05
graphMax = 1.1
graph.SetMaximum(graphMax)
graph.SetMinimum(graphMin)

innerLine = r.TLine(7067, graphMin, 7067, graphMax)
innerLine.SetLineWidth(2)
outerLine = r.TLine(7157, graphMin, 7157, graphMax)
outerLine.SetLineWidth(2)
magicLine = r.TLine(7112, graphMin, 7112, graphMax)
magicLine.SetLineWidth(1)
magicLine.SetLineStyle(7)

pt=r.TPaveText(7060, graphMax*0.45,7074,graphMax*0.55);
pt2=r.TPaveText(7150,graphMax*0.45,7164,graphMax*0.55);
pt3=r.TPaveText(7113,graphMax*0.04,7121,graphMax*0.11);
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
pt3.AddText("magic");
pt3.AddText("radius");
pt3.SetShadowColor(0);
pt3.SetBorderSize(1);
pt3.SetFillColor(0);
pt3.SetLineWidth(1);
pt3.SetLineColor(1);


if ( saveROOT == 1 ):
    file = r.TFile(outputFile, "RECREATE")
    graph.Write("rad")
    file.Close()

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

graph.Draw('APL')
innerLine.Draw("same")
outerLine.Draw("same")
magicLine.Draw("same")
pt.Draw("same")
pt2.Draw("same")
pt3.Draw("same")
c.Draw()

if ( printPlot == 1 ):
    c.Print('plotS/eps/Radial_t0_{0:.5f}_tS_{1}_tm_{2}.eps'.format(t0, tS, tm))    
    c.Print('plotS/png/Radial_t0_{0:.5f}_tS_{1}_tm_{2}.png'.format(t0, tS, tm))    


for x,y in zip(radius, intensity):
    print x, y

#print 'a = ', a
#print 'b = ', b
xe -= 7112

C_E_reco  = -2*beta*beta*fieldIndex*(1-fieldIndex)*msd/(7112*7112)*1e9
#print 'C_E reco  ', C_E_reco, ' ppb'

text_file = open(str(outTextFile), "a")
text_file.write('t0 %f tS %f tm %f fieldIndex %f fom %f xe_reco %f std_reco %f C_E_reco %f \n' % 
        (t0, tS, tm, fieldIndex, fom, xe, std, C_E_reco) )
text_file.close()

# In[ ]:
