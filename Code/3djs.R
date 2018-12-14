library(threejs)
library(htmlwidgets)

dt <- read.csv('STATE_stats.csv')
MyJ3=scatterplot3js(dt$ASSET_AMT/1000000000,dt$INCOME_AMT/1000000000,dt$REVENUE_AMT/1000000000,
                    color = c("orange", "pink", "steelblue")[as.factor(dt$REGION)],
                    main = 'Relationship between Financial Perforamnce Indicators in Billion Dollars',
                    axisLabels=c("Asset","Income","Revenue"))
saveWidget(MyJ3, file="3D_finance.html", selfcontained = TRUE, libdir=NULL, background = "white")
