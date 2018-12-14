library(plotly)
library(htmlwidgets)

dt <- read.csv('ntee_1.csv')
dt <- subset(dt, select = c('NTEE_Cat', 'NAME'))
dt

colors <- c('Spectral')
m <- list(
  l = 200,
  r = 1,
  b = 1,
  t = 100,
  pad = 4
)
p <- plot_ly(dt, labels = ~NTEE_Cat, values = ~Count, type = 'pie',
             hole = 0.4,
             textposition = 'inside',
             textinfo = 'percent',
             insidetextfont = list(color = '#FFFFFF'),
             hoverinfo = 'text',
             text = ~paste(Count, ' IRS Registered Charities & Nonprofits'),
             marker = list(colors = colors,
                           line = list(color = '#FFFFFF', width = 1)),
             width = 1000, height = 800, 
             #The 'pull' attribute can also be used to create space between the sectors
             showlegend = T) %>%
  layout(title = 'U.S. Registered Charities & Nonprofits by Category, (Others = Categories N < 2%)',
         titlefont = list(size = 20),
         autosize = F, 
         margin = m,
         xaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE),
         yaxis = list(showgrid = FALSE, zeroline = FALSE, showticklabels = FALSE))
p
htmlwidgets::saveWidget(p, "donut.html", selfcontained = TRUE)
# chart_link = api_create(p, filename="pie-styled")
# chart_link

