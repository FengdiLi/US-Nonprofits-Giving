library(shiny)
library(shinyWidgets)
library(datasets)

# Data pre-processing ----
# Tweak the "am" variable to have nicer factor labels -- since this
# doesn't rely on any user inputs, we can do this once at startup
# and then use the value throughout the lifetime of the app
mpgData <- read.csv('STATE_stats.csv')
names(mpgData) <- c("State","Full.Name","Capital","Region","NumberofOrgs","Asset","Income","Revenue")
mpgData <- subset(mpgData, select = c(4,5,6,7,8))
mpgData$Region <- factor(mpgData$Region, labels = c("Pancific", "Mid", "Northeast"))

values <- as.factor(c("Number of Orgs","Asset","Income","Revenue"))

# Define UI for miles per gallon app ----
ui <- fluidPage(
  
  # App title ----
  titlePanel("Organizational financial indicators distribution by Region"),
  
  # Sidebar layout with input and output definitions ----
  sidebarLayout(
    
    # Sidebar panel for inputs ----
    sidebarPanel(
      # sliderInput("variable", "Variable:", 
      #             min = 1,
      #             max = 4, 
      #             step = 1,
      #             value = values),
      # Input: Selector for variable to plot against mpg ----
      sliderTextInput("variable", "Variable:",
                      grid = T,
                      hide_min_max = T,
                      choices = c("Asset", "Income", "Revenue", "NumberofOrgs"),
                      selected = "Asset"),
      
      # Input: Checkbox for whether outliers should be included ----
      checkboxInput("outliers", "Show outliers", TRUE)
      
    ),
    
    # Main panel for displaying outputs ----
    mainPanel(
      
      # Output: Formatted text for caption ----
      h3(textOutput("caption")),
      
      # Output: Plot of the requested variable against mpg ----
      plotOutput("mpgPlot")
      
    )
  )
)

# Define server logic to plot various variables against mpg ----
server <- function(input, output) {
  
  # Compute the formula text ----
  # This is in a reactive expression since it is shared by the
  # output$caption and output$mpgPlot functions
  formulaText <- reactive({
    paste(input$variable, "~ Region")
  })
  
  # Return the formula text for printing as a caption ----
  output$caption <- renderText({
    formulaText()
  })
  
  # Generate a plot of the requested variable against mpg ----
  # and only exclude outliers if requested
  output$mpgPlot <- renderPlot({
    boxplot(as.formula(formulaText()),
            data = mpgData,
            outline = input$outliers,
            col = "#75AADB", pch = 19)
  })
  
}

# Create Shiny app ----
shinyApp(ui, server)

