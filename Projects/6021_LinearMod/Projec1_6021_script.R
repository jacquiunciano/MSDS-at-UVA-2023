library(ggplot2)
library(dplyr)
library(MASS)
diamond = read.csv("C:\\Users\\jacqu\\Downloads\\diamonds4.csv", header=TRUE)
diamond$clarity = factor(diamond$clarity, levels=c("I1","I2","I3","SI1","SI2","VS1","VS2","VVS1","VVS2","IF","FL"))
diamond$color = factor(diamond$color, levels=c("D", "E", "F", "G", "H", "I", "J", "K"))
diamond$color2 = factor(diamond$color, levels=c("K", "J", "I", "H", "G", "F", "E", "D"))
diamond$cut = factor(diamond$cut, levels=c("Good", "Very Good", "Ideal", "Astor Ideal"))

ggplot(diamond, aes(x=carat, y=price/1000))+
  geom_point()+
  geom_smooth(method = "lm", se = FALSE)+
  theme_bw()+
  labs(title="Relationship Between The Carat Weight of Diamonds and the Price",
       x="Carat Weight",
       y="Price in Thousands (USD)",
       caption="Figure 1")+
  theme(plot.caption = element_text(hjust = 0, size=10, face="bold"),
        plot.title = element_text(hjust = 0.5))

ggplot(data = diamond) + 
  aes(y = log(price/1000), x=clarity, size=carat, fill=clarity)+ 
  geom_boxplot(alpha=0.8)+
  theme_bw()+
  labs(title='Log-Price of Diamonds by Clarity', 
       x="Level of Clarity",
       y='Log-Price in Thousands (USD)',
       caption="Figure 2.1")+
  guides(fill=FALSE)+
  theme(plot.caption = element_text(hjust = 0, size=10, face="bold"),
        plot.title = element_text(hjust = 0.5))

ggplot(diamond, aes(x=carat, y=price/1000, color=clarity))+
  geom_point()+
  geom_smooth(method = "lm", se = FALSE)+
  facet_wrap(~clarity)+
  theme_bw()+
  labs(title="Relationship Between The Carat Weight of Diamonds and the Price",
       subtitle="by Clarity Grade",
       x="Carat Weight",
       y="Price in Thousands (USD)",
       caption="Figure 2.2",
       color="Clarity Grade")+
  theme(plot.caption = element_text(hjust = 0, size=10, face="bold"),
        plot.title = element_text(hjust = 0.5),
        plot.subtitle = element_text(hjust = 0.5))

ggplot(data = diamond) + 
  aes(y = carat, x=clarity, size=price/1000, color=clarity)+ 
  geom_point(alpha=0.3) + 
  theme_bw()+
  labs(title='Relationship Between Carat Weight and Clarity Grade',
       x='Level Clarity',
       y='Carat Weight',
       caption="Figure 2.3",
       size="Price in Thousands (USD)")+
  guides(color=FALSE)+
  theme(plot.caption = element_text(hjust = 0, size=10, face="bold"),
        plot.title = element_text(hjust = 0.5))

ggplot(diamond, aes(x=clarity, fill= cut))+
  geom_bar(position='fill', color="black")+
  theme_bw()+
  labs(x="Level of Clarity", 
       y="Proportion of Cuts", 
       title="Proportion of Cuts Within Clarity Grades",
       caption="Figure 2.4",
       fill="Cut Grade")+
  theme(plot.caption = element_text(hjust = 0, size=10, face="bold"),
        plot.title = element_text(hjust = 0.5))

ggplot(diamond, aes(x=color2, y=log(price/1000), fill=color2))+
  geom_boxplot()+
  theme_bw()+
  guides(fill=FALSE)+
  labs(title="Log-Price of Diamonds by Color Grade",
       x="Color Grade",
       y="Log-Price in Thousands (USD)",
       caption="Figure 3.1")+
  theme(plot.caption = element_text(hjust = 0, size=10, face="bold"),
        plot.title = element_text(hjust = 0.5))

ggplot(diamond, aes(x=carat, y=price/1000, color=color2))+
  geom_point()+
  geom_smooth(method = "lm", se = FALSE)+
  facet_wrap(~color2)+
  theme_bw()+
  labs(title="Relationship Between The Carat Weight of Diamonds and the Price",
       subtitle="by Color Grade",
       x="Carat Weight",
       y="Price in Thousands (USD)",
       caption="Figure 3.2",
       color="Color Grade")+
  theme(plot.caption = element_text(hjust = 0, size=10, face="bold"),
        plot.title = element_text(hjust = 0.5),
        plot.subtitle = element_text(hjust = 0.5))

ggplot(data = diamond) + 
  aes(y = carat, x=color2, size=price/1000, color=color2)+ 
  geom_point(alpha=0.3) + 
  theme_bw()+
  labs(title='Relationship Between Carat Weight and Color Grade',
       x='Color Grade',
       y='Carat Weight',
       caption="Figure 3.3",
       size="Price in Thousands (USD)")+
  guides(color=FALSE)+
  theme(plot.caption = element_text(hjust = 0, size=10, face="bold"),
        plot.title = element_text(hjust = 0.5))

ggplot(diamond, aes(x=color2, fill= cut))+
  geom_bar(position='fill', color="black")+
  theme_bw()+
  labs(x="Color Grade", 
       y="Proportion of Cuts", 
       title="Proportion of Cuts Within Color Grades",
       caption="Figure 3.4",
       fill="Cut Grade")+
  theme(plot.caption = element_text(hjust = 0, size=10, face="bold"),
        plot.title = element_text(hjust = 0.5))

log_price<- log(diamond$price) #restores symmetry to data and reduces skewness
ggplot(diamond, aes(x=cut, y=log_price, fill=cut)) +
  geom_boxplot()+
  theme_bw()+
  guides(fill=FALSE)+
  labs(x="Cut Type", 
       y="Log-Price in Thousands (USD)", 
       title="Boxplot Representing Log-Price vs Cut of Blue Nile Diamonds",
       caption="Figure 4.1")+
  theme(plot.title = element_text(hjust = 0.5),
        plot.caption = element_text(hjust = 0, size=10, face="bold")) #centering title

ggplot(diamond, aes(x=carat, y=price/1000, color=cut))+
  geom_point()+
  geom_smooth(method = "lm", se = FALSE)+
  facet_wrap(~cut)+
  theme_bw()+
  labs(title="Relationship Between The Carat Weight of Diamonds and the Price",
       subtitle="by Cut Grade",
       x="Carat Weight",
       y="Price in Thousands (USD)",
       caption="Figure 4.2",
       color="Cut Grade")+
  theme(plot.caption = element_text(hjust = 0, size=10, face="bold"),
        plot.title = element_text(hjust = 0.5),
        plot.subtitle = element_text(hjust = 0.5))

ggplot(diamond, aes(x=cut, fill=color))+
  geom_bar(position="fill", color="black")+
  theme_bw()+
  labs(y="Proportion",
       x="Cut Grade",
       title="Proportion of Color Grade Diamonds Within Cut Grade",
       caption="Figure 4.3",
       fill="Color Grade")+
  theme(plot.caption = element_text(hjust = 0, size=10, face="bold"),
        plot.title = element_text(hjust = 0.5))

result<-lm(price~carat, data=diamond)
par(mfrow = c(2, 2))
plot(result)
mtext("Figure 5.1", side = 3, line = -1.5, outer = TRUE)

MASS::boxcox(result, lambda = seq(0, 0.5, 1/100))
mtext("Figure 5.2", side = 3, line = -3.5, outer = TRUE)

ystar<-log(diamond$price)
Data<-data.frame(diamond,ystar)
result.ystar<-lm(ystar~carat, data=diamond)
par(mfrow = c(2, 2))
plot(result.ystar)
mtext("Figure 5.3", side = 3, line = -1.5, outer = TRUE)

ggplot(diamond, aes(x=carat, y=ystar))+
  geom_point()+
  geom_smooth(method = "lm", se = FALSE)+
  theme_bw()+
  labs(title="Relationship Between The Carat Weight of Diamonds and the Log-Price",
       x="Carat Weight",
       y="Log-Price in Thousands (USD)",
       caption="Figure 5.4")+
  theme(plot.caption = element_text(hjust = 0, size=10, face="bold"),
        plot.title = element_text(hjust = 0.5))

xstar<-log(Data$carat)
Data<-data.frame(Data,xstar)
result.xstar<-lm(ystar~xstar, data=Data)
par(mfrow = c(2, 2))
plot(result.xstar)
mtext("Figure 5.5", side = 3, line = -1.5, outer = TRUE)

ggplot(Data, aes(x=xstar, y=ystar))+
  geom_point()+
  geom_smooth(method = "lm", se = FALSE)+
  theme_bw()+
  labs(title="Relationship Between The Log-Carat Weight of Diamonds and the Log-Price",
       x="Log-Carat Weight",
       y="Log-Price in Thousands (USD)",
       caption="Figure 5.6")+
  theme(plot.caption = element_text(hjust = 0, size=10, face="bold"),
        plot.title = element_text(hjust = 0.5))





