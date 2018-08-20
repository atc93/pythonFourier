# coding: utf-8

## Module importS

from importAll import *

## Get command line argumentS

cmdargs = str(sys.argv)

inputRootFile   = str(sys.argv[1])
outputRootFile  = str(sys.argv[2])
outputTextFile  = str(sys.argv[3)
histoName       = str(sys.argv[4])
t0              = float(sys.argv[5]) # in mico-sec
tS              = float(sys.argv[6]) # in mico-sec
tM              = float(sys.argv[7]) # in mico-sec
fieldIndex      = float(sys.argv[8)
printPlot       = int(sys.argv[9])
saveROOT        = int(sys.argv[10])
tag             = str(sys.argv[11])

print ' ================ '
print '   t0 = ', t0
print '   tS = ', tS
print '   tM = ', tM
print '   n  = ', fieldIndex
print ' ================ '

## Styling and plotting

c = r.TCanvas('c','c',900,600)
setCanvasStyle( c )

## Retrieve and plot histogram from ROOT file


inFile = r.TFile(fileName)
fr = inFile.Get('fr')
setHistogramStyle( fr, 'Time [#mus]', 'Intensity [a.u.]')


## Real transform

startBin = fr.FindBin(tS) 
endBin   = fr.FindBin(tM)

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

# Fourier analysis starts here

intensity, radius, minDelta, = array( 'd' ), array( 'd' ), array( 'd' )

cosine  = r.TH1D("cosine",  "cosine",   150,6630,6780)
sine    = r.TH1D("sin",     "sine",     150,6630,6780)

calc_cosine_dist(t0, cosine)
calc_sine_dist(t0, sine)

cosine.GetXaxis().SetRangeUser(6630, 6700)
minBin1 = cosine.GetMinimum()
cosine.GetXaxis().SetRangeUser(6700, 6780)
minBin2 = cosine.GetMinimum()
cosine.GetXaxis().SetRangeUser(6630, 6780)

fom = minBin1-minBin2

minDelta.append(minBin1-minBin2)

cosineClone = cosine.Clone()
cosineClone.SetTitle('Real transform (t0= {0:.4f} #mus)'.format(t0))
cosineClone.GetXaxis().SetTitle("Frequency [kHz]")
cosineClone.GetXaxis().CenterTitle()
cosineClone.GetXaxis().SetTitleOffset(1.3)
cosineClone.SetLineColor(4)
cosineClone.SetLineWidth(2)

cosineClone.SetMaximum( cosineClone.GetMaximum()*1.3 ) 
cosineClone.SetMinimum( cosineClone.GetMinimum()*1.2 ) 

innerLine = r.TLine(6662.799323395121, cosineClone.GetMinimum(), 6662.799323395121, cosineClone.GetMaximum())
innerLine.SetLineWidth(3)
outerLine = r.TLine(6747.651727400435, cosineClone.GetMinimum(), 6747.651727400435, cosineClone.GetMaximum())
outerLine.SetLineWidth(3)    

pt=r.TPaveText(6650,cosineClone.GetMaximum()*0.38,6674,cosineClone.GetMaximum()*0.52);
pt2=r.TPaveText(6737,cosineClone.GetMaximum()*0.38,6759,cosineClone.GetMaximum()*0.52);
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

cosineClone.Draw()
innerLine.Draw("same")
outerLine.Draw("same")
pt.Draw("same")
pt2.Draw("same")

c.Draw()
if ( printPlot == 1 ):
    c.Print('plots/eps/Real_t0_{0:.5f}_tS_{1}_tM_{2}.eps'.format(t0, tS, tM))

## First Apprxomiation

approx = cosine.Clone()

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
    c.Print('plots/eps/FirstApproximation_t0_{0:.5f}_tS_{1}_tM_{2}.eps'.format(t0, tS, tM))


# # Delta Correction

# In[ ]:


# Correction
parabola = cosine.Clone()
parabola.Scale(0)


parabola.Draw()
parabola.SetTitle("The parabola")
c.Update()
c.Draw()


# # 'a' and 'b'optimization

# In[ ]:


# a and b minimization


# In[ ]:


cosine.Draw()
c.Draw()
a,b = minimization()

# # Scaled parabola

# In[ ]:


for iBin in range(1,151):
    parabola.SetBinContent(iBin, -1*( a*parabola.GetBinContent(iBin)+b) )
    
    
parabolaClone = parabola.Clone()
parabolaClone.SetTitle("Parabola")    
    
parabolaClone.GetXaxis().SetTitle("Frequency [kHz]")
parabolaClone.GetXaxis().CenterTitle()
parabolaClone.GetXaxis().SetTitleOffset(1.3)
parabolaClone.SetLineColor(4)
parabolaClone.SetLineWidth(2)
    
parabolaClone.SetMaximum( parabolaClone.GetMaximum()*1.15 ) 
parabolaClone.SetMinimum( parabolaClone.GetMinimum()*0.85 ) 
    
innerLine = r.TLine(6662.799323395121, parabolaClone.GetMinimum(), 6662.799323395121, parabolaClone.GetMaximum())
innerLine.SetLineWidth(3)
outerLine = r.TLine(6747.651727400435, parabolaClone.GetMinimum(), 6747.651727400435, parabolaClone.GetMaximum())
outerLine.SetLineWidth(3)    

pt=r.TPaveText(6650,parabolaClone.GetMaximum()*0.9,6674,parabolaClone.GetMaximum()*1);
pt2=r.TPaveText(6737,parabolaClone.GetMaximum()*0.9,6759,parabolaClone.GetMaximum()*1);
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
    
parabolaClone.Draw()
innerLine.Draw("same")
outerLine.Draw("same")
pt.Draw("same")
pt2.Draw("same")    
c.Draw()    
if ( printPlot == 1 ):
    c.Print('plots/eps/Parabola_t0_{0:.5f}_tS_{1}_tM_{2}.eps'.format(t0, tS, tM))    


# # Complete distribution

# In[ ]:


full = cosine.Clone()
for iBin in range(1,151):
    full.AddBinContent(iBin, parabola.GetBinContent(iBin) )
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
    c.Print('plots/eps/CompleteDistribution_t0_{0:.5f}_tS_{1}_tM_{2}.eps'.format(t0, tS, tM))    


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
    file = r.TFile(outputRootFile, "RECREATE")
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
    c.Print('plotS/eps/Radial_t0_{0:.5f}_tS_{1}_tM_{2}.eps'.format(t0, tS, tM))    
    c.Print('plotS/png/Radial_t0_{0:.5f}_tS_{1}_tM_{2}.png'.format(t0, tS, tM))    


for x,y in zip(radius, intensity):
    print x, y

#print 'a = ', a
#print 'b = ', b
xe -= 7112

C_E_reco  = -2*beta*beta*fieldIndex*(1-fieldIndex)*msd/(7112*7112)*1e9
#print 'C_E reco  ', C_E_reco, ' ppb'

text_file = open(str(outputTextFile), "a")
text_file.write('t0 %f tS %f tM %f fieldIndex %f fom %f xe_reco %f std_reco %f C_E_reco %f \n' % 
        (t0, tS, tM, fieldIndex, fom, xe, std, C_E_reco) )
text_file.close()

# In[ ]:
