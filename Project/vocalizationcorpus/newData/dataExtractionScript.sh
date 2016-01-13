for f in *.wav ; do
	SMILExtract -C /Users/callumc/Downloads/openSMILE-2.2rc1/config/gemaps/GeMAPSv01a.conf -I $f -O extraction/$f.csv
done