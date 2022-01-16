#!/bin/bash

mkdir -p compiled images

echo "----- FST FILES -----"
for i in sources/*.txt tests/*.txt; do
    echo "Compiling: $i"

    fstcompile --isymbols=syms.txt --osymbols=syms.txt $i | fstarcsort > compiled/$(basename $i ".txt").fst
done

echo "Compiling: date2year.fst"
fstconcat compiled/skip.fst compiled/skip.fst > compiled/skip2.fst
fstconcat compiled/skip2.fst compiled/skip2.fst > compiled/skip4.fst
fstconcat compiled/skip4.fst compiled/skip2.fst > compiled/skip6.fst
fstconcat compiled/copy.fst compiled/copy.fst > compiled/copy2.fst
fstconcat compiled/copy2.fst compiled/copy2.fst > compiled/copy4.fst
fstconcat compiled/skip6.fst compiled/copy4.fst > compiled/date2year.fst

echo "Compiling: leap.fst"
fstconcat compiled/skip2.fst compiled/leap_aux.fst > compiled/leap.fst

echo "Compiling: A2R.fst"
# Transducer i
fstinvert compiled/R2A.fst > compiled/A2R.fst

echo "Compiling: birthR2A.fst"
# Transducer j
fstcompose compiled/R2A.fst compiled/d2dd.fst > compiled/bR2A2.fst
fstcompose compiled/R2A.fst compiled/d2dddd.fst > compiled/bR2A4.fst
fstconcat compiled/bR2A2.fst compiled/copy.fst > compiled/dayB.fst
fstconcat compiled/dayB.fst compiled/bR2A2.fst > compiled/dayBmonth.fst
fstconcat compiled/dayBmonth.fst compiled/copy.fst > compiled/dayBmonthB.fst
fstconcat compiled/dayBmonthB.fst compiled/bR2A4.fst > compiled/birthR2A.fst

echo "Compiling: birthA2T.fst"
# Trasducer k
fstconcat compiled/copy.fst compiled/copy.fst > compiled/copy2.fst
fstconcat compiled/copy2.fst compiled/copy.fst > compiled/copy3.fst
fstconcat compiled/copy3.fst compiled/mm2mmm.fst > compiled/copy3M.fst
fstconcat compiled/copy3M.fst compiled/copy3.fst > compiled/copy3M3.fst
fstconcat compiled/copy3M3.fst compiled/copy2.fst > compiled/birthA2T.fst

echo "Compiling: birthT2R.fst"
# Transducer l
fstinvert compiled/d2dd.fst > compiled/inv_d2dd.fst
fstinvert compiled/d2dddd.fst > compiled/inv_d2dddd.fst
fstinvert compiled/mm2mmm.fst > compiled/inv_mm2mmm.fst
fstcompose compiled/inv_d2dd.fst compiled/A2R.fst > compiled/T2Rday.fst
fstconcat compiled/T2Rday.fst compiled/copy.fst > compiled/T2RdayB.fst
fstcompose compiled/inv_mm2mmm.fst compiled/inv_d2dd.fst > compiled/T2Rmonth.fst
fstcompose compiled/T2Rmonth.fst compiled/A2R.fst > compiled/T2RmonthR.fst
fstconcat compiled/T2RdayB.fst compiled/T2RmonthR.fst > compiled/T2RdayBmonth.fst
fstconcat compiled/T2RdayBmonth.fst compiled/copy.fst > compiled/T2RdayBmonthB.fst
fstcompose compiled/inv_d2dddd.fst compiled/A2R.fst > compiled/T2Ryear.fst
fstconcat compiled/T2RdayBmonthB.fst compiled/T2Ryear.fst > compiled/birthT2R.fst

echo "Compiling: birthR2L.fst"
# Transducer m
fstconcat compiled/skip.fst compiled/skip.fst > compiled/skip2.fst
fstcompose compiled/bR2A2.fst compiled/skip2.fst > compiled/R2Lskip2.fst
fstconcat compiled/R2Lskip2.fst compiled/skip.fst > compiled/R2Lskip3.fst
fstconcat compiled/R2Lskip3.fst compiled/R2Lskip3.fst > compiled/R2Lskip6.fst
fstcompose compiled/bR2A4.fst compiled/d2dddd.fst > compiled/R2Lyear.fst
fstcompose compiled/R2Lyear.fst compiled/leap.fst > compiled/R2Lleap.fst
fstconcat compiled/R2Lskip6.fst compiled/R2Lleap.fst > compiled/birthR2L.fst


echo
echo "----- IMAGES -----"
for i in compiled/*.fst; do
    echo "Image: $i"

    fstdraw --portrait --isymbols=syms.txt --osymbols=syms.txt $i | dot -Tpdf > images/$(basename $i ".fst").pdf
done
