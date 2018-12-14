library(leaflet)
library(rgdal)
library(htmlwidgets)
library(htmltools)

states <- readOGR("cb_2017_us_state_20m/cb_2017_us_state_20m.shp",
                  layer = "cb_2017_us_state_20m", GDAL1_integer64_policy = TRUE)

df_UW <- read.csv('UW_State.csv')
df_FC <- read.csv('FCLoc.csv')
df <- read.csv('State_stats.csv')
df_map <- merge(states, df, by.x=c("STUSPS"), by.y=c("STATE"), all.x = F)
#Format pop-up information
popup_UW <- paste0('<strong>Name: </strong>', 
                   '<br>', df_UW$NAME,
                   '<br><strong>Address: </strong>',
                   '<br>', df_UW$STREET,
                   '<br>', df_UW$CITY, ', ', df_UW$STATE, ' ', df_UW$ZIP,
                   '<br><strong>EIN: </strong>', df_UW$EIN
)
popup_FC <- paste0('<strong>Name: </strong>', df_FC$Name,
                   '<br><strong>Address: </strong>', df_FC$Address
)
popup_Cnt <- paste0('<strong>State: </strong>', df_map$Full.Name,
                    '<strong> Capital: </strong>', df_map$Capital,
                    '<br><strong>Region: </strong>', df_map$REGION,
                    '<br><strong>Number of Charities & Nonprofits: </strong>', df_map$Count
)
popup_rg <- paste0('<strong>Region: </strong>', df_map$REGION)
#=====================================================================================
#Make new icons with different color and pic
icon_1 <- awesomeIcons(icon = 'heart', markerColor = 'blue')
icon_2 <- awesomeIcons(icon = 'search', markerColor = 'red')
#=====================================================================================
#Color Pallette
# pal <- colorQuantile("Greys", domain = df_map$Count, n = 9)
bins <- c(0, 5000, 10000, 20000, 35000, 50000, 70000, 900000, 120000, Inf)
pal <- colorBin("RdYlGn", reverse = T, domain = df_map$Count, bins = bins)
levels(df$REGION)
# Create a continuous palette function
pal2 <- colorFactor("Set2", domain = df_map$REGION)

gmap <- leaflet(df_map) %>%
  # Base groups
  addTiles() %>%
  setView(lng = -105, lat = 40, zoom = 4) %>%
  addPolygons(fillColor = ~pal(Count),
              weight = 2,
              opacity = 1,
              color = "white",
              dashArray = "3",
              fillOpacity = 0.7,
              popup = popup_Cnt,
              group="Number of Organizations by State",
              highlight = highlightOptions(
                                          weight = 5,
                                          color = "#666",
                                          dashArray = "",
                                          fillOpacity = 0.7,
                                          bringToFront = TRUE)) %>%
  addPolygons(fillColor = ~pal2(REGION),
              weight = 2,
              opacity = 1,
              color = "white",
              dashArray = "3",
              fillOpacity = 0.7,
              popup = popup_rg,
              group="Region classified by IRS",
              highlight = highlightOptions(
                weight = 5,
                color = "#666",
                dashArray = "",
                fillOpacity = 0.7,
                bringToFront = TRUE)) %>%
  addLegend(pal = pal2, values = ~REGION, opacity = 0.7, title = NULL, position = "bottomright") %>%
  addLegend(pal = pal, values = ~Count, opacity = 0.7, title = NULL, position = "bottomright") %>%
  # Overlay groups
  # addMarkers(data=df_UW,lat=~lat, lng=~lng, popup=popup_UW, group = "United Way Offices") %>%
  
  #=======================================================================================
#Add markers
  addAwesomeMarkers(data=df_UW,lat=~Lat, lng=~Lng, popup=popup_UW, icon = icon_1, group = "United Way Physical Offices") %>%
  addAwesomeMarkers(data=df_FC,lat=~Lat, lng=~Lng, popup=popup_FC, icon = icon_2, group = "Foundation Center Physical Offices") %>%

  #=======================================================================================
# Layers control
  addLayersControl(
    baseGroups = c("Number of Organizations by State","Region classified by IRS"),
    
    #=====================================================================================
    #Add user options to the map
    overlayGroups = c("United Way Physical Offices", "Foundation Center Physical Offices"),
    #=====================================================================================
    
    options = layersControlOptions(collapsed = FALSE)
  ) #%>%
  # hideGroup("United Way Physical Offices") %>% 
  # hideGroup("Foundation Center Physical Offices")
  # htmlwidgets::prependContent(htmltools::tags$h4("Map: Distribution & Density of Nonprofits by State (i.e. United Ways, Foundation Center)"))
gmap
saveWidget(gmap, 'USNonprofits.html', selfcontained = TRUE)
