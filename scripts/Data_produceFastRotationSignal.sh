     inputRootFile="root/FastRotation_60h.root"
    outputRootFile="root/test.root"
         histoName="FastRotation/mergedCalo_intensitySpectrum"
       rebinFactor=100
                tS=4   # in mico-sec
                tM=500 # in mico-sec
      startFitTime=30  # in mico-sec
        endFitTime=500  # in mico-sec
         printPlot=1
          saveROOT=1

python python/Data_produceFastRotationSignal.py $inputRootFile $outputRootFile $histoName $rebinFactor $tS $tM $startFitTime $endFitTime $printPlot $saveROOT -b
