t0=0
tS=4
tm=400
n=0.1075
textfile="frs_60h_T1492_E1700.txt"
rootfile="~/jupyter/root/frs_60h_T1492_E1700.root"

rm -f $textfile

for itm in {0..0}; do
    tm=$(echo "100+$itm*50" | bc)
    for itS in {0..0}; do
        tS=$(echo "4+$itS*0.05" | bc)
        for it0 in {0..10}; do
            t0=$(echo "-0.3264+$it0*0.0002" | bc)
            echo $t0, $tS, $tm
            python Data.py $t0 $tS $tm $n $textfile $rootfile -b
        done
    done
done
