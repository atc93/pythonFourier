# coding: utf-8

## Module imports

from importAll import *

## Get command line argumentS

cmdargs = str(sys.argv)

inputRootFile   = str(sys.argv[1])
outputRootFile  = str(sys.argv[2])
histoName       = str(sys.argv[3])
rebinFactor     = int(sys.argv[4])
tS              = int(sys.argv[5]) # in mico-sec
tM              = int(sys.argv[6]) # in mico-sec
startFitTime    = int(sys.argv[7]) # in mico-sec
endFitTime      = int(sys.argv[8]) # in mico-sec
printPlot       = int(sys.argv[9])
saveROOT        = int(sys.argv[10])

## Retrieve and plot histogram from ROOT file

inFile      = r.TFile( inputRootFile)
outFile     = r.TFile(outputRootFile,'RECREATE')

signal  = inFile.Get( histoName )

## Styling and plotting

c = r.TCanvas('c','c',900,600)
setCanvasStyle( c )
setHistogramStyle( signal, 'Time [#mus]', 'Intensity')

if ( printPlot == 1 ):
    plot( c, signal, 'Intensity', tS, tS+1 )
    plot( c, signal, 'Intensity', tS, tS+10 )
    plot( c, signal, 'Intensity', tS, tS+50 )
    plot( c, signal, 'Intensity', tS, tM )

## Rebin, fit and plot wiggle plot

fr = signal.Clone()
signal.Rebin(rebinFactor)

fit = r.TF1("fit","[0]*exp(-x/[1])*(1+[2]*cos(2*TMath::Pi()*[3]*x+[4]))", startFitTime, endFitTime)
fit.SetParameters(500000,64.4,0.4,0.227,1)
fit.SetNpx(10000)
signal.Fit("fit","SREMQ")

if ( printPlot == 1 ):
    plot( c, signal, 'FittedWiggle', startFitTime, startFitTime+1 )
    plot( c, signal, 'FittedWiggle', startFitTime, startFitTime+10 )
    plot( c, signal, 'FittedWiggle', startFitTime, startFitTime+50 )
    plot( c, signal, 'FittedWiggle', startFitTime, startFitTime+100 )
    plot( c, signal, 'FittedWiggle', startFitTime, startFitTime+200 )
    plot( c, signal, 'FittedWiggle', startFitTime, endFitTime )
    plot( c, signal, 'FittedWiggle', endFitTime-200, endFitTime )
    plot( c, signal, 'FittedWiggle', endFitTime-100, endFitTime )


## Produce finely binned and normalized wiggle plot to original intensity histogram

nBins = fr.GetXaxis().GetNbins()
norm = r.TH1D("norm","norm",nBins,0,tM)
norm.SetLineColor(4)
setHistogramStyle( norm, 'Time [#mus]', 'Intensity')

for i in range(nBins):
    norm.SetBinContent(i,fit.Eval(norm.GetBinCenter(i))/rebinFactor)
    
if ( printPlot == 1 ):
    plot( c, norm, 'WiggleFRS', tS, tS+1 )
    plot( c, norm, 'WiggleFRS', tS, tS+10 )
    plot( c, norm, 'WiggleFRS', tS, tS+50 )
    plot( c, norm, 'WiggleFRS', tS, tS+100 )
    plot( c, norm, 'WiggleFRS', tS, tM )

norm.Write("wiggleHistogram")


## Generate FRS (correct original histogram by wiggle fit)

fr.Divide(norm)
fr.Write("fr")

## Print and save FRS histogram

if ( printPlot == 1 ):
    plot( c, fr, 'FRS', tS, tS+1 )
    plot( c, fr, 'FRS', tS, tS+10 )
    plot( c, fr, 'FRS', tS, tS+50 )
    plot( c, fr, 'FRS', tS, tM )

## Close output ROOT file

outFile.Close()
