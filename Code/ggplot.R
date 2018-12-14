library(ggplot2)
library(reshape2)
library(grid)
library(gtable)

G_source <- read.csv('Giving by Source.csv')
G_source2 <- read.csv('Giving by Source (inflation-adjusted).csv')

test <- data.frame(Year = G_source$Year, 'Actual' = G_source$Total, 
                   'Inflation-adjusted' = G_source2$Total)
test <- melt(test, id = c("Year"))

p <- ggplot(test, aes(x = Year))
p +
  annotate("rect", xmin=2007, xmax=2009, ymin=-Inf, ymax=Inf, alpha=0.1, fill="black")  +
  geom_line(aes(y = value, colour = variable), size = 2) +
  ylab("Giving in Billions of Dollars") +
  ggtitle("Annual Giving by Source in Billions of Dollars (Inflation-Adjusted Based on CPI), 1977-2017") +
  theme(plot.title = element_text(size = 18, hjust = 0.5),
        strip.text.x = element_text(size = 14, colour = "Brown")) +
  scale_x_continuous(breaks = seq(1978,2016,2)) +
  scale_colour_manual(name = 'Measure', labels = c("Actual", "Inflation Adjusted"),
                      values =c('Actual'='steelblue','Inflation.adjusted'='orange'))


test <- melt(subset(G_source, select = -c(2, 3, 5, 7, 9, 11)), id=c("Year"))

p <- ggplot(test, aes(x = Year, y = value, group = 1))
p + 
  geom_point(colour="steelblue", size = 2, alpha=0.7) +
  geom_smooth(method = "lm", formula = y ~ poly(x, 2), se = FALSE, colour = 'orange') +
  facet_wrap(~variable, ncol = 5) +
  ylab("Giving in Billions of Dollars") +
  ggtitle("Annual Giving by Source in Billions of Dollars, 1977-2017") +
  theme(plot.title = element_text(size = 20, hjust = 0.5),
        strip.text.x = element_text(size = 14, colour = "Brown")) +
  scale_x_continuous(
    breaks = seq(1980, 2015, 5)
  )

test <- melt(subset(G_source2, select = -c(2, 3, 5, 7, 9, 11)), id=c("Year"))

p <- ggplot(test, aes(x = Year, y = value, group = 1))
p + 
  geom_point(colour="steelblue", size = 2, alpha=0.7) +
  geom_smooth(method = "lm", formula = y ~ poly(x, 2), se = FALSE, colour = 'orange') +
  facet_wrap(~variable, ncol = 5) +
  ylab("Giving in Billions of Dollars") +
  ggtitle("Annual Giving by Source in Billions of Dollars (Inflation-Adjusted Based on CPI), 1977-2017") +
  theme(plot.title = element_text(size = 20, hjust = 0.5),
        strip.text.x = element_text(size = 14, colour = "Brown")) +
  scale_x_continuous(
    breaks = seq(1980, 2015, 5)
  )

OrgCount <- read.csv('Number Org.csv')
test <- melt(OrgCount, id=c("Year"))

p <- ggplot(test, aes(x = Year))
p +
  geom_bar(aes(y = value/100000, fill = variable), stat="identity")+
  annotate("rect", xmin=2010, xmax=2013, ymin=-Inf, ymax=Inf, alpha=0.1, fill="black")  +
  ylab("Number in Millions") +
  ggtitle("Number of Registered U.S. Nonprofits in Millions, 1991-2017") +
  theme(plot.title = element_text(size = 18, hjust = 0.5),
        strip.text.x = element_text(size = 14, colour = "Brown")) +
  scale_x_continuous(breaks = seq(1990,2015,5)) +
  scale_fill_manual(name = 'Tax Exempt Status', labels = levels(test$variable),
                      values =c('Tax.Exempt.Organizations'='orange','Nonexempt.charitable.trusts'='steelblue'))


