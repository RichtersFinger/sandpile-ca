load 'colors.gnu'

set term pngcairo size 800, 800

set size ratio -1

unset tics; unset label; unset key; unset colorbox
set lmargin screen 0; set rmargin screen 1
set bmargin screen 0; set tmargin screen 1

set palette negative defined (0 newblue, 1.5 pastelblue, 2 verylightgray, 2.5 pastelred, 4 newred)


! mkdir -p res

n0 = 0
n1 = 3600

set autoscale xfix
set autoscale yfix
set cbr [0.4:1]

max(x,y) = x<y?y:x
min(x,y) = x>y?y:x
do for [i=n0:n1-1:1] {

	print i

	set output sprintf('res/plot%05d.png', i)

	pl sprintf('data_womomentum/momentum_%d.dat', i) matrix u 1:2:($1==0?1:$2==0?1:$1==99?1:$2==99?1:$3) w image

	unset output
}

#ffmpeg -framerate 60 -i res/plot%05d.png -c:v libx264 output.mp4