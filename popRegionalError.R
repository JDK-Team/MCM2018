setwd("~/PycharmProjects/MCM2018")

error1 <- read.csv('popRegionalError_1.csv', header=TRUE)
means = c(1:ncol(error1))
for(col in 2:ncol(error1)){
  means[col-1] <- sd(abs(error1[,col]))
}
print(means)