print("hello")
round(x = 1.17, digits = 1)

my.vector <- c(1,3,5,7,9)
#View(my.vector)
my.vector[1]
my.vector[3:5]


my.matrix <- matrix(c(1,3,5,7,9,11), nrow=3, ncol=2)
my.matrix[2,1]

my.array <- array(seq(24),c(2,4,3))
my.array[1,4,2]  # last index is the 3rd dimension // number of layers


volcano
#?volcano
image(volcano)
image(volcano, col = terrain.colors(100))
contour(volcano, add = T)

x <- 1:nrow(volcano)
y <- 1:ncol(volcano)
persp(x,y,volcano,theta=110,phi=40)

library(rgl)
surface3d(x, y, 3*volcano, color = "grey")
play3d(spin3d(rpm=10), duration = 5)

movie3d(spin3d(),duration = 5, convert = F,
dir="Users/meraner/desktop/",movie="tstmov")

#3D data
a <- sort(rnorm(1000))
b <- rnorm(1000)
c <- rnorm(1000) + atan2(a,b)
open3d()
plot3d(a, b, c, col=rainbow(1000))

#Spheres
open3d()
rgl.spheres(rnorm(10),rnorm(10),rnorm(10),
radius=1,color=rainbow(10))








