t0=0
tS=4
tm=400
n=0.1075
textfile="txt/frs_60h_T1492_E1500.txt"
rootfile="root/frs_60h_T1492_E1500.root"

rm -f $textfile
./renice.sh >& renice.log &

for itm in {0..3}; do
    tm=$(echo "100+$itm*100" | bc)
    for itS in {0..12}; do
        tS=$(echo "3.850+$itS*0.025" | bc)
        for it0 in {0..15}; do
            t0=$(echo "-0.3270+$it0*0.0001" | bc)
            echo $t0, $tS, $tm
            python Data_fourierAnalysis.py $t0 $tS $tm $n $textfile $rootfile -b
        done
    done
done
