plot(density(rep(0,1000)))
set.seed(10)
dat<-c(rgamma(300,shape = 2,scale = 2),rgamma(100,shape = 10,scale = 2))
plot(density(dat),ylim=c(0,0.2))
dfn<-function(x,a,alpha1,alpha2,theta){  
    a*dgamma(x,shape=alpha1,scale=theta)+(1-a)*dgamma(x,shape=alpha2,scale=theta)}  
pfn<-function(x,a,alpha1,alpha2,theta){  
    a*pgamma(x,shape=alpha1,scale=theta)+(1-a)*pgamma(x,shape=alpha2,scale=theta)}  
curve(dfn(x,0.75,2,10,2),add=T,col="red")  