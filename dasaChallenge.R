library(readr)
library(ggplot2)
library(data.table)


# Read the Data ----------------------------------------------------------------

raw_data <- fread("PS_20174392719_1491204439457_log.csv", nThread = 4)

#ggplot(data = raw_data, mapping = aes(x = amount)) + geom_freqpoly(colour = 'isFraud', binwidth = 10)

raw_data$isFraud <- as.factor(raw_data$isFraud)
summary(raw_data$isFraud)

# Making separate DataFrames for Frauds and Non Frauds
filterFraud <- raw_data[isFraud == 1,]
filterNotFraud <- raw_data[isFraud == 0,]


# Feature Engineering ----------------------------------------------------------------

# Checking whether same accounts are used as Fraud Destinations
fraudNameDest <- filterFraud[, .N, by='nameDest'] #NO

# Merging the suspicious fraud accounts with the nonFraud transactions
result = merge(fraudNameDest, filterNotFraud, by = 'nameDest', all = F)

# Here we see that there are a lot of genuine transactions done by the accounts in fraud. 
# So we can safely say that a feature cannot be engineered using the nameOrig and nameDest columns 
# and  they can be dropped for modelling purposes.

hist(filterFraud$amount)
hist(filterNotFraud$amount)

# Here we see that NonFraud transactions are generally smaller compared to Fraudulent transactions.
# Amount can be a good variable which can be used in the model. Amount variable is higly skewed.
# If we are using a linear classifier, we would need to do a transformation of this feature. 
# If we are using a tree based classifier, it is more robust to outliers and skewed distributions.