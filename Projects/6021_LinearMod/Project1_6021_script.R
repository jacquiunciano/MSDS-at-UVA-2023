data = read.csv("C:\\Users\\jacqu\\OneDrive\\Documents\\MSDS\\datasets\\kc_house_data.csv")

#stepwise
library(dplyr)
data = data %>%
  select(c(-1,-2))
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
  mutate(wealthy=ifelse(zipcode %in% c(98072, 98027, 98119, 98029, 98052, 98005, 98177, 98065, 98105, 98199, 98006, 98121, 98053, 98074, 98033, 98075, 98112, 98004, 98040, 98039), TRUE, FALSE))

## refactor categorical variables
data$view = factor(data$view)
data$waterfront = factor(data$waterfront)
data$grade = factor(data$grade)
data$floors = factor(data$floors)

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
  geom_density(aes(x=price, fill=view),
               alpha=0.5)+
  facet_wrap(~view, nrow = 1)+
  theme_bw()+
  guides(fill=FALSE)

## grade
v3 = ggplot(data=data)+
  geom_boxplot(aes(x=grade, y=price),
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
  geom_smooth(method='lm', se=FALSE)+
  theme_bw()+
  labs(x="Sq. Ft. Lot", y="log(Price)", title="Price per Sq. Ft. of Lot")

# Sqft_living15
living15 = ggplot(data=data, aes(x=sqft_living15, y=log(price)))+
  geom_point(color="#16537e")+
  geom_smooth(method='lm', se=FALSE)+
  theme_bw()+
  labs(x="Sq. Ft. Living of 15 Neighbors", y="log(Price)", title="Price per Sq. Ft. of 15 Neighbors")

# Sqft_lot 15
lot15 = ggplot(data=data, aes(x=sqft_lot15, y=log(price)))+
  geom_point(color="#16537e")+
  geom_smooth(method='lm', se=FALSE)+
  theme_bw()+
  labs(x="Sq. Ft. Lot of 15 Neighbors", y="log(Price)", title="Price per Sq. Ft. of Lot of 15 Neighbors")

# Floors
floors = ggplot(data=data, aes(x=log(price), color=floors))+
  geom_density()+
  theme_bw()+
  labs(x="log(Price)", y="Density", title="Num. of Floors by Price")

gridExtra::grid.arrange(lot,living15,lot15,floors, ncol=2, nrow=2)

## waterfront
data$waterfront = factor(data$waterfront)
boxplot(price~interaction(waterfront, lex.order=T), data)