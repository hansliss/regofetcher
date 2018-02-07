set term png size 1600, 1200 font "arial,14"
set loadpath "."
set style line 1 lc rgb "#EEEEEE" lw 0.2
set style line 2 lc rgb "#CCCCCC" lw 0.5
set style line 3 lc rgb "#223355" lw 0.5
set style line 5 lt 1 lc rgb "dark-red"
set style line 6 lt 1 lc rgb "dark-blue"
set style line 7 lt 1 lc rgb "dark-green"
set output "#PATH#/regoVals_#PERIOD#.png"
set xdata time
set timefmt "%Y-%m-%dT%H:%M:%S"
set autoscale xfixmax
set ytics nomirror
set autoscale yfixmin
set autoscale yfixmax
set y2tics nomirror
set autoscale y2fixmin
set autoscale y2fixmax
set yrange [* < 0:]
#set y2range [* < 0:]
#set grid ytics ls 2
set datafile separator ","
set datafile missing 'nan'
set grid xtics mxtics ls 1,ls 2

set multiplot
set lmargin 10
set rmargin 10
set bmargin 0

set title "Heat pump data for #PERIOD#"
set format x ""
set size 1,0.7
set origin 0.0,0.3
set ylabel "Power Consumption"
set y2label "Power Consumption"
plot "#PATH#/regoVals_#PERIOD#.csv" using 13:26 with lines ls 5 axes x1y1 title "Power"

set bmargin 5
set tmargin 0
unset title
set format x "%d\n%H:%M"
set mxtics
set xlabel "Date/time"
set size 1,0.3
set origin 0.0,0.0
set ylabel "Outdoor Temperature"
set y2label "Room Temperature"
plot "#PATH#/regoVals_#PERIOD#.csv" using 13:109 with lines ls 7 axes x1y1 title "Outdoor temp", "#PATH#/regoVals_#PERIOD#.csv" using 13:62 with lines ls 6 axes x1y2 title "Room temp"
