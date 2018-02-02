set term png size 1600, 1200 font "arial,14"
set loadpath "."
set style line 1 lc rgb "#EEEEEE" lw 0.2
set style line 2 lc rgb "#CCCCCC" lw 0.5
set style line 3 lc rgb "#223355" lw 0.5
set style line 5 lt 1 lc rgb "dark-red"
set style line 7 lt 1 lc rgb "dark-green"
set output "#PATH#/regoVals_#PERIOD#.png"
set xdata time
set timefmt "%Y-%m-%dT%H:%M:%S"
set autoscale xfixmax
set ytics nomirror
set ytics nomirror
set autoscale yfixmin
set autoscale yfixmax
set yrange [* < 0:]
set grid ytics ls 2
set datafile separator ","
set datafile missing 'nan'
set grid xtics mxtics ls 1,ls 2

set multiplot

set title "Heat pump data for #PERIOD#"
set format x ""
set size 1,0.7
set origin 0.0,0.3
set ylabel "Power Consumption"
plot "#PATH#/regoVals_#PERIOD#.csv" using 1:13 with lines ls 5 axes x1y1 title "Power"

unset title
set format x "%d\n%H:%M"
set mxtics
set xlabel "Date/time"
set size 1,0.3
set origin 0.0,0.0
set ylabel "Outdoor Temperature"
plot "#PATH#/regoVals_#PERIOD#.csv" using 1:26 with lines ls 7 axes x1y2 title "Outdoor temp"


