# code on my Macbook Pro
setwd("/Users/wxc575843/Desktop/code/GoWhere/data/")
# code on On My PC
# setwd("")
data<-read.csv("full_text.csv",header = F)
data<-data[,1:6]
names(data)<-c("userId","time","location","lati","long","tweets")
out_data<-data[data$lati<42&data$lati>38&data$long>-76&data$long< -72,]
write.csv(out_data,"data_NewYork.csv")
