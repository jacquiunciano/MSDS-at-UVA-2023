# setwd("C:\\Users\\Jacqueline\\OneDrive\\Documents\\MSDS")
setwd("C:\\Users\\jacqu\\OneDrive\\Documents\\MSDS")
data = read.csv("datasets\\kc_house_data.csv")
#stepwise
library(dplyr)
data = data %>%
  select(-c(id,date))
fullmod = lm(price~., data=data)
nullmod = lm(price~1, data=data)
step(nullmod, scope=list(lower=nullmod, upper=fullmod), direction="both")
stepmod = lm(formula = price ~ sqft_living + view + grade + yr_built + 
               waterfront + bedrooms + bathrooms + zipcode +  condition + 
               sqft_above + sqft_living15 + yr_renovated + sqft_lot15 + 
               sqft_lot + floors, data = data)
## consider taking off lat/long, use zipcode for neighborhood/location

## Creating the "Wealthy" variable - indicating whether a house belongs to one of the twenty richest zip codes.
data <- data %>% 
  mutate(wealthy=ifelse(zipcode %in% c(98072, 98027, 98119, 98029, 98052, 98005, 98177, 98065, 98105, 
                                       98199, 98006, 98121, 98053, 98074, 98033, 98075, 98112, 98004, 
                                       98040, 98039), TRUE, FALSE))

## regrouped grade levels
data = data %>%
  mutate(grade_group = ifelse(grade %in% list("1", "2", "3"), "poor",
                              ifelse(grade %in% list("4", "5", "6"), "mod_poor",
                                     ifelse(grade %in% list("7", "8", "9", "10"), "average", "high"))))
data$grade_group = factor(data$grade_group, 
                           c("poor", "mod_poor", "average", "high"))

## refactor categorical variables
data$view = factor(data$view)
data$waterfront = factor(data$waterfront)
data$grade = factor(data$grade)
data$floors = factor(data$floors)
data$condition = factor(data$condition)

## making binary variable for zipcode
unique(data$zipcode)

# Check multicollinearity
library(faraway)
vif(stepmod)

# took out sqft_above which decreased the vif for sqft_living 
# sqft_basement was already removed in stepwise regression
stepmod2 = lm(formula = price ~ sqft_living + view + grade + yr_built + 
                waterfront + bedrooms + bathrooms + zipcode +  condition + 
                sqft_living15 + yr_renovated + sqft_lot15 + 
                sqft_lot + floors, data = data)
vif(stepmod2)

## Visualizations
library(ggplot2)
library(gridExtra)
library(MASS)

## sqft_living
v1 = ggplot(data=data)+
  geom_point(aes(x=sqft_living, y=price),
             color="#16537e",
             alpha=0.5)+
  theme_bw()

## view
v2 = ggplot(data=data)+
  geom_density(aes(x=price_log, fill=view),
               alpha=0.5)+
  facet_wrap(~view, nrow = 1)+
  theme_bw()+
  guides(fill=FALSE)

## grade
v3 = ggplot(data=data)+
  geom_boxplot(aes(x=grade, y=price_log),
               alpha=0.5,
               fill=c("#e06666", "#ffd966", "#93c47d", "#76a5af", "#8e7cc3", 
                      "#a64d79", "#0f2b3c", "#ce7e00", "#660000", "#274e13",
                      "#19cea6", "#6005ac"))+
  theme_bw()
gridExtra::grid.arrange(v1,v2, ncol=1, nrow=2)
v3

v1_2 = MASS::boxcox(lm(price~sqft_living, data=data), lambda=seq(-0.05,0.05,0.01))
data$price_log = log(data$price)
v1_3 = ggplot(data=data)+
  geom_point(aes(x=sqft_living, y=price_log),
             color="#16537e",
             alpha=0.5)+
  theme_bw()
data$sqft_living_log = log(data$sqft_living)
v1_4 = ggplot(data=data)+
  geom_point(aes(x=sqft_living_log, y=price_log),
             color="#16537e",
             alpha=0.5)+
  theme_bw()
gridExtra::grid.arrange(v1_3,v1_4, nrow=1)
par(mfrow=c(2,2))
plot(lm(price_log~sqft_living_log, data=data))

# Sqft_lot
lot = ggplot(data=data, aes(x=sqft_lot, y=log(price)))+
  geom_point(color="#16537e")+
  geom_smooth(method='lm', se=FALSE, color="#a04936")+
  theme_bw()+
  labs(x="Sq. Ft. Lot", y="log(Price)", title="Price per Sq. Ft. of Lot")

# Sqft_living15
living15 = ggplot(data=data, aes(x=sqft_living15, y=log(price)))+
  geom_point(color="#16537e")+
  geom_smooth(method='lm', se=FALSE, color="#a04936")+
  theme_bw()+
  labs(x="Sq. Ft. Living of 15 Neighbors", y="log(Price)", title="Price per Sq. Ft. of 15 Neighbors")

# Sqft_lot 15
lot15 = ggplot(data=data, aes(x=sqft_lot15, y=log(price)))+
  geom_point(color="#16537e")+
  geom_smooth(method='lm', se=FALSE, color="#a04936")+
  theme_bw()+
  labs(x="Sq. Ft. Lot of 15 Neighbors", y="log(Price)", title="Price per Sq. Ft. of Lot of 15 Neighbors")

# Floors
floors = ggplot(data=data, aes(x=log(price), color=floors))+
  geom_density()+
  theme_bw()+
  labs(x="log(Price)", y="Density", title="Num. of Floors by Price")

gridExtra::grid.arrange(lot,living15,lot15,floors, ncol=2, nrow=2)

# Waterfront
data$waterfront = factor(data$waterfront)
boxplot(price~interaction(waterfront, lex.order=T), data)

# Yr_built 

data <- data %>%
  mutate(decade = if_else(yr_built >= 2000,
                          paste0(yr_built  %/% 10 * 10, "'s"),
                          paste0((yr_built - 1900) %/% 10 * 10, "'s")))

data %>% 
  mutate(decade=fct_relevel(decade,
                            "10's", "20's", "30's", "40's", "50's", "60's", 
                            "70's", "80's", "90's", "0's", "2010's")) %>% 
  ggplot(aes(as.factor(decade), y=price)) +
  geom_boxplot() + 
  labs(x="Decade Built", y="Price")

# Bedrooms

ggplot(data, aes(as.factor(bedrooms), y=price)) +
  geom_boxplot() + 
  labs(x="Number of Bedrooms", y="Price")

# Bathrooms

ggplot(data, aes(as.factor(bathrooms), y=price)) +
  geom_boxplot() + 
  labs(x="Number of Bathrooms", y="Price")


# LINEAR REGRESSION MODEL
# Fitting the model
model <- lm(price ~ sqft_living + bedrooms + floors + bathrooms, data = data)

# Summarize the model to get the coefficients and other details
summary(model)

# LOGISTIC REGRESSION MODEL
## wealthy~bedrooms+bathrooms+sqft_living+sqft_lot+floors+condition+grade_group+
## sqft_living15+sqft_lot15
finmod = data %>%
  dplyr::select(bedrooms, bathrooms, sqft_living, sqft_lot, floors, condition, 
                grade_group, sqft_living15, sqft_lot15, wealthy)
finmod = finmod[complete.cases(finmod[ , 10]),]
##80-20 split
set.seed(6021)
samp = sample.int(nrow(finmod), floor(.80*nrow(finmod)), replace = F)
train = finmod[samp, ]
test = finmod[-samp, ]

## logisitic visualizations
vlog1 = ggplot(train)+
  geom_bar(aes(x=as.factor(bedrooms), fill=wealthy),
           position="fill")+
  theme_bw()+
  labs(title="Proportion of Houses within Zipcode Catoegory",
       subtitle = "by Number of Bedrooms",
       x="Number of Bedrooms",
       y="Proportion",
       caption="Figure 6.1",
       fill="Zipcode Category")+
  scale_fill_manual(labels=c('Non-Wealthy \nZipcode', 'Wealthy Zipcode'),
                    values=c("#e06666","#ffd966"))+
  theme(plot.caption = element_text(hjust = 0, size=8, face="bold"),
        plot.title = element_text(hjust = 0.5, size=10),
        plot.subtitle = element_text(hjust = 0.5, size=8))

vlog2 = ggplot(train)+
  geom_bar(aes(x=as.factor(bathrooms), fill=wealthy),
           position="fill")+
  theme_bw()+
  labs(title="Proportion of Houses within Zipcode Catoegory",
       subtitle = "by Number of Bathrooms",
       x="Number of Bathrooms",
       y="Proportion",
       caption="Figure 6.2")+
  guides(fill="none")+
  scale_fill_manual(values=c("#e06666","#ffd966"))+
  theme(plot.caption = element_text(hjust = 0, size=8, face="bold"),
        plot.title = element_text(hjust = 0.5, size=10),
        plot.subtitle = element_text(hjust = 0.5, size=8))

vlog3 = ggplot(train)+
  geom_density(aes(x=log(sqft_living), fill=wealthy), alpha=0.5)+
  theme_bw()+
  labs(title="Relationship Between The Area of \nthe House within Zipcode Catoegory",
       x="Log of Square-ft Living Space",
       y="Density",
       caption="Figure 6.3")+
  guides(fill="none")+
  scale_fill_manual(values=c("#e06666","#ffd966"))+
  theme(plot.caption = element_text(hjust = 0, size=8, face="bold"),
        plot.title = element_text(hjust = 0.5, size=8))

vlog4 = ggplot(train)+
  geom_density(aes(x=log(sqft_lot), fill=wealthy), alpha=0.5)+
  theme_bw()+
  labs(title="Relationship Between The Area of \nthe Property within Zipcode Catoegory",
       x="Log of Square-ft Property",
       y="Density",
       caption="Figure 6.4",
       fill="Zipcode Category")+
  scale_fill_manual(labels=c('Non-Wealthy \nZipcode', 'Wealthy Zipcode'),
                    values=c("#e06666","#ffd966"))+
  theme(plot.caption = element_text(hjust = 0, size=8, face="bold"),
        plot.title = element_text(hjust = 0.5, size=8))

vlog5 = ggplot(train)+
  geom_bar(aes(x=as.factor(condition), fill=wealthy),
           position="fill")+
  theme_bw()+
  labs(title="Proportion of Houses within Zipcode Catoegory",
       subtitle = "by Condition Level",
       x="Condition Level",
       y="Proportion",
       caption="Figure 6.6")+
  guides(fill="none")+
  scale_fill_manual(values=c("#e06666","#ffd966"))+
  theme(plot.caption = element_text(hjust = 0, size=8, face="bold"),
        plot.title = element_text(hjust = 0.5, size=10),
        plot.subtitle = element_text(hjust = 0.5, size=8))

vlog6 = ggplot(train)+
  geom_bar(aes(x=as.factor(grade_group), fill=wealthy),
           position="fill")+
  theme_bw()+
  labs(title="Proportion of Houses within Zipcode Catoegory",
       subtitle = "by Grade Level",
       x="Grade Level",
       y="Proportion",
       caption="Figure 6.7")+
  guides(fill="none")+
  scale_fill_manual(values=c("#e06666","#ffd966"))+
  theme(plot.caption = element_text(hjust = 0, size=8, face="bold"),
        plot.title = element_text(hjust = 0.5, size=10),
        plot.subtitle = element_text(hjust = 0.5, size=8))

vlog7 = ggplot(train)+
  geom_density(aes(x=log(sqft_living15), fill=wealthy), alpha=0.5)+
  theme_bw()+
  labs(title="Relationship Between The Area of the 15 \nNearest Neighboring Houses within Zipcode Catoegory",
       x="Log of Square-ft Living Space",
       y="Density",
       caption="Figure 6.8",
       fill="Zipcode Category")+
  scale_fill_manual(labels=c('Non-Wealthy \nZipcode', 'Wealthy Zipcode'),
                    values=c("#e06666","#ffd966"))+
  theme(plot.caption = element_text(hjust = 0, size=8, face="bold"),
        plot.title = element_text(hjust = 0.5, size=8))

vlog8 = ggplot(train)+
  geom_density(aes(x=log(sqft_lot15), fill=wealthy), alpha=0.5)+
  theme_bw()+
  labs(title="Relationship Between The Area of the 15 \nNearest Neighboring Properties within Zipcode Catoegory",
       x="Log of Square-ft Property",
       y="Density",
       caption="Figure 6.9")+
  guides(fill="none")+
  scale_fill_manual(values=c("#e06666","#ffd966"))+
  theme(plot.caption = element_text(hjust = 0, size=8, face="bold"),
        plot.title = element_text(hjust = 0.5, size=8))

vlog9 = ggplot(train)+
  geom_bar(aes(x=as.factor(floors), fill=wealthy),
           position="fill")+
  theme_bw()+
  labs(title="Proportion of Houses within Zipcode Catoegory",
       subtitle = "by Number of Floors",
       x="Number of Floors",
       y="Proportion",
       caption="Figure 6.5")+
  guides(fill="none")+
  scale_fill_manual(values=c("#e06666","#ffd966"))+
  theme(plot.caption = element_text(hjust = 0, size=8, face="bold"),
        plot.title = element_text(hjust = 0.5, size=10),
        plot.subtitle = element_text(hjust = 0.5, size=8))

gridExtra::grid.arrange(vlog1,vlog2, ncol=1, nrow=2)
gridExtra::grid.arrange(vlog3,vlog4,vlog9,vlog5, ncol=2, nrow=2)
gridExtra::grid.arrange(vlog6,vlog7,vlog8, ncol=2, nrow=2)

noprice = glm(wealthy~., family="binomial", data=train)
summary(noprice)

## testing to see of current mod is useful over intercept model
gstat3 = noprice$null.deviance-noprice$deviance
1-pchisq(gstat3, 15)
## pval: 0 ==> this model is useful and should be chosen over an intercept model

## testing beta(sqft_lot, condition, sqft_lot15)
eda = glm(wealthy~bedrooms+bathrooms+sqft_living+grade_group+floors+
            sqft_living15,
          family="binomial", data=train)
gstat4 = noprice$deviance-eda$deviance
1-pchisq(gstat4, 6)
## pval: 1 ==> we can drop betas

summary(eda)

## testing model with ROC and AUC
p_eda=predict(eda, newdata=test, type="response")
r_eda=ROCR::prediction(p_eda, test$wealthy)
roc_eda=ROCR::performance(r_eda, measure="tpr", x.measure="fpr")
plot(roc_eda, main="ROC Curve for Reduced Model")
lines(x = c(0,1), y = c(0,1), col="red")

auc_eda=ROCR::performance(r_eda, measure = "auc")
auc_eda@y.values

## testing beta(floor, condition, grade)
cate = glm(wealthy~bedrooms+bathrooms+sqft_living+sqft_lot+
             sqft_living15+sqft_lot15,
           family="binomial", data=train)
gstat5 = noprice$deviance-cate$deviance
1-pchisq(gstat5, 12)
## pval: 1 ==> we can drop betas

summary(cate)

## testing model with ROC and AUC
p_cate=predict(cate, newdata=test, type="response")
r_cate=ROCR::prediction(p_cate, test$wealthy)
roc_cate=ROCR::performance(r_cate, measure="tpr", x.measure="fpr")
plot(roc_cate, main="ROC Curve for Reduced Model",
     sub="Figure 7.1", font.sub =2)
lines(x = c(0,1), y = c(0,1), col="red")

auc_cate=ROCR::performance(r_cate, measure = "auc")
auc_cate@y.values

sort(faraway::vif(eda))
sort(faraway::vif(cate))

cmatrix = table(test$wealthy, p_cate>0.5)
cmatrix
TN = cmatrix[1,1]
TP = cmatrix[2,2]
FN = cmatrix[1,2]
FP = cmatrix[2,1]
n=dim(test)[1]
n

## error rate
(FP+FN)/n
## accuracy
(TN+TP)/n
## false positive rate
FP/(FP+TN)
## false negative rate
FN/(FN+TP)
## sensitivity
TP/(TP+FN)
## specificity
TN/(TN+FP)
## precision
TP/(TP+FP)












































