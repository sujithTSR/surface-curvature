import pylab
import scipy
from mpl_toolkits.mplot3d import Axes3D
import scipy.ndimage as nd
import numpy as np
def surface_curvature(X,Y,Z):

	(lr,lb)=X.shape

	print(lr)
	#print("awfshss-------------")
	print(lb)
#First Derivatives
	Xv,Xu=np.gradient(X)
	Yv,Yu=np.gradient(Y)
	Zv,Zu=np.gradient(Z)
#	print(Xu)

#Second Derivatives
	Xuv,Xuu=np.gradient(Xu)
	Yuv,Yuu=np.gradient(Yu)
	Zuv,Zuu=np.gradient(Zu)   

	Xvv,Xuv=np.gradient(Xv)
	Yvv,Yuv=np.gradient(Yv)
	Zvv,Zuv=np.gradient(Zv) 

#2D to 1D conversion 
#Reshape to 1D vectors
	Xu=np.reshape(Xu,lr*lb)
	Yu=np.reshape(Yu,lr*lb)
	Zu=np.reshape(Zu,lr*lb)
	Xv=np.reshape(Xv,lr*lb)
	Yv=np.reshape(Yv,lr*lb)
	Zv=np.reshape(Zv,lr*lb)
	Xuu=np.reshape(Xuu,lr*lb)
	Yuu=np.reshape(Yuu,lr*lb)
	Zuu=np.reshape(Zuu,lr*lb)
	Xuv=np.reshape(Xuv,lr*lb)
	Yuv=np.reshape(Yuv,lr*lb)
	Zuv=np.reshape(Zuv,lr*lb)
	Xvv=np.reshape(Xvv,lr*lb)
	Yvv=np.reshape(Yvv,lr*lb)
	Zvv=np.reshape(Zvv,lr*lb)

	Xu=np.c_[Xu, Yu, Zu]
	Xv=np.c_[Xv, Yv, Zv]
	Xuu=np.c_[Xuu, Yuu, Zuu]
	Xuv=np.c_[Xuv, Yuv, Zuv]
	Xvv=np.c_[Xvv, Yvv, Zvv]

#% First fundamental Coeffecients of the surface (E,F,G)
	
	E=np.einsum('ij,ij->i', Xu, Xu) 
	F=np.einsum('ij,ij->i', Xu, Xv) 
	G=np.einsum('ij,ij->i', Xv, Xv) 

	m=np.cross(Xu,Xv,axisa=1, axisb=1) 
	p=np.sqrt(np.einsum('ij,ij->i', m, m)) 
	n=m/np.c_[p,p,p]
# n is the normal
#% Second fundamental Coeffecients of the surface (L,M,N), (e,f,g)
	L= np.einsum('ij,ij->i', Xuu, n) #e
	M= np.einsum('ij,ij->i', Xuv, n) #f
	N= np.einsum('ij,ij->i', Xvv, n) #g

# Alternative formula for gaussian curvature in wiki 
# K = det(second fundamental) / det(first fundamental)
#% Gaussian Curvature
	K=(L*N-M**2)/(E*G-F**2)
	K=np.reshape(K,lr*lb)
#	print(K.size)
#wiki trace of (second fundamental)(first fundamental inverse)
#% Mean Curvature
	H = ((E*N + G*L - 2*F*M)/((E*G - F**2)))/2
	print(H.shape)
	H = np.reshape(H,lr*lb)
#	print(H.size)

#% Principle Curvatures
	Pmax = H + np.sqrt(H**2 - K)
	Pmin = H - np.sqrt(H**2 - K)
#[Pmax, Pmin]
	Principle = [Pmax,Pmin]
	return Principle


def fun(x,y):
	return x**2+y**2
x = scipy.linspace(-1,1,20)
y = scipy.linspace(-1,1,20)
[x,y]=scipy.meshgrid(x,y)

z = (x**3 +y**2 +x*y)
#s = nd.gaussian_filter(z,10)
temp1 = surface_curvature(x,y,z)
print("maximum curvatures")
print(temp1[0])
print("minimum curvatures")
print(temp1[1])
fig = pylab.figure()
ax = Axes3D(fig)

ax.plot_surface(x,y,z)
pylab.show()
